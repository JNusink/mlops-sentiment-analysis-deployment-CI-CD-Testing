import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Load dataset
df = pd.read_csv("IMDB Dataset.csv")
X = df["review"]

# Create and fit vectorizer
vectorizer = TfidfVectorizer(max_features=5000)
vectorizer.fit(X)

# Save vectorizer
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)