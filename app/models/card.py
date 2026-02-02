from sqlmodel import SQLModel, Field

class Card(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = Field(default=None)
    position: int
    list_id: int = Field(foreign_key='list.id', ondelete='CASCADE')