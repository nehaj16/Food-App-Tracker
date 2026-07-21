#models.py defines classes that mirror sql database
#SQL Alchemy used to translate Python to SQL db (quality of life)

#Actual db schema in db folder in backend

import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID #get pg uuid
from sqlalchemy.orm import relationship #ORM tool to avoid joins

from app.database import Base

#Model for Ingredient DB
class Ingredient(Base):
    __tablename__ = "ingredients"
    #have uuid provided in Python as safety
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    default_shelf_life_days = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    inventory_items = relationship("InventoryItem", back_populates="ingredient")
    #get list of inventory Item objects


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id"), nullable=False)
    custom_name = Column(String, nullable=True)
    quantity = Column(Numeric(10, 2), nullable=False)
    unit = Column(String, nullable=False)
    location = Column(String, nullable=False, server_default="fridge")
    expiry_date = Column(Date, nullable=True)
    is_deleted = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    #get ingredient name
    ingredient = relationship("Ingredient", back_populates="inventory_items")
    
    #GENERAL constraints/table rules - can grow later
    #check constraint for units for here
    __table_args__ = (
        CheckConstraint(
            "unit IN ('g','kg','lb','oz','ml','l','fl_oz','gal',"
            "'count','dozen','bag','box','can','bottle','pack')",
            name="inventory_items_unit_check",
        ),
    )