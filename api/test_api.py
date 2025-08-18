import pytest
import os

@pytest.fixture(autouse=True)
def change_test_dir():
    os.chdir(os.path.dirname(__file__))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict_positive():
    response = client.post("/predict", json={"text": "This movie is awesome!"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "positive"
    assert 0 <= data["confidence"] <= 1

def test_predict_negative():
    response = client.post("/predict", json={"text": "This movie is terrible."})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "negative"
    assert 0 <= data["confidence"] <= 1

def test_predict_missing_data():
    response = client.post("/predict", json={})
    assert response.status_code == 422

def test_predict_malformed_data():
    response = client.post("/predict", json={"text": 123})
    assert response.status_code == 422