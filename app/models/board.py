from sqlmodel import SQLModel, Field, Column, DateTime
from datetime import datetime

class Board(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int = Field(foreign_key="user.id", ondelete="CASCADE")
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
        )
    )