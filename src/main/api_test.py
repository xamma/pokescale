from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_get_test():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "this is a test"}

def test_render_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Pokéscale" in response.text

def test_render_pokemon_valid():
    response = client.post("/pokemon", data={"pokemon_name": "pikachu"})
    assert response.status_code == 200
    assert "Info about Pikachu" in response.text
