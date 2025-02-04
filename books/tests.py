from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from books.models import Author  

class LibraryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")

       
        self.author = Author.objects.create(name="Test Author")

        
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass"
        })
        self.token = response.data.get("access")

    def authenticate(self):
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_register_user(self):
       
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password": "password"
        })
        print("DEBUG test_register_user:", response.data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
       
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass"
        })
        print("DEBUG test_login_user:", response.data)  
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

        print("DEBUG test_create_book:", response.data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_authors(self):
        
        response = self.client.get(reverse("author-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recommendation_system(self):
      
        self.authenticate()  # 

        response = self.client.get(reverse("suggested-books-get_recommendations"))

        print("DEBUG test_recommendation_system:", response.data)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
