from pydantic import BaseModel, ConfigDict
from typing import Optional

class ReferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: Optional[str] = None
    description: Optional[str] = None

class ReferenceCreateRequest(BaseModel):
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
