import uvicorn
from fastapi import FastAPI
from routers.Books import router as book_router

app = FastAPI(
    title="Book Inventory API",
    description="""
A RESTful API for managing and querying a book inventory.

It allows clients to:
- Browse available books
- Check stock availability
- Add a Book
- Retrieve book details by title or author
""",
    version="0.1.0",
)

app.include_router(book_router)

def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()