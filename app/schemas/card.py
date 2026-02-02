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

class CardUpdate(CardBase):
    title: str | None = None

class CardMove(BaseModel):
    to_list_id: int

class CardChangePosition(BaseModel):
    new_position: int