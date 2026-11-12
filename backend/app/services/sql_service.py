from sqlalchemy import text
from sqlalchemy.orm import Session

from app.ai.llm import ask_llm
from app.ai.sql_prompt import SQL_SYSTEM_PROMPT
from app.services.sql_validator import validate_sql
from app.utils.sql_utils import clean_sql


def generate_sql(
    question: str,
    role: str,
):

    messages = [
        {
            "role": "system",
            "content": SQL_SYSTEM_PROMPT + (
                " This manager or admin may use SELECT or the exact single-row quantity UPDATE format."
                if role in {"admin", "manager"}
                else " This employee can only use SELECT statements."
            ),
        },
        {
            "role": "system",
            "content": "Inventory columns: id, warehouse_id, product_id, quantity, reorder_level.",
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    sql = ask_llm(messages)
    sql = clean_sql(sql)

    sql = sql.strip()

    validate_sql(sql, role)

    return sql


def execute_sql(
    db: Session,
    sql: str,
    role: str,
):
    query = validate_sql(sql, role)

    if query["operation"] == "update":
        return query

    result = db.execute(text(query["sql"]))
    return [dict(row) for row in result.mappings().all()]
