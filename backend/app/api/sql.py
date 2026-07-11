from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.sql import SQLRequest

from app.services.sql_service import (
    generate_sql,
    execute_sql,
)

router = APIRouter(
    prefix="/sql",
    tags=["SQL"],
)


@router.post("")
def sql(
    request: SQLRequest,
    db: Session = Depends(get_db),
):
    try:

        sql_query = generate_sql(
            db=db,
            question=request.question,
        )

        result = execute_sql(
            db=db,
            sql=sql_query,
        )

        return {
            "success": True,
            "sql": sql_query,
            "result": result,
        }

    except ValueError as e:

        return {
            "success": False,
            "message": str(e),
        }

    except Exception:

        return {
            "success": False,
            "message": "Sorry, I couldn't generate a valid SQL query. Please try rephrasing your request.",
        }