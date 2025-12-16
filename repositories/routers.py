from fastapi import Query, Depends, APIRouter, HTTPException
from schemas import Task
from typing import Annotated
from models import TaskCreate, TaskRead 
from database.db import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/tasks/", response_model=list[TaskRead], tags=['Tasks'])
async def add_task(task_data: TaskCreate, session: AsyncSession = Depends(get_session)):
    new_task = Task(title=task_data.title, description=task_data.description)
    session.add(new_task)
    await session.commit()
    return [new_task]

@router.get("/tasks/", response_model=list[TaskRead], tags=['Tasks'])
async def get_tasks(
    page: Annotated[int, Query(ge=1, le=100)] = 1,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
    session: AsyncSession = Depends(get_session),
):
    offset = (page - 1) * limit
    stmt = select(Task).offset(offset).limit(limit)
    result = await session.execute(stmt)
    tasks = result.scalars().all()
    return tasks

@router.delete("/tasks/{task_id}", response_model=TaskRead, tags=['Tasks'])
async def remove_task(task_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Task).filter(Task.id == task_id)
    result = await session.execute(query)
    task = result.scalars().first()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await session.delete(task)
    await session.commit()
    return task