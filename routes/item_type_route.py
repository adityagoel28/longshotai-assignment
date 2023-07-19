from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from models.itemtype import ItemType as ItemTypes
from config.db import item_type_collection as collection_name
from schema.item_type import individual_serial, list_serial
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_all_types():
    types = collection_name.find()
    return list_serial(types)

@router.get("/{id}")
async def get_a_type(id: str): # this id means do we need to pass in body or parameter or what?
    try:
        # check if id exists in the database
        type = collection_name.find_one({"_id" :ObjectId(id)})
        if type is not None:
            return individual_serial(type)
        else:
            raise HTTPException(status_code=404, detail="Item Type not found")
    except:
        raise HTTPException(status_code=404, detail="Item Type not found")

@router.post("/")
async def create_a_type(type: ItemTypes):
    type_dict = type.dict()
    # space = collection_name.insert_one(dict(space))
    result = collection_name.insert_one(type_dict)
    # new_todo = collection_name.find_one({"_id": todo.inserted_id})
    # return individual_serial(new_todo)

# Put request
@router.put("/{id}")
async def update_a_space_by_id(id: str, type: ItemTypes):
    type = type.dict()
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": type})
    updated_type = collection_name.find_one({"_id": ObjectId(id)})
    return individual_serial(updated_type)

# Delete request
@router.delete("/{id}")
# Deletion of an existing item type is possible only when there are no items linked to that type.
async def delete_a_space_by_id(id: str):
    type = collection_name.find_one({"_id" :ObjectId(id)})
    items = type['items']
    if len(items) > 0:
        raise HTTPException(status_code=400, detail="Deletion of a storage space is possible only when it is unoccupied i.e., devoid of any assigned items.")
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"message": "Space with id: {} deleted successfully".format(id)}