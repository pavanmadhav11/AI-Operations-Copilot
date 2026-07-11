from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.chat_session import router as chat_session_router
from app.core.config import settings
from app.db.init_db import init_db
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.sql import router as sql_router



app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()



app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(chat_session_router)
app.include_router(upload_router)
app.include_router(sql_router)

@app.get("/")
def root():
    return {
        "message": "Backend Running 🚀",
        "app": settings.APP_NAME,
    }