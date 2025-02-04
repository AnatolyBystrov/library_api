import json
import pandas as pd
from pathlib import Path


BOOKS_FILE = Path("/kaggle/input/large-books-metadata-dataset-50-mill-entries/books.json/books.json")

def load_books(limit=10000):
    
    data = []
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= limit: 
                break
            data.append(json.loads(line))
    return pd.DataFrame(data)

def get_top_books(n=10):
    df = load_books()
    return df[["id", "title", "author_name", "average_rating"]].sort_values(
        by="average_rating", ascending=False
    ).head(n)
