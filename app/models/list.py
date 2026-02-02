from sqlmodel import SQLModel, Field

class List(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    position: int
    board_id: int = Field(foreign_key="board.id", ondelete="CASCADE")