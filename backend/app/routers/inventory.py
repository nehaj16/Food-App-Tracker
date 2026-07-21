#FASTAPI routes for adding an item event

from datetime import date, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
#joinedload help with eager loading (same query)
from sqlalchemy.orm import Session, joinedload

from app.database import get_db #session
from app.models import Ingredient, InventoryItem #SQL Alchemy ORM
from app.schemas import InventoryItemCreate, InventoryItemRead #API schemas

#routes under /inventory
router = APIRouter(prefix="/inventory", tags=["inventory"])

#Race-safe find-or-create for an ingredient by name.
#Normalizes the name and either returns the existing row or inserts a new one.
#Two simultaneous requests for the same new name will never both succeed —
#Postgres serializes them, one gets the RETURNING id, the other gets None.
def _get_or_create_ingredient(db: Session, raw_name: str) -> Ingredient:
    normalized = raw_name.strip().lower()

    #atomic insert 
    #If ingredient was new, insert succeeds, if there then conflict triggers
    #and does nothing
    stmt = (
        pg_insert(Ingredient)
        .values(name=normalized)
        .on_conflict_do_nothing(index_elements=["name"])
        .returning(Ingredient.id)
    )
    result = db.execute(stmt).scalar_one_or_none()

    #exists so fetch by name
    if result is None:
        ingredient = db.execute(
            select(Ingredient).where(Ingredient.name == normalized)
        ).scalar_one()
    else: #fetch by id after created
        ingredient = db.execute(
            select(Ingredient).where(Ingredient.id == result)
        ).scalar_one()

    return ingredient

#find or create the ingredient, decide expiry date, build item
@router.post("", response_model=InventoryItemRead, status_code=status.HTTP_201_CREATED)
def create_inventory_item(payload: InventoryItemCreate, db: Session = Depends(get_db)):
    #create new db row from ingredient or get ingredient object from table 
    ingredient = _get_or_create_ingredient(db, payload.name)

    #sets expiry date to user entry but if null then it checks ingredient field
    #FUTURE: add AI to update the db for expiry days automatically
    expiry = payload.expiry_date
    if expiry is None and ingredient.default_shelf_life_days is not None:
        expiry = date.today() + timedelta(days=ingredient.default_shelf_life_days)

    item = InventoryItem(
        ingredient_id=ingredient.id,
        custom_name=payload.custom_name,
        quantity=payload.quantity,
        unit=payload.unit.value,
        location=payload.location.value,
        expiry_date=expiry,
    )
    db.add(item)
    db.commit() #end transaction

    db.refresh(item) #reload row into item w/ timestamps 

    #Eager loading - one query with item.ingredient being queried beforehand
    #avoid N+1 problem when accessing ingredient
    item = db.execute(
        select(InventoryItem)
        .options(joinedload(InventoryItem.ingredient))
        .where(InventoryItem.id == item.id)
    ).scalar_one()

    return item

#DELETE request for item event
#actually a soft delete so it updated the row instead and changes is_deleted to True
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_inventory_item(item_id: UUID, db: Session = Depends(get_db)):
    item = db.get(InventoryItem, item_id)

    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    item.is_deleted = True
    db.commit()
    return None