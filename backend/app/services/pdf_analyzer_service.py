import os
import shutil
import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.models.uploaded_file import UploadedFile

from app.services.pdf_service import extract_pdf_text
from app.ai.pdf_summary import generate_pdf_summary

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_pdf(
    db: Session,
    user_id: int,
    file: UploadFile,
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    filepath = os.path.join(
        UPLOAD_DIR,
        unique_filename,
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    extracted = extract_pdf_text(filepath)

    if len(extracted.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Unable to extract text.",
        )

    summary = generate_pdf_summary(
        extracted,
    )

    pdf = UploadedFile(
        user_id=user_id,
        session_id=None,
        filename=file.filename,
        file_type=file.content_type,
        file_path=filepath,
        extracted_text=extracted,
        summary=summary,
    )

    db.add(pdf)

    db.commit()

    db.refresh(pdf)

    return pdf


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

    if os.path.exists(pdf.file_path):
        os.remove(pdf.file_path)

    db.delete(pdf)

    db.commit()

    return True