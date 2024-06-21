from app.tools.get_database import get_database

db = get_database()
collection = db.users

def get_users():
    """
    Retrieve all users from the collection.

    Returns:
        A cursor object containing all the users in the collection.
    """
    try:
        return collection.find()
    except Exception as e:
        print(f"An error occurred while retrieving users: {e}")
        return None

def get_user(user_id):
    """
    Retrieve a user from the collection based on the user ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        dict: A dictionary representing the user document from the collection.
              Returns None if no user is found with the given ID.
    """
    try:
        return collection.find_one({'user': user_id})
    except Exception as e:
        print(f"An error occurred while retrieving user: {e}")
        return None

def put_user(user_data):
    """
    Inserts a user into the collection.

    Args:
        user_data (dict): A dictionary containing user data, including username and password.

    Returns:
        None
    """        
    try:
        collection.insert_one({"user": user_data.username, "password": user_data.password})

    except Exception as e:
        print(f"An error occurred while inserting user: {e}")

