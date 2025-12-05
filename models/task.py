from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskAddModel(BaseModel): 
    title: str
    description: str

class TaskModel(BaseModel): 
    id: Optional[int] = None
    title: str
    description: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 
