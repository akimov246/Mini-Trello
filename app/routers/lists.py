from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Annotated
from app.models.user import User
from app.schemas.list import ListCreate, ListRead, ListChangePosition
from app.utils.jwt import get_current_user
from app.crud.lists import create_list as create_list_from_crud
from app.crud.lists import get_lists as get_lists_from_crud
from app.crud.lists import change_list_position as change_list_position_from_crud
from app.crud.lists import delete_list as delete_list_from_crud
from app.exceptions import BoardNotFoundError, ListNotFoundError, ListInvalidNewPositionError

lists_router = APIRouter(tags=["lists"])

@lists_router.post("/boards/{board_id}/lists", response_model=ListRead, status_code=status.HTTP_201_CREATED)
def create_list(
        board_id: int,
        payload: ListCreate,
        user: Annotated[User, Depends(get_current_user)],
):
    try:
        list = create_list_from_crud(board_id, payload, user)
    except BoardNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    return list

@lists_router.get("/boards/{board_id}/lists", response_model=list[ListRead])
def get_lists(board_id: int, user: Annotated[User, Depends(get_current_user)]):
    try:
        lists = get_lists_from_crud(board_id, user)
    except BoardNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    return lists

@lists_router.patch("/lists/{list_id}/position", response_model=ListRead)
def change_list_position(list_id: int, payload: ListChangePosition, user: Annotated[User, Depends(get_current_user)]):
    try:
        list = change_list_position_from_crud(list_id, payload, user)
    except ListNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    except ListInvalidNewPositionError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid position")
    return list

@lists_router.delete("/lists/{list_id}")
def delete_list(list_id: int, user: Annotated[User, Depends(get_current_user)]):
    list_deleted = delete_list_from_crud(list_id, user)
    if list_deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")