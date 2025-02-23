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
    assert('Fetuccine' in recipe_list)
    assert('Linguine' in recipe_list)
    assert('Rigatoni' in recipe_list)

def test_unit_conversion(client):
    pass

def test_serving_sizes(client):
    pass

def test_invalid_title(client):
    pass

def test_invalid_units(client):
    pass

def test_invalid_servings(client):
    pass

