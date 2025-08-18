from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_predict_positive():
    response = client.post("/predict", json={"text": "This movie is awesome!"})
    assert response.status_code == 200
    assert response.json()["sentiment"] == "positive"
    assert 0 <= response.json()["confidence"] <= 1


def test_predict_negative():
    response = client.post("/predict", json={"text": "This movie is terrible!"})
    assert response.status_code == 200
    assert response.json()["sentiment"] == "negative"
    assert 0 <= response.json()["confidence"] <= 1


def test_predict_malformed():
    response = client.post("/predict", json={})
    assert response.status_code == 422
    assert "detail" in response.json()
