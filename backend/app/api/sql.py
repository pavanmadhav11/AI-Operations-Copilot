from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.schemas.sql import SQLRequest

from app.services.sql_service import (
    generate_sql,
    execute_sql,
)
from app.services.stock_action_service import create_quantity_action

router = APIRouter(
    prefix="/sql",
    tags=["SQL"],
)


@router.post("")
def sql(
    request: SQLRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:

        sql_query = generate_sql(
            question=request.question,
            role=current_user.role,
            db=db,
        )

        result = execute_sql(
            db=db,
            sql=sql_query,
            role=current_user.role,
        )

        if isinstance(result, dict) and result.get("operation") == "update":
            preview = create_quantity_action(
                db=db,
                user_id=current_user.id,
                request_text=request.question,
                sql=sql_query,
                inventory_id=result["inventory_id"],
                quantity=result["quantity"],
            )
            return {
                "success": True,
                "sql": sql_query,
                "confirmation_required": True,
                "result": preview,
            }

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

    except HTTPException:
        raise

    except Exception:

        return {
            "success": False,
            "message": "Sorry, I couldn't generate a valid SQL query. Please try rephrasing your request.",
        }
