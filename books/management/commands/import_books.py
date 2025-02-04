import os
import json
from django.core.management.base import BaseCommand
from books.models import Book, Author

class Command(BaseCommand):
    help = "Import books from JSON file"

    def handle(self, *args, **kwargs):
        input_file = os.path.join("data", "kaggle", "working", "books_filtered.json")

        if not os.path.exists(input_file):
            self.stderr.write(f"❌ File not found: {input_file}")
            return

        self.stdout.write(f"📂 Loading data from {input_file}...")

        with open(input_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                self.stderr.write(f"⚠️ JSON parsing error: {e}")
                return

        for item in data:
            author_name = item.get("author_name")

            if not author_name:
                authors = item.get("authors", [])
                if authors:
                    author_name = authors[0].get("name", "Unknown Author")
                else:
                    author_name = "Unknown Author"

            author, _ = Author.objects.get_or_create(name=author_name)

            isbn = item.get("isbn", "")
            if not isbn:
                self.stderr.write(f"⚠️ Skipping book without ISBN: {item.get('title', 'Unknown Title')}")
                continue

            book, created = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "title": item.get("title", "Unknown Title"),
                    "published_date": item.get("published_date"),
                    "author": author
                }
            )

            if created:
                self.stdout.write(f"✅ Added book: {book.title}")
            else:
                self.stdout.write(f"⚠️ Book already exists: {book.title}")

        self.stdout.write("🎉 Import completed!")
