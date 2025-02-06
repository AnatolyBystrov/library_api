from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from books.models import Book, Author, FavoriteBook
from books.services import get_personalized_recommendations
import time

class LibraryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.author = Author.objects.create(name="Test Author")
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "testpass"}, format="json")
        self.token = response.data.get("access")

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_register_user(self):
        response = self.client.post(reverse("register"), {"username": "newuser", "password": "password"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "testpass"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_books(self):
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        self.authenticate()
        response = self.client.post(reverse("book-list"), {
            "title": "New Book",
            "author": self.author.id,
            "isbn": "9783161484100",
            "published_date": "2025-01-01",
            "genre": "Fiction"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_authors(self):
        response = self.client.get(reverse("author-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recommendation_system(self):
        self.authenticate()
        response = self.client.get(reverse("suggested-books-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RecommendationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")
        self.book1 = Book.objects.create(title="Book A", author=self.author1, genre="Fiction", average_rating=4.5, isbn="978-1-111-11111-1")
        self.book2 = Book.objects.create(title="Book B", author=self.author1, genre="Fiction", average_rating=4.0, isbn="978-1-222-22222-2")
        self.book3 = Book.objects.create(title="Book C", author=self.author2, genre="Science", average_rating=3.5, isbn="978-1-333-33333-3")
        FavoriteBook.objects.create(user=self.user, book=self.book1)

    def test_recommendations_with_favorites(self):
        start_time = time.time()
        recommendations = get_personalized_recommendations(self.user, n=5)
        execution_time = time.time() - start_time
        self.assertGreater(len(recommendations), 0)
        self.assertNotIn(self.book1, recommendations)
        self.assertLess(execution_time, 1)

    def test_recommendations_without_favorites(self):
        new_user = User.objects.create_user(username="newuser", password="password")
        recommendations = get_personalized_recommendations(new_user, n=5)
        self.assertGreater(len(recommendations), 0)

    def test_recommendations_different_users(self):
        another_user = User.objects.create_user(username="anotheruser", password="password")
        FavoriteBook.objects.create(user=another_user, book=self.book3)
        recommendations_user1 = get_personalized_recommendations(self.user, n=5)
        recommendations_user2 = get_personalized_recommendations(another_user, n=5)
        self.assertNotEqual(recommendations_user1, recommendations_user2)
