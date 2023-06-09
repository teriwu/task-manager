from fastapi import FastAPI, HTTPException
from models import Item
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

from database import (
  fetch_all_items,
  fetch_item,
  post_item,
  put_item,
  delete_item,
)

# allows access to db after setting up middleware cors
origins = ["http://localhost:3000"]

# similar to django's settings.py
app.add_middleware(
  CORSMiddleware,
  allow_origins= origins,
  allow_credentials= True,
  allow_methods= ["*"],
  allow_headers= ["*"],
)

"""CRUD
GET
POST
PUT
DELETE"""

@app.get ("/")
async def read_root():
  return {"hello": "world"}

@app.get ("/items")
async def get_items():
  response = await fetch_all_items()
  # if response:
  return response
  # raise HTTPException("404 no items")

@app.get ("/items/{title}", response_model=Item)
async def get_item(title):
  response = await fetch_item(title)
  if response:
    return response
  raise HTTPException(404, "404 no items")

@app.post ("/items", response_model=Item)
async def create_item(item:Item): # Makes sure the input is a type of class to specify the structure of Item
  response = await post_item(item.dict())
  if response:
    return response
  raise HTTPException(404, "404 no items")

@app.put ("/items/{title}", response_model=Item)
async def update_item(title, description):
  response = await put_item(title, description)
  if response:
    return response
  raise HTTPException(404, "404 no items")

# @app.delete ("/items/{id}")
# async def delete_item():
#   response = await # delete_item()
#   if response:
#     return response
#   raise HTTPException("404 no items")

@app.delete ("/items/{title}", response_model=Item)
async def remove_item(title):
  response = await delete_item(title)
  if response: 
    return response
  raise HTTPException(404, "Item does not exist")