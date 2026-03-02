from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, String, Text, DateTime, Float
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from app.database import Base


# -------------------
# Pydantic model
# -------------------

class EntryCreate(BaseModel):
    type: str
    title: str
    language: str
    project: str
    tags: List[str]
    context: str
    content: str
    id: str


# -------------------
# SQLAlchemy model
# -------------------

class Entry(Base):
    __tablename__ = "entries"

    entry_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    type = Column(String)
    title = Column(String)
    language = Column(String)
    project = Column(String)

    tags = Column(ARRAY(String))
    context = Column(Text)
    content = Column(Text)

    embedding = Column(ARRAY(Float))