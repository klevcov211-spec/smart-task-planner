from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    category: Optional[str] = None
    estimated_minutes: Optional[int] = None
    status: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    estimated_minutes: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True