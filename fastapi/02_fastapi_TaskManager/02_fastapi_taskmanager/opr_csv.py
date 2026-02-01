"""
NOTE: This project is a learning exercise for FastAPI, Pydantic, and CRUD concepts.
Not production-ready. Focus is on experimenting with techniques.
"""

import csv
from typing import Optional
from schemas import Task,TaskID,TaskV2WithID

class OpsCSV():
    DATABASE_NAME = "task.csv"
    FIELDS = [
        "id", "title", "description", "status"
    ]
    
    def all(self)->list[TaskID]:
        with open(OpsCSV.DATABASE_NAME) as file:
            reader = csv.DictReader(file)
            return [TaskID(**i) for i in reader]
    
    def read_all_tasks_v2(self) -> list[TaskV2WithID]:
        with open(OpsCSV.DATABASE_NAME) as file:
            reader = csv.DictReader(file)
            return [TaskV2WithID(**row) for row in reader]

    
    def get_task_by_id(self, id: str) -> Optional[TaskID]:
        for task in self.all():
            if task.id == id:
                return task
        return None
    
    def get_id(self) -> int:
        tasks = self.all()
        if not tasks:
            return 1
        return max(int(task.id) for task in tasks) + 1 

    def save(self,task : TaskID)-> None:
        try:
            with open(OpsCSV.DATABASE_NAME, mode="a", newline="") as file:
                witer = csv.DictWriter(file,fieldnames=OpsCSV.FIELDS)
                witer.writerow(task.model_dump())
        except FileNotFoundError :
            return None

    
    def create_task(self, task : Task)-> dict[str,TaskID]:
        id = self.get_id()
        task_with_id = TaskID(id = str(id), **task.model_dump())
        self.save(task_with_id)
        return {"Created Tasks": task_with_id}
    
    #change this to "Read all → modify → rewrite file" this is a exprement not a real function
    def modify_task(self,id : str, task:dict)->Optional[dict]:
        #This what it will caontain -> task_to_update : TaskID | None = None  this is the modern "task_to_update : Optional[TaskID] = None"
        task_to_update = self.get_task_by_id(id)
        tasks = self.all()
        Update = False
        
        with open(OpsCSV.DATABASE_NAME, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=OpsCSV.FIELDS)
            writer.writeheader()

            for tsk in tasks:
                if tsk.id == id:
                    for field , value in task.items():
                        if value != None:
                            setattr(tsk,field,value)
                    Update = True
                writer.writerow(tsk.model_dump())
                    
        if Update:
            return {'Updated':task_to_update, "Change" : task}
        else:
            return None
        
    def remove_task(self,id: str) -> Optional[Task]:
        tasks = self.all()
        Deleted = False
        tsk_deleted = None

        with open(OpsCSV.DATABASE_NAME, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=OpsCSV.FIELDS)
            writer.writeheader()

            for task in tasks:
                if task.id == id:
                    Deleted = True
                    tsk_deleted = task
                    continue
                writer.writerow(task.model_dump())
        
        if Deleted:
            # Return Task without the ID
            task_dict = tsk_deleted.model_dump()
            del task_dict["id"]
            return Task(**task_dict)
        
        return None
