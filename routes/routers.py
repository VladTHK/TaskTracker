from fastapi import Query, Depends, APIRouter, HTTPException, status, Path
from schemas import Task
from models import TaskCreate, TaskRead, TaskUpdate
from database.db import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/tasks/", response_model=list[TaskRead], tags=['Tasks'])
async def add_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session)
):
    new_task = Task(title=task_data.title, description=task_data.description)
    session.add(new_task)
    await session.commit()
    return [new_task]

@router.put("/tasks/{task_id}", response_model=TaskRead, tags=['Tasks'])
async def update_task(
    task_update: TaskUpdate,
    task_id: int = Path(ge=1, description="Task ID to update"),
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalars().first()
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )    

    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
        
    await session.commit()
    await session.refresh(task)
    return task
    

@router.get("/tasks/", response_model=list[TaskRead], tags=['Tasks'])
async def get_tasks(
    offset: int = Query(ge=0, le=1000, default=0),
    limit: int = Query(ge=1, le=100, default=10),
    session: AsyncSession = Depends(get_session),
):
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