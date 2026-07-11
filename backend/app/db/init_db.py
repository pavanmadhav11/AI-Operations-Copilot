from app.db.database import Base, engine

from app.models.user import User
from app.models.chat import ChatMessage
from app.models.warehouse import Warehouse
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.shipment import Shipment

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()