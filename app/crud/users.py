from app.models.user import User
from app.schemas.user import UserCreate
from app.database import engine
from app.utils.password import generate_password_hash
from sqlmodel import Session, select

def user_exists(username: str) -> bool:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
        return bool(user)

def create_user(credentials: UserCreate) -> User:
    username = credentials.username
    password = credentials.password
    hashed_password = generate_password_hash(password)
    with Session(engine) as session:
        user = User(username=username, hashed_password=hashed_password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_user_by_username(username: str) -> User | None:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user: User | None = session.exec(statement).one_or_none()
        return user

def get_user_by_id(user_id: int) -> User | None:
    with Session(engine) as session:
        user = session.get(User, user_id)
        return user