from sqlalchemy import inspect
from sqlalchemy.orm import Session


def get_database_schema(db: Session):

    inspector = inspect(db.bind)

    schema = ""

    tables = inspector.get_table_names()

    for table in tables:

        schema += f"\nTable: {table}\n"

        columns = inspector.get_columns(table)

        for column in columns:

            schema += f"- {column['name']} ({column['type']})\n"

    return schema