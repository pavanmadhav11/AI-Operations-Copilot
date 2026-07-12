import os
import shutil

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.uploaded_file import UploadedFile

from app.services.pdf_service import extract_pdf_text
from app.services.excel_service import extract_excel_text

from app.ai.pdf_summary import generate_pdf_summary

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_file(
    db: Session,
    user_id: int,
    session_id: int,
    file: UploadFile,
):
    filepath = os.path.join(
        UPLOAD_DIR,
        file.filename,
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:

        extracted_text = ""
        summary = None
        workbook_json = None

        filename = file.filename.lower()

        if filename.endswith(".pdf"):

            extracted_text = extract_pdf_text(filepath)

            if extracted_text.strip():

                summary = generate_pdf_summary(
                    extracted_text
                )

        elif (
            filename.endswith(".xlsx")
            or filename.endswith(".xls")
        ):

            extracted_text, workbook_json = extract_excel_text(
                filepath
            )

        if extracted_text is None:
            extracted_text = ""

        if len(extracted_text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the uploaded document.",
            )

        uploaded = UploadedFile(
            user_id=user_id,
            session_id=session_id,
            filename=file.filename,
            file_type=file.content_type,
            file_path=filepath,
            extracted_text=extracted_text,
            summary=summary,
            workbook_json=workbook_json,
        )

        db.add(uploaded)

        db.commit()

        db.refresh(uploaded)

        return uploaded

    except Exception as e:

        db.rollback()

        if os.path.exists(filepath):
            os.remove(filepath)

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}",
        )


def get_uploaded_files(
    db: Session,
    session_id: int,
):
    return (
        db.query(UploadedFile)
        .filter(
            UploadedFile.session_id == session_id
        )
        .order_by(
            UploadedFile.id.desc()
        )
        .all()
    )


def delete_uploaded_file(
    db: Session,
    user_id: int,
    file_id: int,
):
    uploaded = (
        db.query(UploadedFile)
        .filter(
            UploadedFile.id == file_id,
            UploadedFile.user_id == user_id,
        )
        .first()
    )

    if not uploaded:
        return False

    if os.path.exists(uploaded.file_path):
        os.remove(uploaded.file_path)

    db.delete(uploaded)

    db.commit()

    return True


def get_session_files(
    db: Session,
    session_id: int,
):
    return (
        db.query(UploadedFile)
        .filter(
            UploadedFile.session_id == session_id,
        )
        .all()
    )