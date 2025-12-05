from sqlalchemy import Integer, String, DateTime
from database.db import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

class TaskSchema(Base):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
