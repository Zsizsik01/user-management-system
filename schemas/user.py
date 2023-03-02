def serializeDict(item) -> dict:
    return {
        'id':str(item['_id']),
        'name':item['name'],
        'email':item['email'],
        'password':item['password'],
        'updatedAt':item['updatedAt']
    }

def serializeList(entity) -> list:
    return [serializeDict(item) for item in entity]
