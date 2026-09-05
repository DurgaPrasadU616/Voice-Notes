from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base
from pydantic import BaseModel
from typing import List, Optional, Literal

# --- SQLAlchemy Models ---

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)
    deadline = Column(String, nullable=True)
    priority = Column(String)
    category = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# --- Pydantic Models ---

class ExtractActionsRequest(BaseModel):
    text: str

class ActionItem(BaseModel):
    task: str
    deadline: Optional[str] = None
    priority: Literal["High", "Medium", "Low"]
    category: Optional[str] = None

class ExtractActionsResponse(BaseModel):
    summary: str
    action_items: List[ActionItem]

class TaskCreate(BaseModel):
    task: str
    deadline: Optional[str] = None
    priority: Literal["High", "Medium", "Low"]
    category: Optional[str] = None

class TaskUpdate(BaseModel):
    task: Optional[str] = None
    deadline: Optional[str] = None
    priority: Optional[Literal["High", "Medium", "Low"]] = None
    category: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    task: str
    deadline: Optional[str] = None
    priority: str
    category: Optional[str] = None
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
