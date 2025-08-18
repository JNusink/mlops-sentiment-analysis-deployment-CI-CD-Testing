import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Load data
df = pd.read_csv("IMDB Dataset.csv")
X = df["review"]

# Vectorize
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
vectorizer.fit(X)

# Save vectorizer
with open("vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

# Add newline at end