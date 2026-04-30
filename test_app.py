import pytest
from app import app, init_db
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    init_db("test_aceest.db")
    with app.test_client() as client:
        yield client
    if os.path.exists("test_aceest.db"):
        os.remove("test_aceest.db")

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_add_client(client):
    payload = {
        "name": "Jane Doe",
        "age": 28,
        "weight": 60.0,
        "program": "Fat Loss (FL)"
    }
    response = client.post('/add_client', json=payload)
    assert response.status_code == 201
    assert response.json['calories'] == 1320 # 60 * 22