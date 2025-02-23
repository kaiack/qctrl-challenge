from typing import Dict, List, Tuple
from flask import Flask, request
import json

DEFAULT_MASS_UNIT="g"
DEFAULT_VOLUME_UNIT="ml"
DEFAULT_SERVING_SIZE="1"
DECIMAL_PLACES = 2
DB_FILE = ""

# https://en.wikibooks.org/wiki/Cookbook:Units_of_measurement

# For converting grams to other units
mass_conversions = {
    "g" : 1,
    "lb" : 450
}

# For converting ml to other units
volume_conversions = {
    "ml" : 1,
    "floz": 340
}

app = Flask(__name__)

'''
Open recipes json file and return the titles of all the recipes
'''
def listRecipes() -> List[str]:
    with open('recipes.json') as f:
        recipes = json.load(f)
        return list(recipes.keys())

'''
Find the recipe with given title. Convert the units if applicable. Scale the servings.
Returns a list of ingredients with converted units and scaled servings.
'''
def fetchRecipe(title:str, mass_unit:str, volume_unit:str, servings:int) -> List[Dict[str, str | int]]:

    with open('recipes.json') as f:
        recipes = json.load(f)
        recipe = recipes[title]

        # Convert from grams/ml to specified mass/volume unit.
        for ingredient in recipe:
            if ingredient['unit'] == "g":
                ingredient['quantity'] = round(ingredient['quantity'] / mass_conversions[mass_unit], DECIMAL_PLACES)
                ingredient['unit'] = mass_unit
            else:
                ingredient['quantity'] = round(ingredient['quantity'] / volume_conversions[volume_unit], DECIMAL_PLACES)
                ingredient['unit'] = volume_unit
            
            # Scale up values based on servings
            ingredient["quantity"] *= servings

    return recipe

'''
Validate the received params.
I think django has form validation that would do something similar 
and there are other libraries that do similar stuff but I'm
keeping things simple here
'''
def validate_recipe_params(mass_unit:str, volume_unit:str, servings:str) -> Tuple[bool, str]:
    # Check mass_unit, volume_unit are supported units.
    if mass_unit not in mass_conversions or volume_unit not in volume_conversions:
        return False, "Please specify valid units for mass and/or volume"
    
    # Validate that servings is a positive integer
    if not servings.isdigit() or int(servings) <= 0:
        return False, "Servings should be a positive integer"
    
    return True, ""



# --------------------------------------------------- API ROUTES ---------------------------------------------------


@app.route('/recipes')
def getRecipes():
    try:
        response = listRecipes()
    except:
        return "Something went wrong", 500 

    return response

'''
Users specify mass/volume units based on a list of supported units.
They also specify a number of servings.
'''
@app.route('/recipe')
def getRecipe():
    title = request.args.get("title")

    if not title:
        return 'Bad request!', 400

    # configuration params from query string, with fallback default values.
    mass_unit = request.args.get("mass", DEFAULT_MASS_UNIT)
    volume_unit = request.args.get("volume", DEFAULT_VOLUME_UNIT)
    servings = request.args.get("servings", DEFAULT_SERVING_SIZE)

    is_valid, msg = validate_recipe_params(mass_unit, volume_unit, servings)

    if not is_valid:
        return msg, 400
        
    servings = int(servings)

    try:
        response = fetchRecipe(title, mass_unit, volume_unit, servings)
    except KeyError:
        return "Recipe not found", 400
    except Exception as e:
        print(e) # Pretend this is some kind of logger
        return "Something went wrong", 500

    return response
    