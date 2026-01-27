from pydantic import BaseModel

class ListBase(BaseModel):
    title: str

class ListCreate(ListBase):
    pass

class ListRead(ListBase):
    id: int
    position: int
    board_id: int

class ListChangePosition(BaseModel):
    new_position: int