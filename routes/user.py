from fastapi import APIRouter
from models.user import User
from config.db import conn
from schemas.user import serializeDict, serializeList
from bson import ObjectId
from datetime import datetime

user = APIRouter()

@user.get('/login')
async def login(email, password):
    conn.local.user.find_one_and_update({"email": email, "password": password}, {
        "$set": {
            "updatedAt": datetime.today()
        }
    })

    user = conn.local.user.find_one({"email": email, "password": password})

    if user is not None:
        return serializeDict(user)
    else:
        return -1

@user.get('/')
async def find_all_users():
    return serializeList(conn.local.user.find())

@user.get('/{id}')
async def find_one_user(id):
    if len(id) != 24:
        return -1

    user = conn.local.user.find_one({"_id": ObjectId(id)})

    if user is not None:
        return serializeDict(user)
    else:
        return -1

@user.post('/')
async def create_user(user: User):
    conn.local.user.insert_one(dict(user))
    return serializeList(conn.local.user.find())

@user.put('/{id}')
async def update_user(id, user: User):
    if len(id) != 24:
        return -1

    conn.local.user.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })

    updatedUser = conn.local.user.find_one({"_id": ObjectId(id)})

    if updatedUser is not None:
        return serializeDict(updatedUser)
    else:
        return -1

@user.delete('/{id}')
async def delete_user(id):
    if len(id) != 24:
        return -1

    user = conn.local.user.find_one_and_delete({"_id": ObjectId(id)})