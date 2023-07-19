from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from models.space import Spaces
from config.db import space_collection as collection_name
from schema.space_schema import individual_serial, list_serial
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_all_spaces():
    spaces = collection_name.find()
    return list_serial(spaces)

@router.get("/{id}")
async def get_a_space(id: str): # this id means do we need to pass in body or parameter or what?
    try:
        # check if id exists in the database
        space = collection_name.find_one({"_id" :ObjectId(id)})
        if space is not None:
            return individual_serial(space)
        else:
            raise HTTPException(status_code=404, detail="Space not found")
    except:
        raise HTTPException(status_code=404, detail="Space not found")

@router.post("/")
async def create_a_todo(space: Spaces):
    space_dict = space.dict()
    max_limit = space_dict['max_limit']
    items = len(space_dict['items'])
    if max_limit < items:
        raise HTTPException(status_code=400, detail="Max Limit is less than the number of items")
    # space = collection_name.insert_one(dict(space))
    result = collection_name.insert_one(space_dict)
    # new_todo = collection_name.find_one({"_id": todo.inserted_id})
    # return individual_serial(new_todo)

# Put request
@router.put("/{id}")
async def update_a_space_by_id(id: str, space: Spaces):
    space = space.dict()
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": space})
    updated_space = collection_name.find_one({"_id": ObjectId(id)})
    return individual_serial(updated_space)

# Delete request
@router.delete("/{id}")
async def delete_a_space_by_id(id: str):
    space = collection_name.find_one({"_id" :ObjectId(id)})
    items = space['items']
    if len(items) > 0:
        raise HTTPException(status_code=400, detail="Deletion of a storage space is possible only when it is unoccupied i.e., devoid of any assigned items.")
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"message": "Space with id: {} deleted successfully".format(id)}