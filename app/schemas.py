from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskSchema(BaseModel): 
    id: int
    title: str
    description: str
    created_at: datetime
    
class TaskAddSchema(BaseModel):  
    title: str
    description: str
