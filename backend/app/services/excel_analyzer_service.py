import os
import json
import pandas as pd

from fastapi import UploadFile, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.product import Product
from app.models.uploaded_file import UploadedFile

from app.services.excel_service import extract_excel_text
from app.ai.excel_summary import generate_excel_summary
from app.utils.file_upload import remove_upload, save_upload

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_excel(
    db: Session,
    user_id: int,
    file: UploadFile,
):
    filepath, original_name = save_upload(file, UPLOAD_DIR, {".xlsx", ".xls"})
    try:
        extracted_text, workbook_json = extract_excel_text(filepath)
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Unable to extract data from this workbook.")
        summary = generate_excel_summary(extracted_text)
        extension = os.path.splitext(original_name)[1].lower()
        file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if extension == ".xlsx" else "application/vnd.ms-excel"
        excel = UploadedFile(
            user_id=user_id,
            session_id=None,
            filename=original_name,
            file_type=file_type,
            file_path=filepath,
            extracted_text=extracted_text,
            summary=summary,
            workbook_json=workbook_json,
            source_chunks=json.dumps(json.loads(workbook_json).get("source_chunks", [])),
        )
        db.add(excel)
        db.commit()
        db.refresh(excel)
        return excel
    except HTTPException:
        db.rollback()
        remove_upload(filepath, UPLOAD_DIR)
        raise
    except Exception as error:
        db.rollback()
        remove_upload(filepath, UPLOAD_DIR)
        raise HTTPException(status_code=400, detail="Could not process this Excel workbook.") from error


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

    remove_upload(excel.file_path, UPLOAD_DIR)

    db.delete(excel)

    db.commit()

    return True


def apply_sales_demand(db: Session, user_id: int, file_id: int):
    uploaded = db.query(UploadedFile).filter(
        UploadedFile.id == file_id,
        UploadedFile.user_id == user_id,
        UploadedFile.session_id.is_(None),
    ).first()
    if uploaded is None or not uploaded.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=404, detail="Your uploaded sales workbook was not found.")

    excel = pd.ExcelFile(uploaded.file_path)
    sales_frames = []
    for sheet in excel.sheet_names:
        frame = pd.read_excel(uploaded.file_path, sheet_name=sheet)
        frame.columns = [str(column).strip().lower().replace(" ", "_") for column in frame.columns]
        product_col = next((name for name in ("product_name", "product", "item", "sku") if name in frame.columns), None)
        quantity_col = next((name for name in ("units_sold", "quantity", "qty", "sold") if name in frame.columns), None)
        date_col = next((name for name in ("date", "sale_date", "order_date") if name in frame.columns), None)
        if product_col and quantity_col and date_col:
            sales_frames.append(frame[[product_col, quantity_col, date_col]].rename(columns={
                product_col: "product_name",
                quantity_col: "quantity",
                date_col: "date",
            }))

    if not sales_frames:
        raise HTTPException(status_code=400, detail="Sales data needs product_name, quantity, and date columns.")

    sales = pd.concat(sales_frames, ignore_index=True)
    sales["product_name"] = sales["product_name"].fillna("").astype(str).str.strip()
    sales["quantity"] = pd.to_numeric(sales["quantity"], errors="coerce")
    sales["date"] = pd.to_datetime(sales["date"], errors="coerce").dt.date
    if sales["product_name"].eq("").any() or sales["quantity"].isna().any() or sales["date"].isna().any() or (sales["quantity"] < 0).any():
        raise HTTPException(status_code=400, detail="Sales data contains invalid dates or negative/non-numeric quantities.")

    results = []
    unmatched = []
    for product_name, rows in sales.groupby("product_name"):
        product = db.query(Product).filter(func.lower(Product.name) == product_name.lower()).first()
        if product is None:
            unmatched.append(product_name)
            continue
        day_count = max(1, (rows["date"].max() - rows["date"].min()).days + 1)
        average = round(float(rows["quantity"].sum()) / day_count, 2)
        db.query(Inventory).filter(Inventory.product_id == product.id).update(
            {Inventory.average_daily_demand: average},
            synchronize_session=False,
        )
        results.append({
            "product_name": product.name,
            "total_units_sold": float(rows["quantity"].sum()),
            "days_in_period": day_count,
            "average_daily_demand": average,
        })

    db.commit()
    return {"updated": results, "unmatched_products": unmatched}
