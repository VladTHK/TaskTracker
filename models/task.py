from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskAddModel(BaseModel): 
    title: str
    description: str

class TaskModel(TaskAddModel): 
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 
