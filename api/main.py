from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import logging
import os

app = FastAPI()

# Set up logging
log_dir = "/app/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(filename=os.path.join(log_dir, "sentiment.log"),
                    level=logging.INFO,
                    format="%(asctime)s - %(message)s")





class TextInput(BaseModel):
    text: str





# Load model and vectorizer
with open("sentiment_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)





@app.post("/predict")
async def predict_sentiment(input_data: TextInput):
    try:
        text_vectorized = vectorizer.transform([input_data.text])
        confidence = model.predict_proba(text_vectorized)[0][
            model.predict(text_vectorized)[0]
        ]
        sentiment = "positive" if model.predict(text_vectorized)[0] == 1 else "negative"
        logging.info(f"Text: {input_data.text}, Sentiment: {sentiment}, "
                     f"Confidence: {confidence:.2f}")
        return {"sentiment": sentiment, "confidence": float(confidence)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


