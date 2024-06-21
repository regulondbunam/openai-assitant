from app.tools.get_database import get_database
from bson import ObjectId
                          
db = get_database()
collection = db.users

def get_users():
    """
    Retrieve all users from the collection.

    Returns:
        A cursor object containing all the users in the collection.
    """
    return collection.find()

def get_user(user_id):
    """
    Retrieve a user from the collection based on the user ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        dict: A dictionary representing the user document from the collection.
              Returns None if no user is found with the given ID.
    """
    return collection.find_one({'user': user_id})

def put_user(user_data):
    """
    Inserts a user into the collection.

    Args:
        user_data (dict): A dictionary containing user data, including username and password.

    Returns:
        None
    """
    collection.insert_one({"user": user_data.username, "password": user_data.password})