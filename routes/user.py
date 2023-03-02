from fastapi import APIRouter
from models.user import User
from config.db import conn
from schemas.user import serializeDict, serializeList
from bson import ObjectId
from datetime import datetime
import bcrypt

user = APIRouter()

@user.get('/login')
async def login(email, password):
    '''
    This function logs in the user with the provided email and password.
    :param email: Email address of the user.
    :param password: Password of the user.
    :return: With error message if the email or the password is incorrect. With success message if the login was successful.
    '''

    bytes = password.encode('utf-8')

    user = conn.local.user.find_one({'email': email})

    if user is None:
        return 'The email is incorrect!'

    if bcrypt.checkpw(bytes, serializeDict(user)['password']):
        conn.local.user.find_one_and_update({'email': email}, {
            '$set': {
                'updatedAt': datetime.today()
            }
        })

        return 'Login was successful!'

    return 'The password is incorrect!'

@user.get('/')
async def find_all_users():
    '''
    This function lists all existing users.
    :return: With the list of users.
    '''

    return serializeList(conn.local.user.find())

@user.get('/{id}')
async def find_one_user(id):
    '''
    This function gets a selected user by id.
    :param id: The ID of the selected user.
    :return: With the selected user. With error message if the ID is not valid or the user with the ID does not exist.
    '''

    if ObjectId.is_valid(id) == False:
        return 'Object ID is not valid!'

    user = conn.local.user.find_one({'_id': ObjectId(id)})

    if user is not None:
        return serializeDict(user)
    else:
        return 'User not found!'

@user.post('/')
async def create_user(user: User):
    '''
    This function creates a new user.
    :param user: A user object which contains name, email, password and updatedAt data.
    :return: With the newly created user. With error message if there is already a user with this email address.
    '''

    bytes = user.password.encode('utf-8')
    user.password = bcrypt.hashpw(bytes, bcrypt.gensalt())

    userFromDatabase = conn.local.user.find_one({'email': user.email})

    if userFromDatabase is not None:
        return 'There is already a user with this email address!'

    conn.local.user.insert_one(dict(user))

    return serializeList(conn.local.user.find())

@user.put('/{id}')
async def update_user(id, user: User):
    '''
    This function updates the selected user.
    :param id: The ID of the selected user.
    :param user: A user object which contains name, email, password and updatedAt data.
    :return: With the updated user. With error message if the ID is not valid or the user is not found with the selected ID.
    '''

    if ObjectId.is_valid(id) == False:
        return 'Object ID is not valid!'

    bytes = user.password.encode('utf-8')
    user.password = bcrypt.hashpw(bytes, bcrypt.gensalt())

    del user.updatedAt

    conn.local.user.find_one_and_update({'_id': ObjectId(id)}, {
        '$set': dict(user)
    })

    updatedUser = conn.local.user.find_one({'_id': ObjectId(id)})

    if updatedUser is not None:
        return serializeDict(updatedUser)
    else:
        return 'User not found!'

@user.delete('/{id}')
async def delete_user(id):
    '''
    This function deletes a selected user.
    :param id: The ID of the selected user.
    :return: With success message. With error message if the ID is not valid or the user is not found with the selected ID.
    '''

    if ObjectId.is_valid(id) == False:
        return 'Object ID is not valid!'

    user = conn.local.user.find_one({'_id': ObjectId(id)})

    if user is None:
        return 'User does not exist!'

    conn.local.user.find_one_and_delete({'_id': ObjectId(id)})

    return 'The deletion was successful!'