from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.schema_service import get_database_schema
from app.ai.llm import ask_llm
from app.ai.sql_prompt import SQL_SYSTEM_PROMPT
from app.services.sql_validator import validate_sql
from app.utils.sql_utils import clean_sql


def generate_sql(
    db: Session,
    question: str,
):

    schema = get_database_schema(db)


    messages = [
        {
            "role": "system",
            "content": SQL_SYSTEM_PROMPT,
        },
        {
            "role": "system",
            "content": f"Database Schema:\n\n{schema}",
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    sql = ask_llm(messages)
    sql = clean_sql(sql)

    sql = sql.strip()

    validate_sql(sql)

    return sql


def execute_sql(
    db: Session,
    sql: str,
):

    result = db.execute(text(sql))

    rows = result.mappings().all()

    return [dict(row) for row in rows]