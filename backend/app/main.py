from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload import router as upload_router
from app.api.chat_session import router as chat_session_router
from app.core.config import settings
from app.db.init_db import init_db
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.sql import router as sql_router
from app.api.dashboard import router as dashboard_router
from app.api.report import router as report_router
from app.api.settings import router as settings_router
from app.api.pdf import router as pdf_router
from app.api.excel import router as excel_router
from app.api.analytics import router as analytics_router
from app.api.inventory import router as inventory_router
from app.api.procurement import router as procurement_router
from app.api.recommendations import router as recommendations_router
from app.api.notifications import router as notifications_router
from app.utils.file_upload import MAX_UPLOAD_BYTES
from app.utils.upload_request_limit import UploadRequestLimitMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)


app.add_middleware(
    UploadRequestLimitMiddleware,
    max_bytes=MAX_UPLOAD_BYTES + 1024 * 1024,
    upload_paths={"/upload", "/pdf/upload", "/excel/upload"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ai-operations-copilot-weld.vercel.app",
        "https://ai-operations-copilot-e241ky21w.vercel.app",
    ] + [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()
    if settings.SEED_PRESENTATION_DATA:
        from app.seed_business_data import main as seed_business_data

        seed_business_data(["--confirm-business-data"])



app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(chat_session_router)
app.include_router(upload_router)
app.include_router(sql_router)
app.include_router(dashboard_router)
app.include_router(report_router)
app.include_router(settings_router)
app.include_router(pdf_router)
app.include_router(excel_router)
app.include_router(analytics_router)
app.include_router(inventory_router)
app.include_router(procurement_router)
app.include_router(recommendations_router)
app.include_router(notifications_router)

@app.get("/")
def root():
    return {
        "message": "Backend Running 🚀",
        "app": settings.APP_NAME,
    }
