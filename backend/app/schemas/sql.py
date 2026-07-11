from pydantic import BaseModel


class SQLRequest(BaseModel):
    question: str


class SQLResponse(BaseModel):
    sql: str
    result: list