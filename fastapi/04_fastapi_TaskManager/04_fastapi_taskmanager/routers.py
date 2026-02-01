from fastapi import APIRouter, HTTPException,Path,Body,Query
from opr_csv import OpsCSV
from schemas import Task,TaskID,Status,InsertTask,TaskV2WithID
from typing import Optional
from pydantic import BaseModel


router = APIRouter(
    prefix="/Tasks",
)


opr = OpsCSV()



class TaskFilter(BaseModel):
    status: Optional[str] = None
    title: Optional[str] = None

@router.get('/',response_model=list[TaskID])
async def get_all(
    filter: TaskFilter = Query(default=TaskFilter())

):
    tasks = opr.all()
    if filter.status:
        return [tsk for tsk in tasks if tsk.status == filter.status]
    if filter.title:
        return [tsk for tsk in tasks if tsk.title == filter.title]
    return tasks

@router.get('/sreach',response_model=list[TaskID])
async def sreach(
    keyword : str = Query(...)
    ):

    return [
        task
        for task in opr.all()
        if keyword in (task.status + task.description + task.title)
    ]

@router.get(
    "/v2/tasks",
    response_model=list[TaskV2WithID]
)
def get_tasks_v2():
    tasks = opr.read_all_tasks_v2()
    return tasks

@router.get('/{id_task}')
async def get_by_ID(id_task:int = Path(...))-> Optional[TaskID]:
    task = opr.get_task_by_id(str(id_task))
    if not task:
        raise HTTPException(
            status_code=404, detail="task not found"
        )
    return task

@router.post('/',response_model=dict[str,TaskID])
async def create_task(task : Task = Body(...)):
    if isinstance(task.status,Status):
        return opr.create_task(task)
    else:
        raise HTTPException(
            status_code=400, detail="Invalid status"
        )

@router.put('/{id_task}')
async def update_task(id_task : int = Path(...),
                      task : InsertTask = Body(...)):
    return opr.modify_task(str(id_task),task.model_dump())

@router.delete('/{id_task}')
async def delete(id_task : int = Path(...)):
    task = opr.remove_task(str(id_task))

    if not task:
        raise HTTPException(
            status_code=400, detail="task not found"
        )
    return task
    
    #return opr.remove_task(str(id_task))