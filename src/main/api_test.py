from fastapi.testclient import TestClient
from api import app

# Initializing Test client for api
client = TestClient(app)

# testing test_route
def test_get_test():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "this is a test"}

# testing root_route
def test_render_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Pokéscale" in response.text

# testing pokemon_route
def test_render_pokemon_valid():
    response = client.post("/pokemon", data={"pokemon_name": "pikachu"})
    assert response.status_code == 200
    assert "Info about Pikachu" in response.text
