from pydantic import BaseModel


class DashboardStatsResponse(BaseModel):
    users: int
    documents: int
    aiRequests: int
    storage: str


class ActivityPoint(BaseModel):
    date: str
    requests: int


class RecentActivityItem(BaseModel):
    text: str


class RecentDocumentItem(BaseModel):
    id: int
    filename: str