from sqlmodel import SQLModel,Field
from enum import Enum

class ItemStatus(str, Enum):
    Lost ="Lost"
    Found ="Found"
    Returned ="Returned"

class Item(SQLModel,table=True):
    id:int | None = Field(default=None,primary_key=True)


    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: ItemStatus