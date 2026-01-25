# Book Inventory API 📚

A RESTful API built with FastAPI for managing and querying a book inventory. This project demonstrates **FastAPI routing patterns** and API organization best practices.

## 🎯 Project Purpose

This mini-project focuses on learning and implementing:
- **FastAPI Router** - Organizing endpoints with `APIRouter`
- **Route organization** - Separating concerns across multiple routers
- **CRUD operations** - Complete Create, Read, Update, Delete functionality
- **Path parameters** - Dynamic routing with book IDs and titles
- **Request validation** - Using Pydantic models for data validation

## ✨ Features

- 📖 **Browse Books** - View all books in inventory
- 🔍 **Search** - Find book by id
- ➕ **Add Books** - Add new books to inventory
- ✏️ **Update Book** - Modify existing book details
- 🗑️ **Delete Book** - Remove books from inventory


## 🗂️ Project Structure
```
01_fastapi-router/
├── 01_fastapi_router/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point & router registration
│   ├── db.py                # In-memory database instance
│   ├── routers/
│   │   └── Books.py         # Book CRUD operations router
│   └── schemas/
│       └── Book.py          # Pydantic models (Book, Database)
├── tests/
│   └── __init__.py          # Test files (to be implemented)
├── pyproject.toml           # Poetry dependencies and project config
├── poetry.lock              # Locked dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Poetry

### Installation

#### Using Poetry
```bash
# Navigate to project directory
cd 01_fastapi-router

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Running the Application
```bash
# Start the development server
python3 main.py

# The API will be available at:
# http://localhost:8000

# Interactive API documentation:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

## 📡 API Endpoints

### Book Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/Books` | Get all books |
| `GET` | `/Books/{id_book}` | Get a specific book by ID |
| `POST` | `/Books` | Add a new book |
| `PATCH` | `/Books/{id_book}` | Update an existing book |
| `DELETE` | `/Books/{id}` | Delete a book |

### Example Requests

#### Get All Books
```bash
curl http://localhost:8000/Books
```

#### Add a New Book
```bash
curl -X POST "http://localhost:8000/Books" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "title": "The Pragmatic Programmer",
    "author": "Andrew Hunt",
    "stock": 5,
    "price": 49.99
  }'
```

#### Update a Book
```bash
curl -X PATCH "http://localhost:8000/Books/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Pragmatic Programmer",
    "author": "Andrew Hunt & David Thomas",
    "stock": 10,
    "price": 45.99
  }'
```

#### Delete a Book
```bash
curl -X DELETE "http://localhost:8000/Books/1"
```

**Note:** This project uses an **in-memory dictionary** as a dummy database for learning purposes. Data will be lost on server restart.


## 🎓 What I Learned

- ✅ How to structure FastAPI applications with routers
- ✅ Organizing endpoints by functionality
- ✅ Using path and query parameters
- ✅ Request and response validation with Pydantic
- ✅ HTTP methods (GET, POST, PATCH, DELETE) for RESTful APIs


## 🔄 Future Enhancements

- [ ] Add pagination for book listings
- [ ] Implement filtering (by price range, year, etc.)
- [ ] Add authentication and authorization
- [ ] Connect to a real database (PostgreSQL/SQLite)
- [ ] Add unit tests with pytest
- [ ] Implement error handling and custom exceptions
- [ ] Add logging for debugging
- [ ] Rate limiting


## 🐛 Known Limitations

- **No persistence** - Data is stored in memory and lost on restart
- **No concurrent access handling** - Not thread-safe for production
- **Simple validation** - Minimal business logic validation
- **No authentication** - API is publicly accessible


## 📄 License

MIT License - Free to use for learning purposes.

---

**Part of:** [Backend Labs](https://github.com/def0ultbug/backend-labs) 🔬

💡 **Learning Focus:** Understanding FastAPI routing architecture and RESTful API design patterns.
