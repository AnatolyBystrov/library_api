from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg, Q
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Book, Author, FavoriteBook
from .serializers import BookSerializer, AuthorSerializer, FavoriteBookSerializer, UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'author__name']

    @action(detail=False, methods=['get'])
    def top_books(self, request):
        cache_key = "top_books"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        top_books = (
            Book.objects.annotate(avg_rating=Avg('favorited_by__user'))
            .order_by('-avg_rating')[:10]
        )

        serialized_data = BookSerializer(top_books, many=True).data
        cache.set(cache_key, serialized_data, timeout=3600)
        return Response(serialized_data)

    @action(detail=False, methods=['get'])
    def books_by_genre(self, request):
        genre = request.query_params.get('genre', None)
        if genre:
            books = Book.objects.filter(genre__icontains=genre)
            return Response(BookSerializer(books, many=True).data)
        return Response({"error": "Genre parameter is required"}, status=400)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """🔍 Поиск книг по названию или имени автора"""
        query = request.GET.get("query", "").strip()
        if not query:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        books = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']

    @action(detail=False, methods=['get'])
    def top_authors(self, request):
        cache_key = "top_authors"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        top_authors = (
            Author.objects.annotate(fav_count=Count('books__favorited_by'))
            .order_by('-fav_count')[:5]
        )

        serialized_data = AuthorSerializer(top_authors, many=True).data
        cache.set(cache_key, serialized_data, timeout=3600)
        return Response(serialized_data)


class FavoriteBookViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteBook.objects.filter(user=self.request.user).select_related('book', 'user')


class SuggestedBooksViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cache_key = f"user_recommendations_{user.id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Book.objects.filter(id__in=cached_data)

        favorite_books = FavoriteBook.objects.filter(user=user).values_list('book', flat=True)
        if not favorite_books:
            return Book.objects.none()

        favorite_authors = (
            Book.objects.filter(id__in=favorite_books)
            .values_list('author', flat=True)
            .distinct()
        )

        recommended_books = (
            Book.objects.filter(author__in=favorite_authors)
            .exclude(id__in=favorite_books)
            .select_related('author')
            .annotate(fav_count=Count('favorited_by'))
            .order_by('-fav_count')[:5]
        )

        recommended_books_ids = list(recommended_books.values_list('id', flat=True))
        cache.set(cache_key, recommended_books_ids, timeout=3600)

        return recommended_books

    @action(detail=False, methods=['get'], url_path="get-recommendations")
    def get_recommendations(self, request):
        queryset = self.get_queryset()
        if queryset.exists():
            return Response(BookSerializer(queryset, many=True).data, status=200)
        return Response({"message": "No recommendations available."}, status=404)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "User created successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
