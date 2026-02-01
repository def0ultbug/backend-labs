
"""
NOTE: This project is a learning exercise for FastAPI, Pydantic, and CRUD concepts.
Not production-ready. Focus is on experimenting with techniques.
"""

from pydantic import BaseModel
from enum import Enum
from typing import Optional


class Task(BaseModel):
    title:str
    description:str
    status:str

class TaskV2(BaseModel):
    title: str
    description: str
    status: str
    priority: str | None = "lower"

class TaskV2WithID(TaskV2):
    id: int


# because id wont be used in the create of the task it will be auto 
class TaskID(Task):
    id : str


class Status(str,Enum):
    INCOMPLETE = 'Incomplete'
    ONGOING = 'Ongoing'

class InsertTask(BaseModel):
    title: Optional[str] = None
    description : Optional[str] = None
    status: Optional[str] = None

