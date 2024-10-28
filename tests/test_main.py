from fastapi.testclient import TestClient
from main import app
from models.db import db

client = TestClient(app)

def test_add_sheep():
    new_sheep = {
        "id": 7,
        "name": "Luna",
        "breed": "Suffolk",
        "sex": "ewe"
    }
    response = client.post("/sheep", json=new_sheep)
    assert response.status_code == 201
    assert response.json() == new_sheep

    get_response = client.get(f"/sheep/{new_sheep['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == new_sheep

def test_delete_sheep():
    new_sheep = {"id": 8, "name": "Bessie", "breed": "Suffolk", "sex": "ewe"}
    client.post("/sheep", json=new_sheep)
    response = client.delete("/sheep/8")
    assert response.status_code == 204

    get_response = client.get("/sheep/8")
    assert get_response.status_code == 404

def test_update_sheep():
    new_sheep = {"id": 9, "name": "Charlie", "breed": "Merino", "sex": "ram"}
    client.post("/sheep", json=new_sheep)

    updated_sheep = {"id": 9, "name": "Charlie", "breed": "Texel", "sex": "ram"}
    response = client.put("/sheep/9", json=updated_sheep)
    assert response.status_code == 200
    assert response.json() == updated_sheep

    get_response = client.get("/sheep/9")
    assert get_response.status_code == 200
    assert get_response.json() == updated_sheep

def test_read_all_sheep():
    db.data.clear()
    sheep1 = {"id": 10, "name": "Dolly", "breed": "Finn", "sex": "ewe"}
    sheep2 = {"id": 11, "name": "Lassie", "breed": "Lincoln Longwool", "sex": "ram"}
    client.post("/sheep", json=sheep1)
    client.post("/sheep", json=sheep2)

    response = client.get("/sheep")
    assert response.status_code == 200
    assert response.json() == [sheep1, sheep2]
