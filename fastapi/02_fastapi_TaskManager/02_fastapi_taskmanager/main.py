"""
NOTE: This project is a learning exercise for FastAPI, Pydantic, and CRUD concepts.
Not production-ready. Focus is on experimenting with techniques.
"""

import uvicorn
from fastapi import FastAPI
from routers import router

app = FastAPI(
    title="Task Manager API",
    description="This is a task management API",
    version="0.1.0",
)

app.include_router(router)

def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()