from pydantic import BaseModel
from typing import List

class EntryCreate(BaseModel):
    type: str
    title: str
    language: str
    project: str
    tags: List[str]
    context: str
    content: str
    id: str
    createdAt: str