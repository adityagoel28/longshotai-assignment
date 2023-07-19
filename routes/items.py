from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from models.item import Item as Item
from config.db import item_collection as collection_name, space_collection, item_type_collection
from schema.items import individual_serial, list_serial
from bson import ObjectId
import datetime

router = APIRouter()

@router.get("/")
async def get_all_items():
    item = collection_name.find()
    return list_serial(item)

@router.get("/{id}")
async def get_an_item(id: str):
    try:
        # check if id exists in the database
        item = collection_name.find_one({"_id" :ObjectId(id)})
        if item is not None:
            return individual_serial(item)
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except:
        raise HTTPException(status_code=404, detail="Item not found")

@router.post("/")
async def create_an_item(item: Item):
    item_dict = item.dict()
    space = item_dict['space_assigned_name']
    space_name = space_collection.find_one({"name" :(space)})

    if (not space_name):
        raise HTTPException(status_code=400, detail="Space does not exist with the given name")
    
    expiry_date = item_dict['expiry_date']
    now = datetime.datetime.now(expiry_date.tzinfo)
    if(expiry_date < now):
        raise HTTPException(status_code=400, detail="Expiry date cannot be in the past")
    
    type_category = item_dict['item_type']
    type_name = type_category['name']
    item_type = item_type_collection.find_one({"name" :(type_name)})
    if (not item_type):
        raise HTTPException(status_code=400, detail="Item Type does not exist with the given name")
    
    item_name = item_dict['name']
    refrigeration = type_category['requires_refrigeration']
    if(refrigeration == True and space_name['is_refrigerated'] == False):
        raise HTTPException(status_code=400, detail="Space does not have refrigeration")
    
    result = collection_name.insert_one(item_dict)
    # new_todo = collection_name.find_one({"_id": todo.inserted_id})
    # return individual_serial(new_todo)

# Put request
@router.put("/{id}")
async def move_an_item(id: str, item: Item):
    item = item.dict()
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": item})
    updated_item = collection_name.find_one({"_id": ObjectId(id)})
    return individual_serial(updated_item)

# Delete request
@router.delete("/{id}")
# Deletion of an existing item type is possible only when there are no items linked to that type.
async def delete_a_space_by_id(id: str):
    item = collection_name.find_one({"_id" :ObjectId(id)})
    items = type['items']
    if len(items) > 0:
        raise HTTPException(status_code=400, detail="Deletion of a storage space is possible only when it is unoccupied i.e., devoid of any assigned items.")
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"message": "Space with id: {} deleted successfully".format(id)}