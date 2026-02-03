from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Annotated
from app.schemas.card import CardCreate, CardRead, CardMove, CardChangePosition, CardUpdate
from app.models.user import User
from app.crud.cards import create_card as create_card_from_crud
from app.crud.cards import move_card as move_card_from_crud
from app.crud.cards import change_card_position as change_card_position_from_crud
from app.crud.cards import update_card as update_card_from_crud
from app.crud.cards import delete_card as delete_card_from_crud
from app.crud.cards import get_cards as get_cards_from_crud
from app.utils.jwt import get_current_user
from app.exceptions import ListNotFoundError, CardNotFoundError, CardInvalidNewPositionError

cards_router = APIRouter(tags=["cards"])

@cards_router.post(
    "/lists/{list_id}/cards",
    response_model=CardRead,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED
)
def create_card(list_id: int, payload: CardCreate, user: Annotated[User, Depends(get_current_user)]):
    try:
        card = create_card_from_crud(list_id, payload, user)
    except ListNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    return card

@cards_router.patch("/cards/{card_id}/move", response_model=CardRead)
def move_card(card_id: int, payload: CardMove, user: Annotated[User, Depends(get_current_user)]):
    try:
        card = move_card_from_crud(card_id, payload, user)
    except CardNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return card

@cards_router.patch("/cards/{card_id}/position", response_model=CardRead)
def change_card_position(card_id: int, payload: CardChangePosition, user: Annotated[User, Depends(get_current_user)]):
    try:
        card = change_card_position_from_crud(card_id, payload, user)
    except CardNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    except CardInvalidNewPositionError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid position")
    return card

@cards_router.patch("/cards/{card_id}/update", response_model=CardRead)
def update_card(card_id: int, payload: CardUpdate, user: Annotated[User, Depends(get_current_user)]):
    try:
        card = update_card_from_crud(card_id, payload, user)
    except CardNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return card

@cards_router.delete("/cards/{card_id}")
def delete_card(card_id: int, user: Annotated[User, Depends(get_current_user)]):
    card_deleted = delete_card_from_crud(card_id, user)
    if card_deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")

@cards_router.get("/cards/{list_id}")
def get_cards(list_id: int, user: Annotated[User, Depends(get_current_user)]):
    try:
        cards = get_cards_from_crud(list_id, user)
    except ListNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    return cards