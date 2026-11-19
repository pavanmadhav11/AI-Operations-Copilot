import re


ALLOWED_COLUMN = r"(?:id|warehouse_id|product_id|quantity|reorder_level|average_daily_demand)"
CONDITION = rf"{ALLOWED_COLUMN}\s*(?:<=|>=|!=|=|<|>)\s*(?:[0-9]+|{ALLOWED_COLUMN})"

TOP_DEMAND_PATTERN = re.compile(
    r"^SELECT product_id, SUM\(average_daily_demand\) AS average_daily_demand FROM inventory GROUP BY product_id ORDER BY average_daily_demand DESC LIMIT ([0-9]+)$",
    re.IGNORECASE,
)

SELECT_PATTERN = re.compile(
    rf"^SELECT\s+(?P<columns>\*|{ALLOWED_COLUMN}(?:\s*,\s*{ALLOWED_COLUMN})*)\s+FROM\s+inventory(?:\s+WHERE\s+{CONDITION}(?:\s+AND\s+{CONDITION})*)?(?:\s+ORDER\s+BY\s+{ALLOWED_COLUMN}(?:\s+(?:ASC|DESC))?)?(?:\s+LIMIT\s+[0-9]+)?$",
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

    top_demand = TOP_DEMAND_PATTERN.fullmatch(statement)
    if top_demand:
        limit = int(top_demand.group(1))
        if limit < 1 or limit > 100:
            raise ValueError("The result limit must be between 1 and 100.")
        return {"operation": "top_demand", "limit": limit}

    select = SELECT_PATTERN.fullmatch(statement)
    if select:
        columns = select.group("columns")
        if columns != "*" and "id" not in {column.strip().lower() for column in columns.split(",")}:
            raise ValueError("Include the inventory ID so product and warehouse names can be shown.")
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
