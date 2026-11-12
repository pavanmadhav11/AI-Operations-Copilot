import json
import os

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.ai.pdf_summary import generate_pdf_summary
from app.models.chat_session import ChatSession
from app.models.uploaded_file import UploadedFile
from app.services.excel_service import extract_excel_text
from app.services.pdf_service import extract_pdf_pages, extract_pdf_text
from app.utils.file_upload import remove_upload, save_upload

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_file(db: Session, user_id: int, session_id: int, file: UploadFile):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id,
    ).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Chat session not found.")

    filepath, filename = save_upload(file, UPLOAD_DIR, {".pdf", ".xlsx", ".xls"})

    try:
        extracted_text = ""
        summary = None
        workbook_json = None
        source_chunks = []
        lower_name = filename.lower()

        if lower_name.endswith(".pdf"):
            extracted_text = extract_pdf_text(filepath)
            source_chunks = extract_pdf_pages(filepath)
            if extracted_text.strip():
                summary = generate_pdf_summary(extracted_text)
        elif lower_name.endswith((".xlsx", ".xls")):
            extracted_text, workbook_json = extract_excel_text(filepath)
            source_chunks = json.loads(workbook_json).get("source_chunks", [])

        if not extracted_text or not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the uploaded document.")

        uploaded = UploadedFile(
            user_id=user_id,
            session_id=session_id,
            filename=os.path.basename(filename),
            file_type=(
                "application/pdf" if lower_name.endswith(".pdf")
                else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if lower_name.endswith(".xlsx")
                else "application/vnd.ms-excel"
            ),
            file_path=filepath,
            extracted_text=extracted_text,
            summary=summary,
            workbook_json=workbook_json,
            source_chunks=json.dumps(source_chunks, default=str),
        )
        db.add(uploaded)
        db.commit()
        db.refresh(uploaded)
        return uploaded
    except HTTPException:
        db.rollback()
        remove_upload(filepath, UPLOAD_DIR)
        raise
    except Exception as error:
        db.rollback()
        remove_upload(filepath, UPLOAD_DIR)
        raise HTTPException(status_code=400, detail="Could not process this document.") from error


def get_uploaded_files(db: Session, session_id: int, user_id: int):
    return (
        db.query(UploadedFile)
        .filter(
            UploadedFile.session_id == session_id,
            UploadedFile.user_id == user_id,
        )
        .order_by(UploadedFile.id.desc())
        .all()
    )


def delete_uploaded_file(db: Session, user_id: int, file_id: int):
    uploaded = db.query(UploadedFile).filter(
        UploadedFile.id == file_id,
        UploadedFile.user_id == user_id,
    ).first()
    if not uploaded:
        return False
    remove_upload(uploaded.file_path, UPLOAD_DIR)
    db.delete(uploaded)
    db.commit()
    return True


def get_session_files(db: Session, session_id: int, user_id: int):
    return (
        db.query(UploadedFile)
        .filter(
            UploadedFile.session_id == session_id,
            UploadedFile.user_id == user_id,
        )
        .all()
    )
