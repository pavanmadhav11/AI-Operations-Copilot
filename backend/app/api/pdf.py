from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.schemas.upload import UploadedFileResponse

from app.services.pdf_analyzer_service import (
    upload_pdf,
    get_pdfs,
    delete_pdf,
)

router = APIRouter(
    prefix="/pdf",
    tags=["PDF Analyzer"],
)


@router.post(
    "/upload",
    response_model=UploadedFileResponse,
)
def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return upload_pdf(
        db=db,
        user_id=current_user.id,
        file=file,
    )


@router.get(
    "",
    response_model=list[UploadedFileResponse],
)
def list_pdfs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_pdfs(
        db=db,
        user_id=current_user.id,
    )


@router.delete("/{file_id}")
def remove_pdf(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    success = delete_pdf(
        db=db,
        user_id=current_user.id,
        file_id=file_id,
    )

    if success:
        return {
            "message": "PDF deleted successfully."
        }

    return {
        "message": "PDF not found."
    }