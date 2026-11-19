import re
from datetime import date


ALLOWED_COLUMN = r"(?:id|warehouse_id|product_id|quantity|reorder_level|average_daily_demand)"
CONDITION = rf"{ALLOWED_COLUMN}\s*(?:<=|>=|!=|=|<|>)\s*(?:[0-9]+|{ALLOWED_COLUMN})"

DATE_FILTER = r"(?: WHERE sale_date >= '(\d{4}-\d{2}-\d{2})'(?: AND sale_date < '(\d{4}-\d{2}-\d{2})')?)?"

TOP_SALES_PATTERN = re.compile(
    rf"^SELECT product_id, SUM\(units_sold\) AS total_units_sold FROM sales_records{DATE_FILTER} GROUP BY product_id ORDER BY total_units_sold DESC LIMIT ([0-9]+)$",
    re.IGNORECASE,
)
TOTAL_SALES_PATTERN = re.compile(
    rf"^SELECT SUM\(units_sold\) AS total_units_sold FROM sales_records{DATE_FILTER}$",
    re.IGNORECASE,
)
SALES_TREND_PATTERN = re.compile(
    rf"^SELECT sale_date, SUM\(units_sold\) AS total_units_sold FROM sales_records{DATE_FILTER} GROUP BY sale_date ORDER BY sale_date ASC LIMIT ([0-9]+)$",
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

    for pattern in (TOP_SALES_PATTERN, TOTAL_SALES_PATTERN, SALES_TREND_PATTERN):
        sales_query = pattern.fullmatch(statement)
        if not sales_query:
            continue
        date_values = [value for value in sales_query.groups() if value and "-" in value]
        for date_value in date_values:
            try:
                date.fromisoformat(date_value)
            except ValueError as error:
                raise ValueError("Use a valid date in YYYY-MM-DD format.") from error
        limit = next((int(value) for value in reversed(sales_query.groups()) if value and value.isdigit()), None)
        if limit is not None and not 1 <= limit <= 100:
            raise ValueError("The result limit must be between 1 and 100.")
        return {"operation": "sales_analytics", "sql": statement}

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
        "Use a supported inventory query, a supported sales analysis, or set a stock quantity for one inventory ID."
    )
