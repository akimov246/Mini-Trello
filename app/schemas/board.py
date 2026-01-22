from pydantic import BaseModel
from datetime import datetime

class BorderBase(BaseModel):
    title: str

class BoardCreate(BorderBase):
    pass

class BoardRead(BorderBase):
    id: int
    owner_id: int
    created_at: datetime