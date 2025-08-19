import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Load data
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "IMDB Dataset.csv")

df = pd.read_csv(csv_path)
X = df["review"]
y = df["sentiment"].map({"positive": 1, "negative": 0})

# Vectorize and train
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X_vectorized = vectorizer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model and vectorizer
with open("sentiment_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)
