import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Load dataset
df = pd.read_csv("IMDB Dataset.csv")
X = df["review"]
y = df["sentiment"].map({"positive": 1, "negative": 0})

# Vectorize and train (using a subset for speed)
vectorizer = TfidfVectorizer(max_features=5000)
X_vectorized = vectorizer.fit_transform(X[:1000])  # First 1000 rows
model = LogisticRegression(max_iter=1000)
model.fit(X_vectorized, y[:1000])

# Save model and vectorizer
with open("sentiment_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("New sentiment model and vectorizer created")