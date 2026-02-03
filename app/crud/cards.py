from sqlmodel import Session, select, func, update
from app.database import engine
from app.schemas.card import CardCreate, CardMove, CardChangePosition, CardUpdate
from app.models.user import User
from app.models.card import Card
from app.models.list import List
from app.models.board import Board
from app.crud.lists import get_list
from app.exceptions import ListNotFoundError, CardNotFoundError, CardInvalidNewPositionError


def create_card(list_id: int, payload: CardCreate, user: User) -> Card:
    list = get_list(list_id, user)
    if list is None:
        raise ListNotFoundError("List not found")
    with Session(engine) as session:
        cards_in_list_len = session.exec(
            select(func.count())
            .select_from(Card)
            .where(Card.list_id == list_id)
        ).one()
        card = Card(
            title=payload.title,
            description=payload.description,
            position=cards_in_list_len,
            list_id=list_id,
        )
        session.add(card)
        session.commit()
        session.refresh(card)
        return card

def move_card(card_id: int, payload: CardMove, user: User) -> Card:
    with Session(engine) as session:
        card: Card | None = session.exec(
            select(Card)
            .join(List)
            .join(Board)
            .where(Card.id == card_id)
            .where(user.id == Board.owner_id)
        ).one_or_none()
        if card is None:
            raise CardNotFoundError("Card not found")
        if card.list_id == payload.to_list_id:
            return card
        cards_in_to_list_len = session.exec(
            select(func.count())
            .select_from(Card)
            .where(Card.list_id == payload.to_list_id)
        ).one()
        session.exec(
            update(Card)
            .where(Card.list_id == card.list_id)
            .where(Card.position > card.position)
            .values(position=Card.position - 1)
        )
        card.position = cards_in_to_list_len
        card.list_id = payload.to_list_id
        session.add(card)
        session.commit()
        session.refresh(card)
        return card

def change_card_position(card_id: int, payload: CardChangePosition, user: User) -> Card:
    with Session(engine) as session:
        card: Card | None = session.exec(
            select(Card)
            .join(List)
            .join(Board)
            .where(Card.id == card_id)
            .where(user.id == Board.owner_id)
        ).one_or_none()
        if card is None:
            raise CardNotFoundError("Card not found")
        other_card = session.exec(
            select(Card)
            .join(List)
            .join(Board)
            .where(Board.owner_id == user.id)
            .where(Card.list_id == card.list_id)
            .where(Card.position == payload.new_position)
        ).one_or_none()
        if other_card is None:
            raise CardInvalidNewPositionError("Invalid new position")
        if card == other_card:
            return card
        other_card.position = card.position
        card.position = payload.new_position
        session.add(card)
        session.add(other_card)
        session.commit()
        session.refresh(card)
        return card

def update_card(card_id: int, payload: CardUpdate, user: User) -> Card:
    with Session(engine) as session:
        card: Card | None = session.exec(
            select(Card)
            .join(List)
            .join(Board)
            .where(Card.id == card_id)
            .where(user.id == Board.owner_id)
        ).one_or_none()
        if card is None:
            raise CardNotFoundError("Card not found")
        update_data = payload.model_dump(exclude_unset=True)
        card.sqlmodel_update(update_data)
        session.commit()
        session.refresh(card)
        return card

def delete_card(card_id: int, user: User) -> bool:
    with Session(engine) as session:
        card: Card | None = session.exec(
            select(Card)
            .join(List)
            .join(Board)
            .where(Card.id == card_id)
            .where(user.id == Board.owner_id)
        ).one_or_none()
        if card is None:
            return False
        session.delete(card)
        session.exec(
            update(Card)
            .where(Card.list_id == card.list_id)
            .where(Card.position > card.position)
            .values(position=Card.position - 1)
        )
        session.commit()
        return True