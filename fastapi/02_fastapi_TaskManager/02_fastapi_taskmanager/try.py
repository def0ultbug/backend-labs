"""
NOTE: This file is used for testing functions and logic before integrating them into the main class.
It is meant for experimentation and learning purposes, not for production use.
"""


import csv
from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    title:str
    description:str
    status:str

# because id wont be used in the create of the task it will be auto 
class TaskID(Task):
    id : str


def read_all_tasks():
    try:
        with open("task.csv") as file:
            reader = csv.DictReader(file)
            return [TaskID(**i) for i in reader]
    except FileNotFoundError :
        raise FileNotFoundError('File not Found')
        
def get_task_by_id(id: str) -> Optional[TaskID]:
    for task in read_all_tasks():
        if task.id == id:
            return task
    return None
    

def get_id():
    list_tasks = read_all_tasks()
    return len(list_tasks) + 1

def upadte(id:str,task:dict):
    task_to_update = get_task_by_id(id)
    for field , value in task.items():
        setattr(task_to_update,field,value)
    return task_to_update


l = get_task_by_id('1')
setattr(l,'title','test')
print(l)
print(get_id())
print(upadte(id = "2",task = {'title': 'test2'}))