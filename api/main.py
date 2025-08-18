from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI()

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "sentiment_model.pkl")
vectorizer_path = os.path.join(script_dir, "vectorizer.pkl")
log_dir = "/app/logs"  # Explicit volume mount path

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)
    print("Model and vectorizer loaded successfully")
except Exception as e:
    print(f"Error loading files: {e}")
    raise HTTPException(status_code=500, detail=f"Failed to load model or vectorizer: {e}")

class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict(input: TextInput):
    if not input.text:
        raise HTTPException(status_code=400, detail="Text is required")
    text_vector = vectorizer.transform([input.text])
    prediction = model.predict(text_vector)[0]
    confidence = model.predict_proba(text_vector)[0].max()
    sentiment = "positive" if prediction == 1 else "negative"
    response = {"sentiment": sentiment, "confidence": float(confidence)}

    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "sentiment.log")
    with open(log_file, "a") as f:
        f.write(json.dumps(response) + "\n")

    return response