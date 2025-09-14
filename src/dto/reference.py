# src/dto/reference.py
from pydantic import BaseModel, ConfigDict
from typing import Optional


class ReferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None


class ReferenceCreateRequest(BaseModel):
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
