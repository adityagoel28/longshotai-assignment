from pydantic import BaseModel, Field
from typing import Optional, List
from models.item import Item

class Spaces(BaseModel):
    name: str
    max_limit: int
    is_refrigerated: bool
    items: Optional[List[Item]]

# class Space(Spaces):
#     id: Optional[str] = None