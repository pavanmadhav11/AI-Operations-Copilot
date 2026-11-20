import argparse
import json
import os
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from sqlalchemy import func, inspect, text

from app.auth.hashing import hash_password
from app.db.init_db import init_db
from app.db.database import SessionLocal
from app.models.chat import ChatMessage
from app.models.chat_session import ChatSession
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.purchase_order import PurchaseOrder
from app.models.recommendation_outcome import RecommendationOutcome
from app.models.sales_record import SalesRecord
from app.models.stock_action import StockAction
from app.models.stock_batch import StockBatch
from app.models.stock_movement import StockMovement
from app.models.supplier import Supplier
from app.models.uploaded_file import UploadedFile
from app.models.user import User
from app.models.warehouse import Warehouse


DATA_DIR = Path("business_data")
PASSWORD_ENV = "PRESENTATION_PASSWORD"
BUSINESS_USERS = {
    "admin": ("ananya.reddy@godavarifresh.example", "Ananya Reddy"),
    "manager": ("abhiram_manager@gmail.com", "Abhiram Manager"),
    "employee": ("jeevan_employee@gmail.com", "Jeevan Employee"),
}
BUSINESS_PASSWORD_ENVS = {
    "manager": "PRESENTATION_MANAGER_PASSWORD",
    "employee": "PRESENTATION_EMPLOYEE_PASSWORD",
}
WAREHOUSE_ROWS = [
    ("Visakhapatnam Central Store", "Visakhapatnam"),
    ("Vijayawada Wholesale Store", "Vijayawada"),
    ("Rajamahendravaram Distribution Store", "Rajamahendravaram"),
    ("Tirupati Retail Store", "Tirupati"),
]
PRODUCT_ROWS = [
    ("Araku Valley Arabica Coffee", "Coffee and Tea", 680.0),
    ("Andhra Filter Coffee Powder", "Coffee and Tea", 420.0),
    ("Guntur Sannam Chilli Powder", "Spices", 185.0),
    ("Godavari Palm Jaggery", "Sweeteners", 145.0),
    ("Tirupati Cow Ghee", "Dairy", 590.0),
    ("Vijayawada Paper Cups", "Packaging", 1.8),
    ("Ongole Toned Milk", "Dairy", 34.0),
    ("Kakinada Coconut Milk", "Dairy Alternative", 110.0),
    ("Anantapur Groundnut Oil", "Cooking Oil", 210.0),
    ("Nellore Sona Masoori Rice", "Grains", 72.0),
    ("Chittoor Mango Pulp", "Fruit Products", 155.0),
    ("Vizianagaram Cashews", "Dry Fruits", 780.0),
    ("Prakasam Turmeric Powder", "Spices", 160.0),
    ("Tirupati Laddu Boxes", "Packaging", 6.0),
    ("Rayalaseema Millet Flour", "Grains", 95.0),
    ("Godavari Fresh Curd", "Dairy", 42.0),
    ("Vijayawada Green Tea", "Coffee and Tea", 260.0),
    ("Visakhapatnam Cleaning Wipes", "Cleaning Supplies", 125.0),
]
LEGACY_PRODUCT_NAMES = {
    "Arabica Coffee": "Araku Valley Arabica Coffee",
    "Oat Milk": "Kakinada Coconut Milk",
    "Paper Cups": "Vijayawada Paper Cups",
    "Vanilla Syrup": "Godavari Palm Jaggery",
    "Sanitizer Wipes": "Visakhapatnam Cleaning Wipes",
    "Matcha Powder": "Vijayawada Green Tea",
    "Greek Yogurt": "Godavari Fresh Curd",
}
LEGACY_WAREHOUSES = {
    "Central Warehouse": WAREHOUSE_ROWS[0],
    "North Warehouse": WAREHOUSE_ROWS[1],
}
LEGACY_FILES = {
    "Northstar_Supplier_Quote.pdf": "Sri_Lakshmi_Foods_Quotation.pdf",
    "Inventory_Operations_Guide.pdf": "Godavari_Fresh_Store_Operations.pdf",
    "Northstar_Sales_History.xlsx": "Godavari_Fresh_Monthly_Sales.xlsx",
}
TEXT_REPLACEMENTS = {
    "Northstar Food Supply": "Sri Lakshmi Foods and Provisions",
    "Central Warehouse": WAREHOUSE_ROWS[0][0],
    "North Warehouse": WAREHOUSE_ROWS[1][0],
    "Arabica Coffee": "Araku Valley Arabica Coffee",
    "Oat Milk": "Kakinada Coconut Milk",
    "Paper Cups": "Vijayawada Paper Cups",
    "Vanilla Syrup": "Godavari Palm Jaggery",
    "Sanitizer Wipes": "Visakhapatnam Cleaning Wipes",
    "Matcha Powder": "Vijayawada Green Tea",
    "Greek Yogurt": "Godavari Fresh Curd",
}


def utc_stamp(day, hour=10):
    return datetime.combine(day, time(hour=hour), tzinfo=timezone.utc)


def write_pdf(path, title, lines):
    styles = getSampleStyleSheet()
    story = [Paragraph(title, styles["Title"]), Spacer(1, 14)]
    story.extend(Paragraph(str(line), styles["BodyText"]) for line in lines)
    SimpleDocTemplate(str(path), pagesize=letter).build(story)


def write_quote(path, quote_date):
    write_pdf(
        path,
        "Supplier Price Quotation",
        [
            "Supplier: Sri Lakshmi Foods and Provisions",
            "Email: orders@srilakshmifoods.example",
            f"Quote reference: SLF-{quote_date:%Y%m%d}-18",
            f"Quote date: {quote_date.isoformat()}",
            "Delivery location: Visakhapatnam Central Store, Andhra Pradesh",
            "Expected lead time: 4 days",
            "Quoted items:",
            "Araku Valley Arabica Coffee | 24 bags | INR 680.00 per bag",
            "Guntur Sannam Chilli Powder | 40 packs | INR 185.00 per pack",
            "Prices are in Indian rupees. Quote valid for 21 days.",
        ],
    )


def write_operations_guide(path):
    write_pdf(
        path,
        "Godavari Fresh Store Operations",
        [
            "Godavari Fresh Supply Co. operates stores in Visakhapatnam, Vijayawada, Rajamahendravaram, and Tirupati.",
            "Araku Valley Arabica Coffee is stocked at each location. Compare the available quantity with the reorder level before raising a purchase request.",
            "Ongole Toned Milk and Godavari Fresh Curd are perishable items. Check each lot's expiry date before issuing stock.",
            "Managers review stock changes and transfers before confirmation. Employees can view stock and read reports.",
            "Monthly sales workbooks use product_name, units_sold, and date columns to calculate average daily demand.",
            "Supplier quotations list quantities, unit prices in INR, quote references, and expected delivery time.",
        ],
    )


def write_receiving_note(path, receipt_date, warehouse, product, quantity, supplier, reference):
    write_pdf(
        path,
        "Goods Receipt Note",
        [
            "Godavari Fresh Supply Co.",
            f"Receipt reference: {reference}",
            f"Received on: {receipt_date.isoformat()}",
            f"Receiving location: {warehouse.name}, {warehouse.city}, Andhra Pradesh",
            f"Supplier: {supplier}",
            f"Item received: {product.name}",
            f"Quantity received: {quantity} units",
            "The store team counted the delivery and filed this receipt for stock reconciliation.",
        ],
    )


def write_sales_workbook(path, today):
    workbook = Workbook()
    sales = workbook.active
    sales.title = "Monthly Sales"
    sales.append(["product_name", "units_sold", "date"])
    tracked_products = [
        PRODUCT_ROWS[index][0]
        for index in (0, 1, 2, 4, 8, 9, 10, 11, 14, 15)
    ]
    for day_offset in range(29, -1, -1):
        sale_date = today - timedelta(days=day_offset)
        for product_index, product_name in enumerate(tracked_products):
            quantity = 2 + ((day_offset + product_index * 3) % 9)
            sales.append([product_name, quantity, sale_date])
    for cell in sales[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(fill_type="solid", fgColor="334155")

    counts = workbook.create_sheet("Cycle Count Review")
    counts.append(["product_name", "warehouse", "counted_units", "review_note"])
    counts.append(["Vijayawada Paper Cups", "Visakhapatnam Central Store", 118, "Physical count completed"])
    counts.append(["Nellore Sona Masoori Rice", "Vijayawada Wholesale Store", 42, "Count checked by the store supervisor"])
    counts.append(["Godavari Fresh Curd", "Tirupati Retail Store", 0, "No remaining units at the afternoon count"])
    workbook.save(path)
    return tracked_products


def add_file(db, user_id, session_id, filename, path, file_type, text, summary, chunks, uploaded_at, workbook_json=None):
    record = db.query(UploadedFile).filter(
        UploadedFile.user_id == user_id,
        UploadedFile.session_id == session_id if session_id is not None else UploadedFile.session_id.is_(None),
        UploadedFile.filename == filename,
    ).first()
    if record is None:
        record = UploadedFile(user_id=user_id, session_id=session_id, filename=filename)
    record.file_type = file_type
    record.file_path = str(path.resolve())
    record.extracted_text = text
    record.summary = summary
    record.workbook_json = workbook_json
    record.source_chunks = json.dumps(chunks, default=str)
    record.uploaded_at = uploaded_at
    db.add(record)
    db.flush()
    return record


def relink_legacy_files(db, today, quote_path, guide_path, sales_path, quote_text, guide_text, sales_text, guide_chunks, sales_chunks, workbook_json, quote_day):
    file_data = {
        quote_path.name: {
            "path": quote_path,
            "type": "application/pdf",
            "text": quote_text,
            "summary": "Supplier quotation for coffee and chilli powder, delivered to Visakhapatnam.",
            "chunks": [{"location": "page 1", "text": quote_text}],
            "uploaded_at": utc_stamp(quote_day, 10),
            "workbook_json": None,
        },
        guide_path.name: {
            "path": guide_path,
            "type": "application/pdf",
            "text": guide_text,
            "summary": "Store procedures for stock counts, expiry checks, transfers, and supplier orders.",
            "chunks": guide_chunks,
            "uploaded_at": utc_stamp(today - timedelta(days=27), 9),
            "workbook_json": None,
        },
        sales_path.name: {
            "path": sales_path,
            "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "text": sales_text,
            "summary": "Monthly sales workbook with daily quantities for ten Andhra Pradesh store products.",
            "chunks": sales_chunks,
            "uploaded_at": utc_stamp(today - timedelta(days=2), 13),
            "workbook_json": workbook_json,
        },
    }
    for uploaded in db.query(UploadedFile).filter(UploadedFile.filename.in_(file_data)).all():
        details = file_data[uploaded.filename]
        uploaded.file_path = str(details["path"].resolve())
        uploaded.file_type = details["type"]
        uploaded.extracted_text = details["text"]
        uploaded.summary = details["summary"]
        uploaded.source_chunks = json.dumps(details["chunks"], default=str)
        uploaded.workbook_json = details["workbook_json"]
        uploaded.uploaded_at = details["uploaded_at"]


def restore_business_files(db):
    for uploaded in db.query(UploadedFile).all():
        path = Path(uploaded.file_path)
        if "business_data" not in path.parts or path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        if uploaded.filename.lower().endswith((".xlsx", ".xls")):
            end_date = (uploaded.uploaded_at.date() if uploaded.uploaded_at else date.today()) + timedelta(days=2)
            write_sales_workbook(path, end_date)
        else:
            lines = (uploaded.extracted_text or uploaded.summary or "Store record").splitlines()
            title = "Goods Receipt Note" if uploaded.filename.startswith("Goods_Receipt_") else "Store Operations Document"
            write_pdf(path, title, [line for line in lines if line.strip()])


def get_or_create_user(db, role, password):
    email, name = BUSINESS_USERS[role]
    user = db.query(User).filter(func.lower(User.email) == email.lower()).first()
    if user:
        return user
    user = db.query(User).filter(User.role == role).order_by(User.id.asc()).first()
    if user:
        if user.name in {"Alex Morgan", "Priya Shah", "Jordan Lee"}:
            user.name = name
        return user
    if not password:
        raise SystemExit(f"Set {PASSWORD_ENV} before creating missing user accounts.")
    user = User(name=name, email=email, hashed_password=hash_password(password), role=role)
    db.add(user)
    db.flush()
    return user


def normalize_legacy_names(db):
    inspector = inspect(db.get_bind())
    if "role_id" in {column["name"] for column in inspector.get_columns("users")} and "roles" in inspector.get_table_names():
        db.execute(text(
            "UPDATE users AS existing_user "
            "SET role = lower(existing_role.name) "
            "FROM roles AS existing_role "
            "WHERE existing_user.role_id = existing_role.id "
            "AND lower(existing_role.name) IN ('admin', 'manager', 'employee')"
        ))
    for warehouse in db.query(Warehouse).all():
        replacement = LEGACY_WAREHOUSES.get(warehouse.name)
        if replacement:
            warehouse.name, warehouse.city = replacement
            if warehouse.manager in {"Priya Shah", "Alex Morgan"}:
                warehouse.manager = BUSINESS_USERS["manager"][1]
    for product in db.query(Product).all():
        new_name = LEGACY_PRODUCT_NAMES.get(product.name)
        if new_name:
            product.name = new_name
    for supplier in db.query(Supplier).filter(Supplier.name == "Northstar Food Supply").all():
        supplier.name = "Sri Lakshmi Foods and Provisions"
        supplier.email = "orders@srilakshmifoods.example"
    for user in db.query(User).all():
        if user.name == "Alex Morgan":
            user.name = "Ananya Reddy"
            if user.email.lower().endswith("@northstar.example") and db.query(User).filter(func.lower(User.email) == BUSINESS_USERS["admin"][0].lower()).first() is None:
                user.email = BUSINESS_USERS["admin"][0]
        elif user.name == "Priya Shah":
            user.name = "Sai Kiran Varma"
            if user.email.lower().endswith("@northstar.example") and db.query(User).filter(func.lower(User.email) == BUSINESS_USERS["manager"][0].lower()).first() is None:
                user.email = BUSINESS_USERS["manager"][0]
        elif user.name == "Jordan Lee":
            user.name = "Lakshmi Prasanna"
            if user.email.lower().endswith("@northstar.example") and db.query(User).filter(func.lower(User.email) == BUSINESS_USERS["employee"][0].lower()).first() is None:
                user.email = BUSINESS_USERS["employee"][0]
    for session in db.query(ChatSession).all():
        if session.title == "Stock and Supplier Questions":
            session.title = "Visakhapatnam Supplier Review"
        elif session.title == "Employee Inventory Review":
            session.title = "Store Floor Stock Review"
        elif session.title == "Alex Morgan Chat":
            session.title = "Ananya Reddy Operations Review"
    for message in db.query(ChatMessage).all():
        for previous, current in TEXT_REPLACEMENTS.items():
            message.message = message.message.replace(previous, current)
    for action in db.query(StockAction).all():
        for previous, current in TEXT_REPLACEMENTS.items():
            action.request_text = action.request_text.replace(previous, current)
    for uploaded in db.query(UploadedFile).all():
        uploaded.filename = LEGACY_FILES.get(uploaded.filename, uploaded.filename)
        for previous, current in TEXT_REPLACEMENTS.items():
            if uploaded.extracted_text:
                uploaded.extracted_text = uploaded.extracted_text.replace(previous, current)
            if uploaded.summary:
                uploaded.summary = uploaded.summary.replace(previous, current)
            if uploaded.source_chunks:
                uploaded.source_chunks = uploaded.source_chunks.replace(previous, current)
    for order in db.query(PurchaseOrder).all():
        if order.quote_reference == "DB-2026-1042":
            order.quote_reference = f"SLF-{date.today() - timedelta(days=6):%Y%m%d}-18"
        for previous, current in TEXT_REPLACEMENTS.items():
            order.items_json = order.items_json.replace(previous, current)


def create_roles(db, password):
    users = {
        role: get_or_create_user(db, role, password)
        for role in ("admin", "manager", "employee")
    }
    return users


def ensure_business_accounts(db, users=None):
    accounts = {}
    for role in ("manager", "employee"):
        account_password = os.environ.get(BUSINESS_PASSWORD_ENVS[role])
        if not account_password:
            continue
        email, name = BUSINESS_USERS[role]
        user = db.query(User).filter(func.lower(User.email) == email.lower()).first()
        if user is not None and user.role == "admin":
            raise SystemExit(f"The requested {role} email is already assigned to an admin account.")
        if user is None:
            user = db.query(User).filter(User.role == role).order_by(User.id.asc()).first()
        if user is None and users is not None:
            user = users.get(role)
        if user is None:
            user = User(
                name=name,
                email=email,
                hashed_password=hash_password(account_password),
                role=role,
            )
            db.add(user)
            db.flush()
        previous_name = user.name
        user.name = name
        user.email = email
        user.hashed_password = hash_password(account_password)
        user.role = role
        db.flush()
        if role == "manager":
            db.query(Warehouse).filter(
                Warehouse.manager.in_([previous_name, "Sai Kiran Varma", "Priya Shah"])
            ).update({Warehouse.manager: name}, synchronize_session=False)
        accounts[role] = user
    return accounts


def create_inventory(db, products, warehouses):
    rows = []
    for product_index, (name, _, _) in enumerate(PRODUCT_ROWS):
        product = products[name]
        for warehouse_index, warehouse in enumerate(warehouses):
            reorder_level = 12 + ((product_index * 2 + warehouse_index) % 9)
            is_low = (product_index + warehouse_index * 2) % 5 == 0
            quantity = max(2, reorder_level // 3) if is_low else reorder_level + 8 + ((product_index * 3 + warehouse_index * 7) % 34)
            demand = round(0.8 + ((product_index + warehouse_index * 2) % 10) * 0.35, 2)
            lead_time = 2 + ((product_index + warehouse_index) % 6)
            row = db.query(Inventory).filter(
                Inventory.product_id == product.id,
                Inventory.warehouse_id == warehouse.id,
            ).first()
            if row is None:
                row = Inventory(
                    product_id=product.id,
                    warehouse_id=warehouse.id,
                    quantity=quantity,
                    reorder_level=reorder_level,
                    average_daily_demand=demand,
                    supplier_lead_time_days=lead_time,
                )
                db.add(row)
                db.flush()
            else:
                row.reorder_level = reorder_level
                row.average_daily_demand = demand
                row.supplier_lead_time_days = lead_time
            rows.append(row)
    return rows


def add_monthly_stock_activity(db, inventory_rows, user, today):
    selected_rows = inventory_rows[:15]
    for pair_index, row in enumerate(selected_rows):
        first_day = today - timedelta(days=29 - pair_index * 2)
        initial_quantity = row.quantity
        increased_quantity = initial_quantity + 1
        db.add(StockMovement(
            inventory_id=row.id,
            user_id=user.id,
            movement_type="adjustment",
            quantity_before=initial_quantity,
            quantity_change=1,
            quantity_after=increased_quantity,
            reason="Receiving count corrected after the supplier delivery was checked.",
            created_at=utc_stamp(first_day, 11),
        ))
        db.add(StockMovement(
            inventory_id=row.id,
            user_id=user.id,
            movement_type="adjustment",
            quantity_before=increased_quantity,
            quantity_change=-1,
            quantity_after=initial_quantity,
            reason="Counter issue reconciled with the end-of-day stock count.",
            created_at=utc_stamp(first_day + timedelta(days=1), 17),
        ))


def add_batches(db, products, warehouses, inventory_rows, today):
    perishable_names = {"Ongole Toned Milk", "Godavari Fresh Curd", "Tirupati Cow Ghee", "Kakinada Coconut Milk"}
    row_by_key = {(row.product_id, row.warehouse_id): row for row in inventory_rows}
    for product_index, name in enumerate(perishable_names):
        product = products[name]
        for warehouse_index, warehouse in enumerate(warehouses):
            row = row_by_key[(product.id, warehouse.id)]
            existing_batches = db.query(StockBatch).filter(
                StockBatch.product_id == product.id,
                StockBatch.warehouse_id == warehouse.id,
            ).count()
            if existing_batches:
                continue
            offsets = [-2, 4, 11, 24]
            expiry_offset = offsets[(product_index + warehouse_index) % len(offsets)]
            first_quantity = max(1, row.quantity // 3)
            second_quantity = max(1, row.quantity - first_quantity)
            db.add_all([
                StockBatch(
                    product_id=product.id,
                    warehouse_id=warehouse.id,
                    lot_code=f"GF-{product_index + 1:02d}-{warehouse_index + 1:02d}-A",
                    quantity=first_quantity,
                    expiration_date=today + timedelta(days=expiry_offset),
                ),
                StockBatch(
                    product_id=product.id,
                    warehouse_id=warehouse.id,
                    lot_code=f"GF-{product_index + 1:02d}-{warehouse_index + 1:02d}-B",
                    quantity=second_quantity,
                    expiration_date=today + timedelta(days=35 + warehouse_index),
                ),
            ])


def add_chat_history(db, users, sessions, inventory_rows, products, warehouses, today):
    row_by_pair = {(row.product_id, row.warehouse_id): row for row in inventory_rows}
    for day_offset in range(29, -1, -1):
        day = today - timedelta(days=day_offset)
        role = ("manager", "employee", "admin")[day_offset % 3]
        session = sessions[role]
        product_name, _, _ = PRODUCT_ROWS[(day_offset * 3) % len(PRODUCT_ROWS)]
        warehouse = warehouses[day_offset % len(warehouses)]
        row = row_by_pair[(products[product_name].id, warehouse.id)]
        questions = [
            f"How many units of {product_name} are available at {warehouse.name}?",
            f"Does {product_name} at {warehouse.name} need attention this week?",
            f"Please compare the current stock for {product_name} at {warehouse.name} with its reorder level.",
        ]
        answer = (
            f"The inventory record for {product_name} at {warehouse.name} shows {row.quantity} units. "
            f"The reorder level is {row.reorder_level} units, and average daily demand is {row.average_daily_demand:.2f} units."
        )
        db.add_all([
            ChatMessage(
                session_id=session.id,
                role="user",
                message=questions[day_offset % len(questions)],
                created_at=utc_stamp(day, 9),
            ),
            ChatMessage(
                session_id=session.id,
                role="assistant",
                message=answer,
                created_at=utc_stamp(day, 9) + timedelta(minutes=1),
            ),
        ])


def add_recommendation_history(db, manager, inventory_rows, today):
    for day_offset in range(29, -1, -1):
        row = inventory_rows[(day_offset * 5) % len(inventory_rows)]
        accepted = day_offset % 4 != 0
        recommendation_type = "transfer" if day_offset % 2 else "reorder"
        db.add(RecommendationOutcome(
            user_id=manager.id,
            inventory_id=row.id,
            recommendation_type=recommendation_type,
            recommended_quantity=max(1, row.reorder_level - row.quantity),
            actual_quantity=max(1, row.reorder_level - row.quantity) if accepted else None,
            accepted=accepted,
            note=(
                "The store manager accepted the suggested quantity after checking the weekly count."
                if accepted
                else "The manager deferred the suggestion until the next supplier review."
            ),
            created_at=utc_stamp(today - timedelta(days=day_offset), 16),
        ))


def add_action_history(db, manager, inventory_rows, today):
    low_row = next((row for row in inventory_rows if row.quantity < row.reorder_level), inventory_rows[0])
    details = {
        "inventory_id": low_row.id,
        "quantity_before": low_row.quantity,
        "quantity_after": low_row.quantity + 3,
    }
    pending = StockAction(
        user_id=manager.id,
        action_type="set_quantity",
        request_text=f"Set the counted quantity to {low_row.quantity + 3} for the next stock review.",
        generated_sql=f"UPDATE inventory SET quantity = {low_row.quantity + 3} WHERE id = {low_row.id}",
        details_json=json.dumps(details),
        status="pending",
        created_at=utc_stamp(today - timedelta(days=1), 14),
    )
    db.add(pending)

    source_row = next((
        row for row in inventory_rows
        if row.product_id == low_row.product_id
        and row.warehouse_id != low_row.warehouse_id
        and row.quantity > row.reorder_level
    ), None)
    if source_row is not None:
        product = db.query(Product).filter(Product.id == low_row.product_id).first()
        transfer_details = {
            "source_inventory_id": source_row.id,
            "source_warehouse_id": source_row.warehouse_id,
            "source_quantity_before": source_row.quantity,
            "destination_inventory_id": low_row.id,
            "destination_warehouse_id": low_row.warehouse_id,
            "destination_quantity_before": low_row.quantity,
            "product_id": low_row.product_id,
            "quantity": 2,
            "recommendation_inventory_id": low_row.id,
            "recommended_quantity": 2,
        }
        db.add(StockAction(
            user_id=manager.id,
            action_type="transfer",
            request_text=f"Move two units of {product.name} to support the lower store balance.",
            generated_sql=f"Transfer 2 units of {product.name} to the destination store",
            details_json=json.dumps(transfer_details),
            status="pending",
            created_at=utc_stamp(today - timedelta(days=2), 13),
        ))

    cancelled = StockAction(
        user_id=manager.id,
        action_type="set_quantity",
        request_text="The receiving count was checked and this stock change was cancelled.",
        generated_sql=f"UPDATE inventory SET quantity = {low_row.quantity} WHERE id = {low_row.id}",
        details_json=json.dumps({
            "inventory_id": low_row.id,
            "quantity_before": low_row.quantity,
            "quantity_after": low_row.quantity,
        }),
        status="cancelled",
        reviewed_by_user_id=manager.id,
        reviewed_at=utc_stamp(today - timedelta(days=4), 12),
        created_at=utc_stamp(today - timedelta(days=5), 10),
    )
    db.add(cancelled)


def ensure_seeded_sales_records(db):
    monthly_sales_file = db.query(UploadedFile).filter(
        UploadedFile.filename == "Godavari_Fresh_Monthly_Sales.xlsx",
        UploadedFile.session_id.is_(None),
    ).order_by(UploadedFile.id.desc()).first()
    if monthly_sales_file is None:
        return
    existing_records = db.query(SalesRecord.id).filter(
        SalesRecord.source_file_id == monthly_sales_file.id
    ).first()
    if existing_records:
        return
    from app.services.excel_analyzer_service import apply_sales_demand

    apply_sales_demand(db, monthly_sales_file.user_id, monthly_sales_file.id)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm-business-data", "--confirm-presentation-data", action="store_true", required=True)
    parser.parse_args(argv)
    init_db()
    today = date.today()
    password = os.environ.get(PASSWORD_ENV)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db = SessionLocal()
    try:
        marker_product = db.query(Product).filter(Product.name == PRODUCT_ROWS[0][0]).first()
        marker_warehouse = db.query(Warehouse).filter(Warehouse.name == WAREHOUSE_ROWS[0][0]).first()
        marker_session = db.query(ChatSession).filter(ChatSession.title == "Monthly Store Stock Review").first()
        if marker_product and marker_warehouse and marker_session:
            restore_business_files(db)
            ensure_business_accounts(db)
            ensure_seeded_sales_records(db)
            db.commit()
            print("The Andhra Pradesh monthly inventory data is already in the database.")
            return

        normalize_legacy_names(db)
        users = create_roles(db, password)
        users.update(ensure_business_accounts(db, users))

        warehouses = []
        for name, city in WAREHOUSE_ROWS:
            warehouse = db.query(Warehouse).filter(Warehouse.name == name).first()
            if warehouse is None:
                warehouse = Warehouse(name=name, city=city, manager=users["manager"].name)
                db.add(warehouse)
                db.flush()
            else:
                warehouse.city = city
                warehouse.manager = users["manager"].name
            warehouses.append(warehouse)

        products = {}
        for name, category, price in PRODUCT_ROWS:
            product = db.query(Product).filter(Product.name == name).first()
            if product is None:
                product = Product(name=name, category=category, price=price)
                db.add(product)
                db.flush()
            else:
                product.category = category
                product.price = price
            products[name] = product

        sessions = {}
        for role, user in users.items():
            session = ChatSession(
                user_id=user.id,
                title="Monthly Store Stock Review" if role == "manager" else f"{user.name} Stock Review",
                created_at=utc_stamp(today - timedelta(days=29), 8),
            )
            db.add(session)
            db.flush()
            sessions[role] = session

        inventory_rows = create_inventory(db, products, warehouses)
        supplier = db.query(Supplier).filter(Supplier.name == "Sri Lakshmi Foods and Provisions").first()
        if supplier is None:
            supplier = Supplier(name="Sri Lakshmi Foods and Provisions", email="orders@srilakshmifoods.example")
            db.add(supplier)
            db.flush()

        quote_day = today - timedelta(days=6)
        quote_path = DATA_DIR / "Sri_Lakshmi_Foods_Quotation.pdf"
        write_quote(quote_path, quote_day)
        quote_text = (
            "Supplier: Sri Lakshmi Foods and Provisions\n"
            "Email: orders@srilakshmifoods.example\n"
            f"Quote reference: SLF-{quote_day:%Y%m%d}-18\n"
            "Lead time: 4 days\n"
            "Araku Valley Arabica Coffee: 24 bags at INR 680 per bag\n"
            "Guntur Sannam Chilli Powder: 40 packs at INR 185 per pack"
        )
        quote_file = add_file(
            db,
            users["manager"].id,
            None,
            quote_path.name,
            quote_path,
            "application/pdf",
            quote_text,
            "Supplier quotation for coffee and chilli powder, delivered to Visakhapatnam.",
            [{"location": "page 1", "text": quote_text}],
            utc_stamp(quote_day, 10),
        )
        for role, user in users.items():
            add_file(
                db,
                user.id,
                sessions[role].id,
                quote_path.name,
                quote_path,
                "application/pdf",
                quote_text,
                "Quotation details for the monthly stock review.",
                [{"location": "page 1", "text": quote_text}],
                utc_stamp(quote_day, 10),
            )

        guide_path = DATA_DIR / "Godavari_Fresh_Store_Operations.pdf"
        write_operations_guide(guide_path)
        guide_text = (
            "Godavari Fresh Supply Co. operates stores in Visakhapatnam, Vijayawada, "
            "Rajamahendravaram, and Tirupati. Araku Valley Arabica Coffee is stocked "
            "at each location. Managers review stock changes and transfers before confirmation."
        )
        guide_chunks = [{"location": "page 1", "text": guide_text}]
        for role, user in users.items():
            add_file(
                db,
                user.id,
                sessions[role].id,
                guide_path.name,
                guide_path,
                "application/pdf",
                guide_text,
                "Store procedures for stock counts, expiry checks, transfers, and supplier orders.",
                guide_chunks,
                utc_stamp(today - timedelta(days=27 + list(users).index(role)), 9),
            )

        sales_path = DATA_DIR / "Godavari_Fresh_Monthly_Sales.xlsx"
        tracked_products = write_sales_workbook(sales_path, today)
        sales_text = f"Monthly sales history from {today - timedelta(days=29)} to {today}."
        sales_rows = [
            {"name": "Monthly Sales", "rows": 301, "columns": ["product_name", "units_sold", "date"], "validation": {"errors": [], "warnings": []}},
            {"name": "Cycle Count Review", "rows": 3, "columns": ["product_name", "warehouse", "counted_units", "review_note"], "validation": {"errors": [], "warnings": []}},
        ]
        sales_chunks = [{
            "location": "sheet Monthly Sales",
            "text": f"Thirty days of dated sales records for {', '.join(tracked_products)}.",
        }]
        workbook_json = json.dumps({"sheets": sales_rows, "source_chunks": sales_chunks})
        sales_file = add_file(
            db,
            users["manager"].id,
            None,
            sales_path.name,
            sales_path,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            sales_text,
            "Monthly sales workbook with daily quantities for ten Andhra Pradesh store products.",
            sales_chunks,
            utc_stamp(today - timedelta(days=2), 13),
            workbook_json,
        )
        relink_legacy_files(
            db,
            today,
            quote_path,
            guide_path,
            sales_path,
            quote_text,
            guide_text,
            sales_text,
            guide_chunks,
            sales_chunks,
            workbook_json,
            quote_day,
        )
        for role, user in users.items():
            add_file(
                db,
                user.id,
                sessions[role].id,
                sales_path.name,
                sales_path,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                sales_text,
                "Monthly sales figures for inventory questions.",
                sales_chunks,
                utc_stamp(today - timedelta(days=2), 13),
                workbook_json,
            )
            if role != "manager":
                add_file(
                    db,
                    user.id,
                    None,
                    sales_path.name,
                    sales_path,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    sales_text,
                    "Monthly sales figures for inventory analysis.",
                    sales_chunks,
                    utc_stamp(today - timedelta(days=2), 13),
                    workbook_json,
                )

        supplier_names = [
            "Sri Lakshmi Foods and Provisions",
            "Godavari Dairy Distributors",
            "Vijaya Packaging Traders",
            "Rayalaseema Agro Products",
        ]
        supplier_by_name = {supplier.name: supplier}
        for name in supplier_names[1:]:
            item = db.query(Supplier).filter(Supplier.name == name).first()
            if item is None:
                item = Supplier(name=name, email=f"orders@{name.split()[0].lower()}.example")
                db.add(item)
                db.flush()
            supplier_by_name[name] = item

        quote_reference = f"SLF-{quote_day:%Y%m%d}-18"
        quote_items = [
            {"product_name": PRODUCT_ROWS[0][0], "quantity": 24, "unit_price": 680.0, "line_total": 16320.0, "source_page": 1},
            {"product_name": PRODUCT_ROWS[2][0], "quantity": 40, "unit_price": 185.0, "line_total": 7400.0, "source_page": 1},
        ]
        for order_index, day_offset in enumerate((22, 15, 8, 2)):
            order_day = today - timedelta(days=day_offset)
            po_supplier = supplier_by_name[supplier_names[order_index % len(supplier_names)]]
            db.add(PurchaseOrder(
                supplier_id=po_supplier.id,
                user_id=users["manager"].id,
                source_file_id=quote_file.id,
                inventory_id=inventory_rows[order_index].id,
                quote_reference=f"GF-{order_day:%Y%m%d}-{order_index + 31:02d}",
                items_json=json.dumps(quote_items),
                total_amount=sum(item["line_total"] for item in quote_items),
                recommended_quantity=24 + order_index * 4,
                status="draft",
                created_at=utc_stamp(order_day, 14),
            ))

        add_batches(db, products, warehouses, inventory_rows, today)
        add_monthly_stock_activity(db, inventory_rows, users["manager"], today)
        add_chat_history(db, users, sessions, inventory_rows, products, warehouses, today)
        add_recommendation_history(db, users["manager"], inventory_rows, today)
        add_action_history(db, users["manager"], inventory_rows, today)

        receipt_suppliers = [supplier.name for supplier in supplier_by_name.values()]
        for day_offset in range(29, -1, -1):
            receipt_day = today - timedelta(days=day_offset)
            warehouse = warehouses[day_offset % len(warehouses)]
            product_name, _, _ = PRODUCT_ROWS[(day_offset * 2) % len(PRODUCT_ROWS)]
            product = products[product_name]
            quantity = 12 + ((day_offset * 7) % 38)
            supplier_name = receipt_suppliers[day_offset % len(receipt_suppliers)]
            reference = f"GRN-{receipt_day:%Y%m%d}-{day_offset + 1:02d}"
            filename = f"Goods_Receipt_{warehouse.city.replace(' ', '_')}_{receipt_day.isoformat()}.pdf"
            path = DATA_DIR / filename
            write_receiving_note(path, receipt_day, warehouse, product, quantity, supplier_name, reference)
            text = (
                f"Goods receipt {reference}. Received {quantity} units of {product.name} "
                f"from {supplier_name} at {warehouse.name} in {warehouse.city} on {receipt_day.isoformat()}."
            )
            role = ("manager", "employee", "admin")[day_offset % 3]
            add_file(
                db,
                users[role].id,
                None,
                filename,
                path,
                "application/pdf",
                text,
                f"Goods receipt for {product.name} at {warehouse.name}.",
                [{"location": "page 1", "text": text}],
                utc_stamp(receipt_day, 15),
            )

        add_file(
            db,
            users["admin"].id,
            None,
            quote_path.name,
            quote_path,
            "application/pdf",
            quote_text,
            "Supplier quotation retained for procurement review.",
            [{"location": "page 1", "text": quote_text}],
            utc_stamp(quote_day, 11),
        )

        ensure_seeded_sales_records(db)
        db.commit()
        print("Andhra Pradesh monthly inventory data has been added.")
        print(f"Date range: {today - timedelta(days=29)} through {today}")
        print("The data covers inventory, stock history, batches, chat, documents, recommendations, and supplier drafts.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
