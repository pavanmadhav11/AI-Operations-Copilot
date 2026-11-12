import os
import json
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.models.uploaded_file import UploadedFile

from app.services.pdf_service import extract_pdf_text, extract_pdf_pages
from app.ai.pdf_summary import generate_pdf_summary
from app.utils.file_upload import remove_upload, save_upload

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_pdf(
    db: Session,
    user_id: int,
    file: UploadFile,
):

    filepath, original_name = save_upload(file, UPLOAD_DIR, {".pdf"})
    try:
        extracted = extract_pdf_text(filepath)
        if not extracted.strip():
            raise HTTPException(status_code=400, detail="Unable to extract text from this PDF.")
        summary = generate_pdf_summary(extracted)
        pdf = UploadedFile(
            user_id=user_id,
            session_id=None,
            filename=original_name,
            file_type="application/pdf",
            file_path=filepath,
            extracted_text=extracted,
            summary=summary,
            source_chunks=json.dumps(extract_pdf_pages(filepath)),
        )
        db.add(pdf)
        db.commit()
        db.refresh(pdf)
        return pdf
    except HTTPException:
        db.rollback()
        remove_upload(filepath, UPLOAD_DIR)
        raise
    except Exception as error:
        db.rollback()
        remove_upload(filepath, UPLOAD_DIR)
        raise HTTPException(status_code=400, detail="Could not process this PDF.") from error


def get_pdfs(
    db: Session,
    user_id: int,
):

    return (
        db.query(UploadedFile)
        .filter(
            UploadedFile.user_id == user_id,
            UploadedFile.session_id == None,
            UploadedFile.file_type == "application/pdf",
        )
        .order_by(
            UploadedFile.id.desc()
        )
        .all()
    )
def delete_pdf(
    db: Session,
    user_id: int,
    file_id: int,
):
    pdf = (
        db.query(UploadedFile)
        .filter(
            UploadedFile.id == file_id,
            UploadedFile.user_id == user_id,
            UploadedFile.session_id == None,
        )
        .first()
    )

    if not pdf:
        return False

    remove_upload(pdf.file_path, UPLOAD_DIR)

    db.delete(pdf)

    db.commit()

    return True
