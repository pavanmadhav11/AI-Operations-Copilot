from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.schemas.upload import UploadedFileResponse

from app.services.excel_analyzer_service import (
    upload_excel,
    get_excels,
    delete_excel,
)

router = APIRouter(
    prefix="/excel",
    tags=["Excel Analyzer"],
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
    return upload_excel(
        db=db,
        user_id=current_user.id,
        file=file,
    )


@router.get(
    "",
    response_model=list[UploadedFileResponse],
)
def list_excels(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_excels(
        db=db,
        user_id=current_user.id,
    )


@router.delete("/{file_id}")
def remove_excel(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    success = delete_excel(
        db=db,
        user_id=current_user.id,
        file_id=file_id,
    )

    if success:
        return {
            "message": "Excel deleted successfully."
        }

    return {
        "message": "Excel not found."
    }