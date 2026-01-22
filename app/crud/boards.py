from app.models.board import Board
from app.models.user import User
from app.schemas.board import BoardCreate
from app.database import engine
from datetime import datetime, timezone
from sqlmodel import Session, select

def create_board(payload: BoardCreate, user: User) -> Board:
    board = Board(
        title=payload.title,
        owner_id=user.id,
        created_at=datetime.now(timezone.utc),
    )
    with Session(engine) as session:
        session.add(board)
        session.commit()
        session.refresh(board)
        return board

def get_board(board_id: int, user: User) -> Board | None:
    with Session(engine) as session:
        board = session.exec(select(Board).where(
            Board.id == board_id,
            Board.owner_id == user.id
        )).one_or_none()
        return board

def get_boards(user: User):
    with Session(engine) as session:
        boards = session.exec(select(Board).where(Board.owner_id == user.id)).all()
        return boards

def delete_board(board_id: int, user: User) -> bool:
    with Session(engine) as session:
        board = session.exec(select(Board).where(
            Board.id == board_id,
            Board.owner_id == user.id
        )).one_or_none()
        if board:
            session.delete(board)
            session.commit()
            return True
        return False