import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.main.domain.auth.controllers import router as auth_router
from app.main.domain.speech_to_text.controllers import router as speech_to_text_router
from app.main.domain.users.controllers import router as user_router
from app.main.domain.writing_to_speech.controllers import (
    router as writing_to_text_router,
)
from app.main.domain.writings.controllers import router as writing_router
from app.main.infrastructure import models
from app.main.infrastructure.database.base import engine
from app.main.middlware.log_middleware import LogMiddleware

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(LogMiddleware)
origins = [
    # os.getenv("FRONTEND_URL"),
    "https://speechify-scripts.vercel.app/",
    "https://speechify-scripts.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(writing_router)
app.include_router(writing_to_text_router)
app.include_router(speech_to_text_router)
app.include_router(user_router)
app.include_router(auth_router)
