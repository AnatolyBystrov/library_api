# Library API

## Overview
Library API is a Django REST Framework-based API that allows users to manage books, authors, and user authentication with JWT. The API also includes a book recommendation system based on user preferences.

## Features
- User authentication using JWT (Login, Registration)
- CRUD operations for books and authors
- Book search by title or author
- Book recommendation system based on user preferences
- API secured with JWT authentication

## Tech Stack
- **Backend:** Django, Django REST Framework (DRF)
- **Database:** SQLite (can be replaced with PostgreSQL/MySQL)
- **Authentication:** JWT (JSON Web Token)
- **Dev Tools:** Django Extensions, Django Filters, CORS Headers

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/AnatolyBystrov/library_api.git
cd library_api
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional, for Admin Panel)
```bash
python manage.py createsuperuser
```

### 6. Run the Server
```bash
python manage.py runserver
```
Server will start at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|-------------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login and obtain JWT token |

### Books & Authors
| Method | Endpoint | Description |
|--------|-------------|-------------|
| GET | `/api/books/` | Get a list of books |
| POST | `/api/books/` | Add a new book (Auth required) |
| GET | `/api/books/{id}/` | Get book details |
| PUT | `/api/books/{id}/` | Update a book (Auth required) |
| DELETE | `/api/books/{id}/` | Delete a book (Auth required) |
| GET | `/api/authors/` | Get a list of authors |
| POST | `/api/authors/` | Add a new author (Auth required) |

### Book Recommendations
| Method | Endpoint | Description |
|--------|-------------|-------------|
| GET | `/api/books/recommendations/` | Get personalized book recommendations |

## API Request Examples

### Get All Books
```bash
curl http://localhost:8000/api/books/
```

### Get Book by ID
```bash
curl http://localhost:8000/api/books/1/
```

### Create Book
```bash
curl -X POST http://localhost:8000/api/books/ \
    -H "Content-Type: application/json" \
    -d '{"title": "New Book", "author": "Author Name", "isbn": "1234567890123"}'
```

### Update Book
```bash
curl -X PUT http://localhost:8000/api/books/1/ \
    -H "Content-Type: application/json" \
    -d '{"title": "Updated Book", "author": "Updated Author", "isbn": "9876543210987"}'
```

### Delete Book
```bash
curl -X DELETE http://localhost:8000/api/books/1/
```

## Testing
Run unit tests using:
```bash
python manage.py test books
```

## Deployment
To deploy the project:
1. Set up a production database (PostgreSQL recommended)
2. Configure `ALLOWED_HOSTS` and `DEBUG=False` in `settings.py`
3. Use Gunicorn & Nginx for server deployment

## Contact
For any issues, feel free to open a GitHub issue or reach out via email.

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcwNDY3MzQ3LCJpYXQiOjE3Mzg5MzEzNDcsImp0aSI6IjA1OGFkN2JkZjQ5MjQ1MzliYjhmNDM3MWNmNTljMmM4IiwidXNlcl9pZCI6Mn0.tm_YO2ciha7yhp8O7H4jyWAnwGyMoHQ1MJzNsMn05XU"
}

SELECT book_id, AVG(rating) AS avg_rating
FROM user_favorites
GROUP BY book_id
ORDER BY avg_rating DESC
LIMIT 5;
