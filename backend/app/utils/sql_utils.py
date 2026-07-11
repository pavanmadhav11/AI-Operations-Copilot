import re


def clean_sql(sql: str):

    sql = sql.replace("```sql", "")

    sql = sql.replace("```", "")

    sql = sql.strip()

    sql = re.sub(r";+$", ";", sql)

    return sql