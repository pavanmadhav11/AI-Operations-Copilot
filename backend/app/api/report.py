import os

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.services.report_service import (
    generate_dashboard_report,
    generate_chat_report,
    generate_document_report,
    generate_sql_report,
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


def report_file(path, filename):
    return FileResponse(
        path,
        filename=filename,
        background=BackgroundTask(os.remove, path),
    )


def report_user_id(current_user):
    return None if current_user.role == "admin" else current_user.id


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    file = generate_dashboard_report(db, report_user_id(current_user))
    return report_file(file, "dashboard_report.pdf")


@router.get("/chat")
def chat(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    file = generate_chat_report(db, report_user_id(current_user))
    return report_file(file, "chat_report.pdf")


@router.get("/documents")
def documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    file = generate_document_report(db, report_user_id(current_user))
    return report_file(file, "documents_report.pdf")


@router.get("/sql")
def sql(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    file = generate_sql_report(db, report_user_id(current_user))
    return report_file(file, "sql_report.pdf")
