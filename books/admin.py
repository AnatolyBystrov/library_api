from django.contrib import admin
from .models import Book, Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date", "isbn")
    list_filter = ("published_date",)
    search_fields = ("title", "author__name", "isbn")
