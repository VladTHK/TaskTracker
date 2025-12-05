from fastapi import FastAPI, Depends, APIRouter, HTTPException
from schemas import TaskSchema 
from models import TaskAddModel, TaskModel 
from database.db import engine, get_session, Base
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/tasks/", response_model=list[TaskModel], tags=['Tasks'])
async def add_task(task_data: TaskAddModel, session: AsyncSession = Depends(get_session)):
    new_task = TaskSchema(title=task_data.title, description=task_data.description)
    session.add(new_task)
    await session.commit()
    return [new_task]

@router.get("/tasks/", response_model=list[TaskModel], tags=['Tasks'])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    query = select(TaskSchema)
    result = await session.execute(query)
    tasks = result.scalars().all()
    return tasks

@router.delete("/tasks/{task_id}", response_model=TaskModel, tags=['Tasks'])
async def remove_task(task_id: int, session: AsyncSession = Depends(get_session)):
    query = select(TaskSchema).filter(TaskSchema.id == task_id)
    result = await session.execute(query)
    task = result.scalars().first()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await session.delete(task)
    await session.commit()
    return task