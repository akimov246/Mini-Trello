import uvicorn

from fastapi import FastAPI
from app.routers.signup import signup_router
from app.routers.login import login_router
from app.routers.profile import profile_router
from app.routers.boards import boards_router
from app.routers.lists import lists_router
from app.routers.cards import cards_router
app = FastAPI(
    title="Mini-Trello",
    description="Backend-API, повторяющий базовый функционал Trello",
    redoc_url=None,
)

app.include_router(signup_router)
app.include_router(login_router)
app.include_router(profile_router)
app.include_router(boards_router)
app.include_router(lists_router)
app.include_router(cards_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)