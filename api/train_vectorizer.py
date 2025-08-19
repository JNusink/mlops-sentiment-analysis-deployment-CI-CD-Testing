import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Load data with error handling
try:
    df = pd.read_csv("IMDB Dataset.csv", encoding='utf-8')
    X = df["review"]
    if X.empty or X.isnull().all():
        raise ValueError("No valid review data found in IMDB Dataset.csv")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit(1)

# Vectorize
try:
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
    vectorizer.fit(X)
    print(f"Vectorized {len(X)} reviews successfully")
except Exception as e:
    print(f"Error during vectorization: {e}")
    exit(1)

# Save vectorizer with validation
try:
    with open("vectorizer.pkl", "wb") as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)
    print("vectorizer.pkl generated successfully")
except Exception as e:
    print(f"Error saving vectorizer: {e}")
    exit(1)
