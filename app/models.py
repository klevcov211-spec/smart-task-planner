from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    category = Column(String, default="другое")
    estimated_minutes = Column(Integer, default=30)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)