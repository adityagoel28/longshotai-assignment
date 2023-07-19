from fastapi import FastAPI
# from routes.route import router
from pymongo.mongo_client import MongoClient
from routes.space_route import router as SpaceRouter
from routes.item_type_route import router as ItemTypeRouter
from routes.items import router as ItemRouter

app = FastAPI()

app.include_router(SpaceRouter, tags=["Space"], prefix="/space")
app.include_router(ItemTypeRouter, tags=["ItemType"], prefix="/itemtype")
app.include_router(ItemRouter, tags=["Item"], prefix="/item")
# app.include_router(router)