from sqlmodel import Session, select, update
from app.database import engine
from app.models.board import Board
from app.schemas.list import ListCreate, ListChangePosition
from app.models.user import User
from app.models.list import List
from app.crud.boards import get_board
from app.exceptions import BoardNotFoundError, ListNotFoundError, ListInvalidNewPositionError


def create_list(board_id: int, payload: ListCreate, user: User) -> List:
    board = get_board(board_id, user)
    if board is None:
        raise BoardNotFoundError("Board not found")
    with Session(engine) as session:
        lists_in_board = session.exec(select(List).where(List.board_id == board_id)).all()
        list = List(
            title=payload.title,
            board_id=board_id,
            position=len(lists_in_board),
        )
        session.add(list)
        session.commit()
        session.refresh(list)
        return list

def get_lists(board_id: int, user: User):
    board = get_board(board_id, user)
    if board is None:
        raise BoardNotFoundError("Board not found")
    with Session(engine) as session:
        lists = session.exec(select(List).where(List.board_id == board_id)).all()
        return lists

def get_list(list_id: int, user: User) -> List | None:
    with Session(engine) as session:
        list = session.exec(
            select(List)
            .join(Board)
            .where(List.id == list_id)
            .where(Board.owner_id == user.id)
        ).one_or_none()
        return list

def change_list_position(list_id: int, payload: ListChangePosition, user: User) -> List:
    list = get_list(list_id, user)
    if list is None:
        raise ListNotFoundError("List not found")
    new_position = payload.new_position
    with Session(engine) as session:
        other_list = session.exec(
            select(List)
            .join(Board)
            .where(Board.id == list.board_id)
            .where(List.position == new_position)
        ).one_or_none()
        if other_list is None:
            raise ListInvalidNewPositionError("Invalid new position")
        if list == other_list:
            return list
        other_list.position = list.position
        list.position = new_position
        session.add(list)
        session.add(other_list)
        session.commit()
        session.refresh(list)
        return list

def delete_list(list_id: int, user: User) -> bool:
    list = get_list(list_id, user)
    if list is None:
        return False
    with Session(engine) as session:
        session.delete(list)
        session.exec(
            update(List)
            .where(List.board_id == list.board_id)
            .where(List.position > list.position)
            .values(position=List.position - 1)
        )
        session.commit()
        return True