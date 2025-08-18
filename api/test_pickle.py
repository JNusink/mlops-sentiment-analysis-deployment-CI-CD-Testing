import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

with open("sentiment_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
print("Model and vectorizer loaded successfully")