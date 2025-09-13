# src/dto/document.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.dto.category import CategoryResponse
from src.dto.reference import ReferenceResponse


class DocumentCreateRequest(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None
    reference_id: Optional[int] = None


class DocumentUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    reference_id: Optional[int] = None


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    category_id: Optional[int] = None
    reference_id: Optional[int] = None


class DocumentIncludedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    category: Optional[CategoryResponse] = None
    reference: Optional[ReferenceResponse] = None
