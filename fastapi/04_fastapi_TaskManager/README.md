# FastAPI CSV Task Manager 📝

A RESTful API built with FastAPI for managing tasks with CSV-based storage. This project demonstrates **advanced FastAPI patterns**, API versioning, and comprehensive API documentation.

## ⚠️ Important Note for Reviewers

This project is a **learning exercise**. Its purpose is to practice modern FastAPI and Python techniques, including:
- Pydantic models and validation
- CRUD operations
- Repository-service separation
- Dependency inversion and type hinting

**Not production-ready:**
- Uses CSV instead of a database
- Minimal error handling
- No concurrency/file-locking handling

Please evaluate it in the context of **learning and experimentation**, not production code.

## 🎯 Project Purpose

This mini-project focuses on learning and implementing:
- **CRUD operations** - Complete Create, Read, Update, Delete functionality
- **RESTful endpoints** - Following REST architectural principles
- **Complex queries and filtering** - Advanced search and filter capabilities
- **API Versioning** - Managing different API versions
- **Swagger Documentation** - Interactive API documentation with OpenAPI

## ✨ Features

- 📋 **Task Management** - Complete CRUD operations for tasks
- 🔍 **Advanced Filtering** - Filter tasks by status, priority, due date, etc.
- 📊 **Query Parameters** - Flexible querying with multiple parameters
- 📚 **API Versioning** - Support for multiple API versions
- 📖 **Interactive Documentation** - Auto-generated Swagger UI and ReDoc
- 💾 **CSV Storage** - File-based persistence (for learning purposes)
- ✅ **Data Validation** - Robust validation using Pydantic models

## 🗂️ Project Structure

```
04_fastapi_TaskManager/
├── 04_fastapi_taskmanager/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point & configuration
│   ├── routers.py           # API route definitions
│   ├── schemas.py           # Pydantic models for validation
│   ├── opr_csv.py           # CSV operations and data access layer
│   ├── task.csv             # CSV file for task storage
│   └── try.py               # Experimental/testing scripts
├── tests/
│   └── __init__.py          # Test files (to be implemented)
├── pyproject.toml           # Poetry dependencies and project config
├── poetry.lock              # Locked dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Poetry (for dependency management)

### Installation

#### Using Poetry
```bash
# Navigate to project directory
cd 04_fastapi_TaskManager

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Running the Application
```bash
# Start the development server
python -m 04_fastapi_taskmanager.main

# Or if main.py has a run configuration:
python 04_fastapi_taskmanager/main.py

# The API will be available at:
# http://localhost:8000

# Interactive API documentation:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

## 📡 API Endpoints

### Task Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/Tasks/` | Get all tasks (with optional filters)|
| `POST` | `/Tasks/` | Create a new task |
| `GET` | `/Tasks/sreach` | Search tasks |
| `GET` | `/Tasks/v2/tasks` | Get tasks (Version 2) |
| `GET` | `/Tasks/{id_task}` | Get a specific task by ID |
| `PUT` | `/Tasks/{id_task}` | Update an existing task |
| `DELETE` | `/Tasks/{id_task}` | Delete a task |

### Query Parameters & Filtering

The API supports advanced filtering through query parameters:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `status` | string | Filter by task status | `?status=completed` |
| `title` | string | Filter by task title | `?title=Task 1` |
| `keyword` | string | Filter by keyword | `?keyword=A` |

### Example Requests

#### Get All Tasks
```bash
curl http://localhost:8000/tasks
```

#### Get Tasks with Filters
```bash
# Filter by status
curl "http://localhost:8000/tasks?status=Ongoing"

# Filter by multiple criteria
curl "http://localhost:8000/tasks?keyword=a"

```

#### Create a New Task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete FastAPI project",
    "description": "Finish the task manager API",
    "status": "Ongoing",
  }'
```

#### Get a Specific Task
```bash
curl http://localhost:8000/tasks/1
```

#### Update a Task (Full Update)
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete FastAPI project - Updated",
    "description": "Finish and document the task manager API",
    "status": "Ongoing"
  }'
```

#### Partial Update (PATCH)
```bash
curl -X PATCH "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

#### Delete a Task
```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## 🔄 API Versioning

This project implements API versioning to demonstrate how to manage different versions of your API:

```bash
# Version 1
curl http://localhost:8000/v1/tasks

# Version 2 (with enhanced features)
curl http://localhost:8000/v2/tasks
```

**Version differences:**
- **v1**: Basic CRUD operations
- **v2**: Enhanced with new field 

## 📚 API Documentation

The API comes with auto-generated interactive documentation:

### Swagger UI
Visit `http://localhost:8000/docs` for interactive API testing with:
- Visual endpoint exploration
- Request/response examples
- Try-it-out functionality
- Schema definitions

### ReDoc
Visit `http://localhost:8000/redoc` for a clean, readable documentation interface:
- Three-panel design
- Schema explorer
- Code samples
- Detailed descriptions

### OpenAPI Specification
Access the raw OpenAPI JSON at `http://localhost:8000/openapi.json`

## 🎓 What I Learned

- ✅ Building RESTful APIs with FastAPI
- ✅ Implementing complete CRUD operations
- ✅ Advanced query parameters and filtering
- ✅ API versioning strategies
- ✅ Pydantic models for data validation
- ✅ Auto-generating API documentation with Swagger/OpenAPI
- ✅ Repository pattern for data access
- ✅ Dependency injection patterns
- ✅ Type hinting and modern Python practices

## 🛠️ Technologies Used

- **FastAPI** - Modern web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Python CSV** - File-based data storage
- **Uvicorn** - ASGI server for running FastAPI
- **Poetry** - Dependency management


## 🐛 Known Limitations

- **CSV Storage** - Not suitable for production; no ACID properties
- **No Concurrency Control** - File locking not implemented
- **Limited Validation** - Basic validation only
- **No Authentication** - API is publicly accessible
- **No Data Relationships** - No support for complex data models
- **Performance** - CSV reads entire file into memory
- **No Transactions** - Cannot rollback failed operations

```

## 📝 Sample Data Format (task.csv)

```csv
id,title,description,status
1,Task One,Description One,Incomplete
2,Task Two,Description Two,Ongoing
```

## 📄 License

MIT License - Free to use for learning purposes.

---

**Part of:** Backend Development Learning Journey 🚀

💡 **Learning Focus:** Mastering FastAPI routing, RESTful API design, API documentation, and modern Python development practices.

## 🤝 Contributing

This is a learning project, but feedback and suggestions are welcome! Feel free to:
- Open issues for bugs or suggestions
- Submit pull requests for improvements
- Share your learning experience


*Built with ❤️ while learning FastAPI and modern Python development*