from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.cores.database import Base, engine
from app.routers import auth, users, thumbnail

app = FastAPI(title="YouTube Thumbnail Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(thumbnail.router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")