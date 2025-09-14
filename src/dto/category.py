from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.dto.reference import ReferenceResponse


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None


class CategoryCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryIncludeReferencesResponse(CategoryResponse):
    model_config = ConfigDict(from_attributes=True)

    references: list[ReferenceResponse]
