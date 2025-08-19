import pickle

try:
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    print("Loaded successfully:", vectorizer)
except Exception as e:
    print(f"Failed to load vectorizer: {e}")
