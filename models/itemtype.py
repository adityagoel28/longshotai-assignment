from pydantic import BaseModel, Field
from typing import Optional, List

class ItemType(BaseModel):
    name: str
    requires_refrigeration: bool