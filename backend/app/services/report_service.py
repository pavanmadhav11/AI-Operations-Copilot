import os
import uuid
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from sqlalchemy.orm import Session

from app.models.chat import ChatMessage
from app.models.chat_session import ChatSession
from app.models.uploaded_file import UploadedFile
from app.models.user import User

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)
styles = getSampleStyleSheet()


def _report_path(report_name):
    return os.path.join(REPORT_DIR, f"{uuid.uuid4().hex}_{report_name}")


def _build_pdf(filename, title, lines):
    doc = SimpleDocTemplate(filename)
    story = [Paragraph(title, styles["Title"]), Paragraph("<br/><br/>", styles["Normal"])]
    story.extend(Paragraph(str(line), styles["BodyText"]) for line in lines)
    doc.build(story)
    return filename


def generate_dashboard_report(db: Session, user_id: int | None = None):
    filename = _report_path("dashboard_report.pdf")
    message_query = db.query(ChatMessage).join(ChatSession)
    session_query = db.query(ChatSession)
    document_query = db.query(UploadedFile)
    user_query = db.query(User)
    if user_id is not None:
        message_query = message_query.filter(ChatSession.user_id == user_id)
        session_query = session_query.filter(ChatSession.user_id == user_id)
        document_query = document_query.filter(UploadedFile.user_id == user_id)
        user_query = user_query.filter(User.id == user_id)

    total_users = user_query.count()
    total_sessions = session_query.count()
    total_messages = message_query.count()
    total_documents = document_query.count()
    pdf_files = document_query.filter(UploadedFile.file_type.contains("pdf")).count()
    excel_files = document_query.filter(UploadedFile.file_type.contains("sheet")).count()
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
    return _build_pdf(filename, "Dashboard Report", lines)


def generate_chat_report(db: Session, user_id: int | None = None):
    filename = _report_path("chat_report.pdf")
    query = db.query(ChatMessage).join(ChatSession)
    if user_id is not None:
        query = query.filter(ChatSession.user_id == user_id)
    messages = query.order_by(ChatMessage.created_at.desc()).limit(100).all()
    lines = []
    for message in messages:
        lines.extend([
            "<br/>",
            f"<b>{escape(message.role.upper())}</b>",
            escape(message.message),
            "---------------------------------------------",
        ])
    lines.extend(["<br/>", f"Generated On : {datetime.now().strftime('%d %b %Y %I:%M %p')}"])
    return _build_pdf(filename, "Chat History Report", lines)


def generate_document_report(db: Session, user_id: int | None = None):
    filename = _report_path("documents_report.pdf")
    query = db.query(UploadedFile)
    if user_id is not None:
        query = query.filter(UploadedFile.user_id == user_id)
    documents = query.order_by(UploadedFile.uploaded_at.desc()).all()
    lines = []
    for document in documents:
        lines.extend([
            "<br/>",
            f"<b>File :</b> {escape(document.filename)}",
            f"<b>Type :</b> {escape(document.file_type or '')}",
        ])
        if document.summary:
            lines.append(f"<b>Summary :</b> {escape(document.summary)}")
        lines.append("---------------------------------------------")
    lines.extend(["<br/>", f"Generated On : {datetime.now().strftime('%d %b %Y %I:%M %p')}"])
    return _build_pdf(filename, "Documents Report", lines)


def generate_sql_report(db: Session, user_id: int | None = None):
    filename = _report_path("sql_report.pdf")
    query = db.query(ChatMessage).join(ChatSession).filter(ChatMessage.role == "user")
    if user_id is not None:
        query = query.filter(ChatSession.user_id == user_id)
    prompts = query.all()
    lines = []
    for prompt in prompts:
        lines.extend(["<br/>", escape(prompt.message), "---------------------------------------------"])
    lines.extend(["<br/>", f"Generated On : {datetime.now().strftime('%d %b %Y %I:%M %p')}"])
    return _build_pdf(filename, "SQL Prompt History Report", lines)
