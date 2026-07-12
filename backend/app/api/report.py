from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
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


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    file = generate_dashboard_report(db)

    return FileResponse(
        file,
        filename="dashboard_report.pdf",
    )


@router.get("/chat")
def chat(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    file = generate_chat_report(db)

    return FileResponse(
        file,
        filename="chat_report.pdf",
    )


@router.get("/documents")
def documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    file = generate_document_report(db)

    return FileResponse(
        file,
        filename="documents_report.pdf",
    )


@router.get("/sql")
def sql(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    file = generate_sql_report(db)

    return FileResponse(
        file,
        filename="sql_report.pdf",
    )