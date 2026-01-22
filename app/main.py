import uvicorn

from fastapi import FastAPI
from app.routers.signup import signup_router
from app.routers.login import login_router
from app.routers.profile import profile_router
from app.routers.boards import boards_router
from datetime import datetime, timezone

app = FastAPI()

app.include_router(signup_router)
app.include_router(login_router)
app.include_router(profile_router)
app.include_router(boards_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)