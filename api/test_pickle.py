import os
import pickle
import pytest


def test_pickle_files_exist():
    if not (
        os.path.exists("sentiment_model.pkl")
        and os.path.exists("vectorizer.pkl")
    ):
        pytest.skip("Model/vectorizer pickle files not available.")

    with open("sentiment_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)

    with open("vectorizer.pkl", "rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    assert model is not None
    assert vectorizer is not None
