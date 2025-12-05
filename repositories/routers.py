from fastapi import FastAPI, Depends, APIRouter
from schemas.task import TaskSchema
from models.task import TaskModel, TaskAddModel
from fastapi import FastAPI, Depends
from database.db import engine, get_session, Base
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.post("/tasks/", response_model=list[TaskModel], tags=['Tasks'])
async def add_task(task_data: TaskAddModel, session: AsyncSession = Depends(get_session)):
    new_task = TaskSchema(title=task_data.title, description=task_data.description)
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task

@router.get("/tasks/", response_model=list[TaskModel], tags=['Tasks'])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    query = select(TaskSchema)
    result = await session.execute(query)
    tasks = result.scalars().all()
    return tasks