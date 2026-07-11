FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "GRANT",
    "REVOKE",
    "MERGE",
]


def validate_sql(sql: str):

    sql = sql.strip()

    if sql == "NOT_POSSIBLE":
        raise ValueError(
            "The request cannot be answered with a read-only SQL query."
        )

    sql_upper = sql.upper()

    if not sql_upper.startswith("SELECT"):
        raise ValueError(
            "Only SELECT statements are allowed."
        )

    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in sql_upper:

            raise ValueError(
                f"Unsafe SQL detected: {keyword}"
            )

    return True