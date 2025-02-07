from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    BookViewSet, AuthorViewSet, FavoriteBookViewSet, SuggestedBooksViewSet,
    RegisterView, LoginView
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'favorites', FavoriteBookViewSet, basename='favorite-books')
router.register(r'suggested-books', SuggestedBooksViewSet, basename="suggested-books")

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('books/search/', BookViewSet.as_view({'get': 'search'}), name="book-search"),
]
