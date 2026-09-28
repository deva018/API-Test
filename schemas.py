from sqlmodel import SQLModel
from models import ItemStatus


class ItemCreate(SQLModel):
    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: ItemStatus


class ItemUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    location: str | None = None
    reported_by: str | None = None
    status: ItemStatus | None = None