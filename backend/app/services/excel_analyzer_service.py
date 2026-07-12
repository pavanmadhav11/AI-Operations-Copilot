import os
import shutil
import uuid

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.models.uploaded_file import UploadedFile

from app.services.excel_service import extract_excel_text
from app.ai.excel_summary import generate_excel_summary

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_excel(
    db: Session,
    user_id: int,
    file: UploadFile,
):
    if not (
        file.filename.lower().endswith(".xlsx")
        or file.filename.lower().endswith(".xls")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only Excel files are allowed.",
        )

    unique_filename = (
        f"{uuid.uuid4()}_{file.filename}"
    )

    filepath = os.path.join(
        UPLOAD_DIR,
        unique_filename,
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    extracted_text, workbook_json = extract_excel_text(
        filepath
    )

    if len(extracted_text.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Unable to extract Excel data.",
        )

    summary = generate_excel_summary(
        extracted_text,
    )

    excel = UploadedFile(
        user_id=user_id,
        session_id=None,
        filename=file.filename,
        file_type=file.content_type,
        file_path=filepath,
        extracted_text=extracted_text,
        summary=summary,
        workbook_json=workbook_json,
    )

    db.add(excel)

    db.commit()

    db.refresh(excel)

    return excel


def get_excels(
    db: Session,
    user_id: int,
):
    return (
        db.query(UploadedFile)
        .filter(
            UploadedFile.user_id == user_id,
            UploadedFile.session_id == None,
        )
        .filter(
            UploadedFile.file_type.in_(
                [
                    "application/vnd.ms-excel",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ]
            )
        )
        .order_by(
            UploadedFile.id.desc()
        )
        .all()
    )


def delete_excel(
    db: Session,
    user_id: int,
    file_id: int,
):
    excel = (
        db.query(UploadedFile)
        .filter(
            UploadedFile.id == file_id,
            UploadedFile.user_id == user_id,
            UploadedFile.session_id == None,
        )
        .first()
    )

    if not excel:
        return False

    if os.path.exists(excel.file_path):
        os.remove(excel.file_path)

    db.delete(excel)

    db.commit()

    return True