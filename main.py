from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, select

from database import engine
from models import Item, ItemStatus
from schemas import ItemCreate, ItemUpdate


app = FastAPI(title="College Lost & Found API")


# Create database table when application starts
@app.on_event("startup")
def create_tables():
    SQLModel.metadata.create_all(engine)


# Home
@app.get("/")
def home():
    return {"message": "Lost & Found API is working"}


# 1. CREATE ITEM
@app.post("/items", response_model=Item)
def create_item(item: ItemCreate):

    with Session(engine) as session:

        db_item = Item(**item.model_dump())

        session.add(db_item)
        session.commit()
        session.refresh(db_item)

        return db_item


# 2. GET ALL ITEMS
@app.get("/items", response_model=list[Item])
def get_items():

    with Session(engine) as session:

        items = session.exec(select(Item)).all()

        return items


# 3. GET ITEMS BY STATUS
@app.get("/items/status/{status}", response_model=list[Item])
def get_items_by_status(status: ItemStatus):

    with Session(engine) as session:

        statement = select(Item).where(Item.status == status)

        items = session.exec(statement).all()

        return items


# 4. GET ITEMS BY CATEGORY
@app.get("/items/category/{category}", response_model=list[Item])
def get_items_by_category(category: str):

    with Session(engine) as session:

        statement = select(Item).where(Item.category == category)

        items = session.exec(statement).all()

        return items


# 5. GET ITEM BY ID
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):

    with Session(engine) as session:

        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        return item


# 6. UPDATE ITEM
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_data: ItemUpdate):

    with Session(engine) as session:

        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        update_data = item_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(item, key, value)

        session.add(item)
        session.commit()
        session.refresh(item)

        return item


# 7. DELETE ITEM
@app.delete("/items/{item_id}")
def delete_item(item_id: int):

    with Session(engine) as session:

        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        session.delete(item)
        session.commit()

        return {
            "message": "Item deleted successfully"
        }