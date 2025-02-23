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

def test_unit_conversion(client):
    response = client.get('/recipe?title=Chicken%20Stir-Fry')
    ingredients_metric = json.loads(response.data)

    response2 = client.get('/recipe?title=Chicken%20Stir-Fry&mass=lb&volume=floz')
    ingredients_converted = json.loads(response2.data)
    assert(len(ingredients_metric) == len(ingredients_converted))

    LB_TO_G = 450
    FLOZ_TO_ML = 340

    # Loop through, check all units were converted and converted quantities are correct
    for i in range(len(ingredients_metric)):
        assert(ingredients_converted[i]['unit'] in ['lb', 'floz']) 
        
        if ingredients_metric[i]["unit"] == "g":
            assert(round(ingredients_metric[i]["quantity"] / LB_TO_G, 2) == ingredients_converted[i]['quantity'])
        else:
            assert(round(ingredients_metric[i]["quantity"] / FLOZ_TO_ML, 2) == ingredients_converted[i]['quantity'])


def test_serving_sizes(client):
    pass

def test_invalid_title(client):
    pass

def test_invalid_units(client):
    pass

def test_invalid_servings(client):
    pass

