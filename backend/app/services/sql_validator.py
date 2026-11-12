import re


ALLOWED_COLUMN = r"(?:id|warehouse_id|product_id|quantity|reorder_level)"

SELECT_PATTERN = re.compile(
    rf"^SELECT\s+(?:\*|{ALLOWED_COLUMN}(?:\s*,\s*{ALLOWED_COLUMN})*)\s+FROM\s+inventory(?:\s+WHERE\s+{ALLOWED_COLUMN}\s*(?:=|<|>|<=|>=|!=)\s*(?:[0-9]+|{ALLOWED_COLUMN}))?(?:\s+ORDER\s+BY\s+{ALLOWED_COLUMN}(?:\s+(?:ASC|DESC))?)?(?:\s+LIMIT\s+[0-9]+)?$",
    re.IGNORECASE,
)

UPDATE_PATTERN = re.compile(
    r"^UPDATE\s+inventory\s+SET\s+quantity\s*=\s*([0-9]+)\s+WHERE\s+id\s*=\s*([0-9]+)$",
    re.IGNORECASE,
)


def validate_sql(sql: str, role: str):
    statement = sql.strip().rstrip(";").strip()

    if not statement or ";" in statement or "--" in statement or "/*" in statement:
        raise ValueError("Only one simple SQL statement is allowed.")

    if SELECT_PATTERN.fullmatch(statement):
        return {"operation": "select", "sql": statement}

    update = UPDATE_PATTERN.fullmatch(statement)
    if update:
        if role not in {"admin", "manager"}:
            raise ValueError("Only managers and admins can change stock.")
        return {
            "operation": "update",
            "quantity": int(update.group(1)),
            "inventory_id": int(update.group(2)),
        }

    raise ValueError(
        "Use a SELECT from inventory, or set a stock quantity for one inventory ID."
    )
