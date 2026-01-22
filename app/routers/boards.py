from fastapi import APIRouter, Depends, status, HTTPException, Response

from app.models.user import User
from app.schemas.board import BoardCreate, BoardRead
from app.utils.jwt import get_current_user
from app.crud.boards import create_board as create_board_from_crud
from app.crud.boards import get_boards as get_boards_from_crud
from app.crud.boards import get_board as get_board_from_crud
from app.crud.boards import delete_board as delete_board_from_crud
from typing import Annotated

boards_router = APIRouter(
    prefix="/boards",
    tags=["boards"],
)

@boards_router.post("/", response_model=BoardRead, status_code=status.HTTP_201_CREATED)
def create_board(payload: BoardCreate, user: Annotated[User, Depends(get_current_user)]):
    board = create_board_from_crud(payload, user)
    return board

@boards_router.get("/", response_model=list[BoardRead])
def get_boards(user: Annotated[User, Depends(get_current_user)]):
    boards = get_boards_from_crud(user)
    return boards

@boards_router.get("/{board_id}", response_model=BoardRead)
def get_board(board_id: int, user: Annotated[User, Depends(get_current_user)]):
    board = get_board_from_crud(board_id, user)
    if board is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    return board

@boards_router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(board_id: int, user: Annotated[User, Depends(get_current_user)]):
    board_deleted = delete_board_from_crud(board_id, user)
    if board_deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")