from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books", db_index=True)
    published_date = models.DateField(null=True, blank=True, db_index=True)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=255, blank=True, db_index=True)  
    average_rating = models.FloatField(default=0.0, db_index=True)  

    class Meta:
        ordering = ['-published_date']  

    def __str__(self):
        return self.title

class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="favorited_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
