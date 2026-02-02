from pydantic import BaseModel

class CardBase(BaseModel):
    title: str
    description: str | None = None

class CardCreate(CardBase):
    pass

class CardRead(CardBase):
    id: int
    position: int
    list_id: int

class CardMove(BaseModel):
    to_list_id: int