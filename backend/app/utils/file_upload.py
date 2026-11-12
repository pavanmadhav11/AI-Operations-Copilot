import os
import uuid
import zipfile

from fastapi import HTTPException

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_UNPACKED_XLSX_BYTES = 50 * 1024 * 1024
CHUNK_BYTES = 1024 * 1024


def remove_upload(filepath: str, upload_dir: str = "uploads"):
    upload_root = os.path.realpath(upload_dir)
    target_path = os.path.realpath(filepath)
    try:
        if os.path.commonpath([upload_root, target_path]) != upload_root:
            return False
    except ValueError:
        return False
    if os.path.isfile(target_path):
        os.remove(target_path)
    return True


def save_upload(file, upload_dir: str, allowed_extensions: set[str]):
    original_name = (file.filename or "upload").replace("\\", "/").split("/")[-1]
    extension = os.path.splitext(original_name)[1].lower()
    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="This file type is not supported.")

    header = file.file.read(1024)
    file.file.seek(0)
    if extension == ".pdf" and b"%PDF-" not in header:
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF.")
    if extension == ".xlsx" and not header.startswith(b"PK"):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid Excel workbook.")
    if extension == ".xls" and not header.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid Excel workbook.")

    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, f"{uuid.uuid4().hex}{extension}")
    total_bytes = 0
    try:
        with open(filepath, "wb") as buffer:
            while True:
                chunk = file.file.read(CHUNK_BYTES)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if total_bytes > MAX_UPLOAD_BYTES:
                    raise HTTPException(status_code=413, detail="Uploads must be 10 MB or smaller.")
                buffer.write(chunk)

        if extension == ".xlsx":
            with zipfile.ZipFile(filepath) as workbook:
                unpacked_bytes = sum(entry.file_size for entry in workbook.infolist())
            if unpacked_bytes > MAX_UNPACKED_XLSX_BYTES:
                raise HTTPException(status_code=413, detail="The expanded workbook is too large to process.")
        return filepath, original_name[:255]
    except zipfile.BadZipFile as error:
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid Excel workbook.") from error
    except Exception:
        if os.path.exists(filepath):
            os.remove(filepath)
        raise
