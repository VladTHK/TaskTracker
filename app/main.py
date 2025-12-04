from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, get_session, Base
from models import TaskModel
from schemas import TaskSchema, TaskAddSchema

app = FastAPI(title="Task Tracker")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/tasks", response_model=TaskSchema)
async def add_task(data: TaskAddSchema, session: AsyncSession = Depends(get_session)):
    new_task = TaskModel(title=data.title, description=data.description)
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task

@app.get("/tasks", response_model=list[TaskSchema])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    query = select(TaskModel)
    result = await session.execute(query)
    return result.scalars().all()
