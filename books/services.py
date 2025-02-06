import json
import pandas as pd
from pathlib import Path
from django.db.models import Q
from .models import Book, FavoriteBook

BOOKS_FILE = Path("/mnt/data/books_filtered.json")

def load_books(limit=10000):
    data = []
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            data.append(json.loads(line))
    return pd.DataFrame(data)

def get_personalized_recommendations(user, n=10):
    favorite_books = FavoriteBook.objects.filter(user=user).values_list("book__id", flat=True)
    if not favorite_books:
        return get_top_books(n)
    
    favorite_genres = Book.objects.filter(id__in=favorite_books).values_list("genre", flat=True)
    recommended_books = Book.objects.filter(genre__in=favorite_genres).exclude(id__in=favorite_books)
    
    return recommended_books.order_by("-average_rating")[:n]

def get_top_books(n=10):
    return Book.objects.all().order_by("-average_rating")[:n]
