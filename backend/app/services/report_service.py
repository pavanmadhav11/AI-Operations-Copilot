import os
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.chat import ChatMessage
from app.models.chat_session import ChatSession
from app.models.uploaded_file import UploadedFile

REPORT_DIR = "reports"

os.makedirs(REPORT_DIR, exist_ok=True)

styles = getSampleStyleSheet()


def _build_pdf(filename, title, lines):
    doc = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(title, styles["Title"])
    )

    story.append(
        Paragraph("<br/><br/>", styles["Normal"])
    )

    for line in lines:
        story.append(
            Paragraph(str(line), styles["BodyText"])
        )

    doc.build(story)

    return filename


def generate_dashboard_report(db: Session):

    filename = os.path.join(
        REPORT_DIR,
        "dashboard_report.pdf",
    )

    total_users = db.query(User).count()

    total_sessions = db.query(ChatSession).count()

    total_messages = db.query(ChatMessage).count()

    total_documents = db.query(UploadedFile).count()

    pdf_files = (
        db.query(UploadedFile)
        .filter(
            UploadedFile.file_type.contains("pdf")
        )
        .count()
    )

    excel_files = (
        db.query(UploadedFile)
        .filter(
            UploadedFile.file_type.contains("sheet")
        )
        .count()
    )

    lines = [

        "AI Operations Copilot",

        "<br/>",

        "SYSTEM OVERVIEW",

        "<br/>",

        f"Total Users : {total_users}",

        f"Chat Sessions : {total_sessions}",

        f"Total Messages : {total_messages}",

        "<br/>",

        f"Total Documents : {total_documents}",

        f"PDF Files : {pdf_files}",

        f"Excel Files : {excel_files}",

        "<br/>",

        f"Generated On : {datetime.now().strftime('%d %b %Y %I:%M %p')}",

    ]

    return _build_pdf(
        filename,
        "Dashboard Report",
        lines,
    )


def generate_chat_report(db: Session):

    filename = os.path.join(
        REPORT_DIR,
        "chat_report.pdf",
    )

    messages = (
        db.query(ChatMessage)
        .order_by(ChatMessage.created_at.desc())
        .limit(100)
        .all()
    )

    lines = []

    for msg in messages:

        lines.append("<br/>")

        lines.append(
            f"<b>{msg.role.upper()}</b>"
        )

        lines.append(
            msg.message
        )

        lines.append(
            "---------------------------------------------"
        )

    lines.append("<br/>")

    lines.append(
        f"Generated On : {datetime.now().strftime('%d %b %Y %I:%M %p')}"
    )

    return _build_pdf(
        filename,
        "Chat History Report",
        lines,
    )


def generate_document_report(db: Session):

    filename = os.path.join(
        REPORT_DIR,
        "documents_report.pdf",
    )

    documents = (
        db.query(UploadedFile)
        .order_by(
            UploadedFile.uploaded_at.desc()
        )
        .all()
    )

    lines = []

    for doc in documents:

        lines.append("<br/>")

        lines.append(
            f"<b>File :</b> {doc.filename}"
        )

        lines.append(
            f"<b>Type :</b> {doc.file_type}"
        )

        if doc.summary:

            lines.append(
                f"<b>Summary :</b> {doc.summary}"
            )

        lines.append(
            "---------------------------------------------"
        )

    lines.append("<br/>")

    lines.append(
        f"Generated On : {datetime.now().strftime('%d %b %Y %I:%M %p')}"
    )

    return _build_pdf(
        filename,
        "Documents Report",
        lines,
    )


def generate_sql_report(db: Session):

    filename = os.path.join(
        REPORT_DIR,
        "sql_report.pdf",
    )

    prompts = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.role == "user"
        )
        .all()
    )

    lines = []

    for prompt in prompts:

        lines.append("<br/>")

        lines.append(
            prompt.message
        )

        lines.append(
            "---------------------------------------------"
        )

    lines.append("<br/>")

    lines.append(
        f"Generated On : {datetime.now().strftime('%d %b %Y %I:%M %p')}"
    )

    return _build_pdf(
        filename,
        "SQL Prompt History Report",
        lines,
    )