from rest_framework import serializers
from .models import Book, Author, FavoriteBook
from django.contrib.auth.models import User


from rest_framework import serializers
from .models import Book, Author, FavoriteBook

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'isbn': {'max_length': 13}  # Максимум 13 символов!
        }

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class FavoriteBookSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FavoriteBook
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]