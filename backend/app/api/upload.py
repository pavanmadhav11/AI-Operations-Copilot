from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.schemas.upload import UploadedFileResponse

from app.services.upload_service import (
    save_uploaded_file,
    get_uploaded_files,
    delete_uploaded_file,
)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post(
    "",
    response_model=UploadedFileResponse,
)
def upload_file(
    session_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return save_uploaded_file(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
        file=file,
    )


@router.get(
    "",
    response_model=list[UploadedFileResponse],
)
def list_uploaded_files(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_uploaded_files(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )


@router.delete("/{file_id}")
def remove_uploaded_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    success = delete_uploaded_file(
        db=db,
        user_id=current_user.id,
        file_id=file_id,
    )

    if success:
        return {
            "message": "File deleted successfully."
        }

    return {
        "message": "File not found."
    }
