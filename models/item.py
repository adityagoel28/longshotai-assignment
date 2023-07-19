from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from models.itemtype import ItemType

class Item(BaseModel):
    name: str
    expiry_date: Optional[datetime]
    space_assigned_name: str
    item_type: ItemType = Field(...)