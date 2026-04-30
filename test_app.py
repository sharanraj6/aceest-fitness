import pytest
from app import app, init_db
import sqlite3
import os

@pytest.fixture
def client():
    
    app.config['TESTING'] = True
    init_db()
    with app.test_client() as client:
        yield client
    
    if os.path.exists("aceest_fitness.db"):
        os.remove("aceest_fitness.db")

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b"healthy" in response.data

def test_add_client(client):
    payload = {
        "name": "John Doe",
        "weight": 80.0,
        "program": "Muscle Gain"
    }
    response = client.post('/client', json=payload)
    assert response.status_code == 201
    
    assert response.json['calories'] == 2800