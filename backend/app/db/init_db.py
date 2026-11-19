from app.db.database import Base, engine

from app.models.user import User
from app.models.chat import ChatMessage
from app.models.warehouse import Warehouse
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.stock_action import StockAction
from app.models.stock_movement import StockMovement
from app.models.stock_batch import StockBatch
from app.models.supplier import Supplier
from app.models.purchase_order import PurchaseOrder
from app.models.notification import Notification
from app.models.recommendation_outcome import RecommendationOutcome
from app.models.uploaded_file import UploadedFile
from app.models.sales_record import SalesRecord
from sqlalchemy import text

def init_db():
    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) NOT NULL DEFAULT 'employee'")
        )
        connection.execute(
            text("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS average_daily_demand FLOAT NOT NULL DEFAULT 0")
        )
        connection.execute(
            text("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS supplier_lead_time_days INTEGER NOT NULL DEFAULT 0")
        )
        connection.execute(
            text("ALTER TABLE uploaded_files ADD COLUMN IF NOT EXISTS source_chunks TEXT")
        )
        connection.execute(
            text("ALTER TABLE stock_actions ADD COLUMN IF NOT EXISTS reviewed_by_user_id INTEGER REFERENCES users(id)")
        )
        connection.execute(
            text("ALTER TABLE stock_actions ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP WITH TIME ZONE")
        )
        connection.execute(
            text("CREATE INDEX IF NOT EXISTS ix_inventory_product_warehouse ON inventory (product_id, warehouse_id)")
        )
        connection.execute(
            text("CREATE INDEX IF NOT EXISTS ix_stock_movements_created_id ON stock_movements (created_at, id)")
        )


if __name__ == "__main__":
    init_db()
