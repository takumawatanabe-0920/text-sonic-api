from fastapi.middleware.cors import CORSMiddleware
from app.main.writings.controllers import router as writing_router
from fastapi import FastAPI
from .middlware.log_middleware import LogMiddleware
from app.main.infrastructure.prisma_service import prisma

app = FastAPI()
app.add_middleware(LogMiddleware)
origins = [
    "http://localhost:3016",
    "https://text-sonic.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(writing_router)


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()
