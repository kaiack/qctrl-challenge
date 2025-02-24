import json
import pytest
from server import app


# fixture allows for resuable code across tests, 
# in this case we need a test client for each test.
@pytest.fixture()
def client():
    # flask provides a test client which allows you to send requests to it directly rather than 
    # having a server running on a port and then sending requests to that.
    return app.test_client()

def test_list_recipes(client):
    response = client.get('/recipes')
    recipe_list = json.loads(response.data)
    assert('Penne' in recipe_list)
    assert('Linguine' in recipe_list)
    assert('Penne Arrabbiata' in recipe_list)
    assert('Chicken Stir-Fry' in recipe_list)
    assert('Pancakes' in recipe_list)
    assert('Chips' not in recipe_list)

def test_unit_conversion(client):
    response = client.get('/recipe?title=Chicken%20Stir-Fry')
    ingredients_metric = json.loads(response.data)

    response2 = client.get('/recipe?title=Chicken%20Stir-Fry&mass=lb&volume=floz')
    ingredients_imperial = json.loads(response2.data)
    assert(len(ingredients_metric) == len(ingredients_imperial))

    LB_TO_G = 450
    FLOZ_TO_ML = 340

    # Loop through, check all units were converted and converted quantities are correct
    for i in range(len(ingredients_metric)):
        assert(ingredients_imperial[i]['unit'] in ['lb', 'floz']) 

        if ingredients_metric[i]["unit"] == "g":
            assert(round(ingredients_metric[i]["quantity"] / LB_TO_G, 2) == ingredients_imperial[i]['quantity'])
        else:
            assert(round(ingredients_metric[i]["quantity"] / FLOZ_TO_ML, 2) == ingredients_imperial[i]['quantity'])


def test_serving_sizes(client):
    response = client.get('/recipe?title=Pancakes')
    ingredients_single = json.loads(response.data)

    response2 = client.get('/recipe?title=Pancakes&servings=4')
    ingredients_quadruple = json.loads(response2.data)

    # Check all ingredients are 4x larger.
    assert(len(ingredients_single) == len(ingredients_quadruple))

    for i in range(len(ingredients_single)):
        assert(ingredients_single[i]['quantity'] * 4 == ingredients_quadruple[i]['quantity'])

def test_unit_and_servings(client):
    OZ_TO_G = 28
    response = client.get('/recipe?title=Pancakes')
    ingredients_single = json.loads(response.data)

    # Check unit conversion doesn affect servings
    response3 = client.get('/recipe?title=Pancakes&mass=oz&servings=2')
    ingredients_oz = json.loads(response3.data)

    for j in range(len(ingredients_oz)):
        if ingredients_single[j]['unit'] == 'g':
            assert(round(ingredients_single[j]['quantity'] * 2 / OZ_TO_G, 2) == ingredients_oz[j]['quantity'])
        else:
            assert(round(ingredients_single[j]['quantity'] * 2, 2) == ingredients_oz[j]['quantity'])

def test_invalid_title(client):
    response = client.get('/recipe?title=pizza')
    assert(response.status_code == 400)
    assert(response.data.decode('utf-8') == "Recipe not found")

def test_invalid_params(client):
    response = client.get('/recipe?title=Pancakes&mass=K')
    assert(response.status_code == 400)
    assert(response.data.decode('utf-8') == "Please specify valid units for mass and/or volume")

    response = client.get('/recipe?title=Pancakes&volume=L')
    assert(response.status_code == 400)
    assert(response.data.decode('utf-8') == "Please specify valid units for mass and/or volume")

    response = client.get('/recipe?title=Pancakes&servings=0')
    assert(response.status_code == 400)
    assert(response.data.decode('utf-8') == "Servings should be a positive integer")

    response = client.get('/recipe?title=Pancakes&servings=-1')
    assert(response.status_code == 400)
    assert(response.data.decode('utf-8') == "Servings should be a positive integer")

    

