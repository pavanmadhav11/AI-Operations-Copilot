import argparse
import json
import os
from datetime import date, timedelta

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from sqlalchemy import func

from app.auth.hashing import hash_password
from app.db.init_db import init_db
from app.db.database import SessionLocal
from app.models.chat import ChatMessage
from app.models.chat_session import ChatSession
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.purchase_order import PurchaseOrder
from app.models.recommendation_outcome import RecommendationOutcome
from app.models.stock_action import StockAction
from app.models.stock_batch import StockBatch
from app.models.stock_movement import StockMovement
from app.models.supplier import Supplier
from app.models.uploaded_file import UploadedFile
from app.models.user import User
from app.models.warehouse import Warehouse

DEMO_DIR = "business_data"
DEMO_PASSWORD_ENV = "PRESENTATION_PASSWORD"
DEMO_USERS = {
    "admin": ("alex.morgan@northstar.example", "Alex Morgan"),
    "manager": ("priya.shah@northstar.example", "Priya Shah"),
    "employee": ("jordan.lee@northstar.example", "Jordan Lee"),
}


def create_pdf(filepath, title, lines):
    styles = getSampleStyleSheet()
    story = [Paragraph(title, styles["Title"]), Spacer(1, 16)]
    story.extend(Paragraph(line, styles["BodyText"]) for line in lines)
    SimpleDocTemplate(filepath, pagesize=letter).build(story)


def create_quote_pdf(filepath):
    create_pdf(
        filepath,
        "Supplier Quote",
        [
            "Supplier: Northstar Food Supply",
            "Email: purchasing@northstar.example",
            "Quote reference: DB-2026-1042",
            "Lead time: 5 days",
            "Quoted items:",
            "Product: Arabica Coffee | Quantity: 25 | Unit price: $13.50",
            "Product: Paper Cups | Quantity: 1000 | Unit price: $0.04",
            "Prices are in US dollars. Quote valid for 30 days.",
        ],
    )


def create_guide_pdf(filepath):
    create_pdf(
        filepath,
        "Warehouse Stock Guide",
        [
            "Inventory Operations Guide",
            "Arabica Coffee is stored at Central Warehouse and North Warehouse.",
            "The reorder level at Central Warehouse is 15 bags. The reorder level at North Warehouse is 12 bags.",
            "Oat Milk has a 3 day supplier lead time. Review its expiry date before using it.",
            "Managers prepare and confirm stock changes. Employees can view inventory but cannot change stock.",
            "Use the sales workbook to calculate average daily demand for matching products.",
        ],
    )


def create_sales_workbook(filepath, today):
    workbook = Workbook()
    sales = workbook.active
    sales.title = "Sales History"
    sales.append(["product_name", "units_sold", "date"])
    sales_rows = [
        ("Arabica Coffee", 5),
        ("Arabica Coffee", 4),
        ("Arabica Coffee", 6),
        ("Arabica Coffee", 4),
        ("Arabica Coffee", 5),
        ("Arabica Coffee", 4),
        ("Arabica Coffee", 6),
        ("Oat Milk", 3),
        ("Oat Milk", 2),
        ("Oat Milk", 4),
        ("Oat Milk", 3),
        ("Oat Milk", 2),
        ("Oat Milk", 3),
        ("Oat Milk", 3),
    ]
    for index, (product_name, quantity) in enumerate(sales_rows):
        sales.append([product_name, quantity, today - timedelta(days=6 - index % 7)])
    for cell in sales[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(fill_type="solid", fgColor="1D4ED8")

    checks = workbook.create_sheet("Quality Checks")
    checks.append(["item_code", "stock_count", "note", None])
    checks.append(["CUP-12", 120, "duplicate receipt", "unexpected value under blank heading"])
    checks.append(["CUP-12", 120, "duplicate receipt", "unexpected value under blank heading"])
    checks.append(["MILK-1", -4, "negative count to review", "unexpected value under blank heading"])
    checks.append([None, None, "blank cells to review", "unexpected value under blank heading"])
    workbook.save(filepath)


def add_uploaded_file(db, user_id, session_id, filename, filepath, file_type, text, summary, chunks, workbook_json=None):
    record = UploadedFile(
        user_id=user_id,
        session_id=session_id,
        filename=filename,
        file_type=file_type,
        file_path=os.path.abspath(filepath),
        extracted_text=text,
        summary=summary,
        workbook_json=workbook_json,
        source_chunks=json.dumps(chunks, default=str),
    )
    db.add(record)
    db.flush()
    return record


def create_demo_files(today):
    os.makedirs(DEMO_DIR, exist_ok=True)
    quote_path = os.path.join(DEMO_DIR, "Northstar_Supplier_Quote.pdf")
    guide_path = os.path.join(DEMO_DIR, "Inventory_Operations_Guide.pdf")
    workbook_path = os.path.join(DEMO_DIR, "Northstar_Sales_History.xlsx")
    create_quote_pdf(quote_path)
    create_guide_pdf(guide_path)
    create_sales_workbook(workbook_path, today)
    return quote_path, guide_path, workbook_path


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm-presentation-data", action="store_true", required=True)
    parser.parse_args(argv)
    demo_password = os.environ.get(DEMO_PASSWORD_ENV)
    if not demo_password or len(demo_password) < 12:
        raise SystemExit(f"Set {DEMO_PASSWORD_ENV} to a password with at least 12 characters.")
    init_db()
    today = date.today()
    quote_path, guide_path, workbook_path = create_demo_files(today)
    db = SessionLocal()
    demo_emails = [email for email, _ in DEMO_USERS.values()]
    try:
        existing = db.query(User).filter(func.lower(User.email).in_([email.lower() for email in demo_emails])).first()
        if existing:
            print("Presentation accounts already exist. No database records were changed.")
            return

        users = {}
        for role, (email, name) in DEMO_USERS.items():
            user = User(name=name, email=email, hashed_password=hash_password(demo_password), role=role)
            db.add(user)
            db.flush()
            users[role] = user

        central = Warehouse(name="Central Warehouse", city="Austin", manager="Priya Shah")
        north = Warehouse(name="North Warehouse", city="Dallas", manager="Priya Shah")
        db.add_all([central, north])
        db.flush()

        product_rows = [
            ("Arabica Coffee", "Coffee", 18.5),
            ("Oat Milk", "Dairy Alternative", 4.25),
            ("Paper Cups", "Packaging", 0.08),
            ("Vanilla Syrup", "Beverage", 7.5),
            ("Sanitizer Wipes", "Cleaning", 9.0),
            ("Matcha Powder", "Tea", 24.0),
            ("Greek Yogurt", "Dairy", 5.75),
        ]
        products = {}
        for name, category, price in product_rows:
            product = Product(name=name, category=category, price=price)
            db.add(product)
            db.flush()
            products[name] = product

        inventory_rows = [
            ("Arabica Coffee", central, 5, 15, 2.0, 6),
            ("Arabica Coffee", north, 40, 12, 1.5, 6),
            ("Oat Milk", central, 2, 10, 1.0, 3),
            ("Paper Cups", central, 3, 12, 1.2, 10),
            ("Vanilla Syrup", central, 4, 10, 0.5, 8),
            ("Sanitizer Wipes", central, 6, 14, 0.8, 5),
            ("Matcha Powder", central, 3, 9, 0.4, 12),
            ("Greek Yogurt", north, 24, 8, 1.5, 4),
        ]
        inventory = {}
        for name, warehouse, quantity, reorder_level, demand, lead_time in inventory_rows:
            row = Inventory(
                product_id=products[name].id,
                warehouse_id=warehouse.id,
                quantity=quantity,
                reorder_level=reorder_level,
                average_daily_demand=demand,
                supplier_lead_time_days=lead_time,
            )
            db.add(row)
            db.flush()
            inventory[(name, warehouse.name)] = row
            db.add(StockMovement(
                inventory_id=row.id,
                user_id=users["manager"].id,
                movement_type="opening_stock",
                quantity_before=0,
                quantity_change=quantity,
                quantity_after=quantity,
                reason="Opening stock",
            ))

        batch_rows = [
            ("Arabica Coffee", central, "COF-C-100", 5, today + timedelta(days=180)),
            ("Arabica Coffee", north, "COF-N-200", 40, today + timedelta(days=210)),
            ("Oat Milk", central, "OAT-EXP-301", 2, today + timedelta(days=12)),
            ("Paper Cups", central, "CUP-400", 3, today + timedelta(days=90)),
            ("Vanilla Syrup", central, "SYR-500", 4, today + timedelta(days=120)),
            ("Sanitizer Wipes", central, "SAN-EXP-601", 6, today + timedelta(days=14)),
            ("Matcha Powder", central, "MAT-EXP-701", 3, today + timedelta(days=20)),
            ("Greek Yogurt", north, "YOG-OLD-800", 0, today - timedelta(days=30)),
            ("Greek Yogurt", north, "YOG-EXP-801", 6, today - timedelta(days=3)),
            ("Greek Yogurt", north, "YOG-FRESH-802", 18, today + timedelta(days=25)),
        ]
        for name, warehouse, lot_code, quantity, expiration_date in batch_rows:
            db.add(StockBatch(
                product_id=products[name].id,
                warehouse_id=warehouse.id,
                lot_code=lot_code,
                quantity=quantity,
                expiration_date=expiration_date,
            ))

        yogurt_inventory = inventory[("Greek Yogurt", north.name)]
        db.add(StockMovement(
            inventory_id=yogurt_inventory.id,
            user_id=users["manager"].id,
            movement_type="expiry_writeoff",
            quantity_before=26,
            quantity_change=-2,
            quantity_after=24,
            reason="Historical expiry write-off",
        ))

        manager_session = ChatSession(user_id=users["manager"].id, title="Stock and Supplier Questions")
        employee_session = ChatSession(user_id=users["employee"].id, title="Employee Inventory Review")
        admin_session = ChatSession(user_id=users["admin"].id, title="Alex Morgan Chat")
        db.add_all([manager_session, employee_session, admin_session])
        db.flush()

        quote_text = "\n".join([
            "Supplier: Northstar Food Supply",
            "Email: purchasing@northstar.example",
            "Quote reference: DB-2026-1042",
            "Lead time: 5 days",
            "Product: Arabica Coffee | Quantity: 25 | Unit price: $13.50",
            "Product: Paper Cups | Quantity: 1000 | Unit price: $0.04",
        ])
        quote_chunks = [{"location": "page 1", "text": quote_text}]
        quote_file = add_uploaded_file(
            db, users["manager"].id, None, "Northstar_Supplier_Quote.pdf", quote_path,
            "application/pdf", quote_text, "Sample supplier quote for Arabica Coffee and Paper Cups.", quote_chunks,
        )
        add_uploaded_file(
            db, users["manager"].id, manager_session.id, "Northstar_Supplier_Quote.pdf", quote_path,
            "application/pdf", quote_text, "Sample supplier quote for document citation practice.", quote_chunks,
        )
        add_uploaded_file(
            db, users["admin"].id, None, "Northstar_Supplier_Quote.pdf", quote_path,
            "application/pdf", quote_text, "Sample supplier quote for admin procurement practice.", quote_chunks,
        )

        guide_text = "\n".join([
            "Inventory Operations Guide",
            "Arabica Coffee is stored at Central Warehouse and North Warehouse.",
            "The reorder level at Central Warehouse is 15 bags. The reorder level at North Warehouse is 12 bags.",
            "Oat Milk has a 3 day supplier lead time. Review its expiry date before using it.",
            "Managers prepare and confirm stock changes. Employees can view inventory but cannot change stock.",
            "Use the sales workbook to calculate average daily demand for matching products.",
        ])
        guide_chunks = [{"location": "page 1", "text": guide_text}]
        for user, session in [
            (users["manager"], manager_session),
            (users["employee"], employee_session),
            (users["admin"], admin_session),
        ]:
            add_uploaded_file(
                db, user.id, session.id, "Inventory_Operations_Guide.pdf", guide_path,
                "application/pdf", guide_text, "Sample guide for inventory questions and page citations.", guide_chunks,
            )
            db.add_all([
                ChatMessage(session_id=session.id, role="user", message="What does the operations guide say about coffee reorder levels?"),
                ChatMessage(session_id=session.id, role="assistant", message="The guide lists reorder levels for both warehouses. Ask a new question to see a page citation."),
            ])

        sales_text = "product_name units_sold date\nArabica Coffee 5 " + str(today - timedelta(days=6))
        sales_preview = {
            "sheets": [
                {"name": "Sales History", "rows": 14, "columns": ["product_name", "units_sold", "date"], "validation": {"errors": [], "warnings": []}},
                {"name": "Quality Checks", "rows": 4, "columns": ["item_code", "stock_count", "note", "Unnamed: 3"], "validation": {"errors": ["Unnamed columns: Unnamed: 3"], "warnings": ["1 duplicate rows found", "2 empty cells found", "1 negative numeric values found"]}},
            ],
            "source_chunks": [
                {"location": "sheet Sales History", "text": "Arabica Coffee: 34 units across 7 dates (5, 4, 6, 4, 5, 4, 6). Oat Milk: 20 units across 7 dates (3, 2, 4, 3, 2, 3, 3)."},
                {"location": "sheet Quality Checks", "text": "Duplicate rows, blank cells, and a negative stock count are included as validation examples."},
            ],
        }
        workbook_json = json.dumps(sales_preview)
        sales_chunks = sales_preview["source_chunks"]
        add_uploaded_file(
            db, users["manager"].id, None, "Northstar_Sales_History.xlsx", workbook_path,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", sales_text,
            "Seven days of sample sales history for Arabica Coffee and Oat Milk.", sales_chunks, workbook_json,
        )
        add_uploaded_file(
            db, users["manager"].id, manager_session.id, "Northstar_Sales_History.xlsx", workbook_path,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", sales_text,
            "Sales history for demand estimates.", sales_chunks, workbook_json,
        )
        add_uploaded_file(
            db, users["employee"].id, None, "Northstar_Sales_History.xlsx", workbook_path,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", sales_text,
            "Sample workbook. Sales history import is manager/admin only.", sales_chunks, workbook_json,
        )
        add_uploaded_file(
            db, users["admin"].id, None, "Northstar_Sales_History.xlsx", workbook_path,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", sales_text,
            "Sales history for demand estimates.", sales_chunks, workbook_json,
        )
        add_uploaded_file(
            db, users["admin"].id, admin_session.id, "Northstar_Sales_History.xlsx", workbook_path,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", sales_text,
            "Sales history for demand estimates.", sales_chunks, workbook_json,
        )

        supplier = Supplier(name="Northstar Food Supply", email="purchasing@northstar.example")
        db.add(supplier)
        db.flush()
        coffee_central = inventory[("Arabica Coffee", central.name)]
        db.add(PurchaseOrder(
            supplier_id=supplier.id,
            user_id=users["manager"].id,
            source_file_id=quote_file.id,
            inventory_id=coffee_central.id,
            quote_reference="DB-2026-1042",
            items_json=json.dumps([
                {"product_name": "Arabica Coffee", "quantity": 25, "unit_price": 13.5, "line_total": 337.5, "source_page": 1},
                {"product_name": "Paper Cups", "quantity": 1000, "unit_price": 0.04, "line_total": 40.0, "source_page": 1},
            ]),
            total_amount=377.5,
            recommended_quantity=20,
            status="draft",
        ))

        oat_inventory = inventory[("Oat Milk", central.name)]
        action_details = {
            "inventory_id": oat_inventory.id,
            "quantity_before": oat_inventory.quantity,
            "quantity_after": 8,
        }
        db.add(StockAction(
            user_id=users["manager"].id,
            action_type="set_quantity",
            request_text="Set Oat Milk at Central Warehouse to 8 units",
            generated_sql=f"UPDATE inventory SET quantity = 8 WHERE id = {oat_inventory.id}",
            details_json=json.dumps(action_details),
            status="pending",
        ))

        db.add_all([
            RecommendationOutcome(
                user_id=users["manager"].id,
                inventory_id=coffee_central.id,
                recommendation_type="transfer",
                recommended_quantity=10,
                actual_quantity=10,
                accepted=True,
                note="Transfer recommendation accepted.",
            ),
            RecommendationOutcome(
                user_id=users["manager"].id,
                inventory_id=oat_inventory.id,
                recommendation_type="reorder",
                recommended_quantity=18,
                actual_quantity=None,
                accepted=False,
                note="Reorder recommendation declined.",
            ),
        ])

        db.commit()
        print("Sample business data created.")
        print("Presentation account password was read from the environment.")
        for role, (email, _) in DEMO_USERS.items():
            print(f"{role}: {email}")
        print(f"Business documents: {os.path.abspath(DEMO_DIR)}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
