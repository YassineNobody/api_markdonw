from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: Optional[str] = None
    

class CategoryCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    