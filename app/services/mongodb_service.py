from app.tools.get_database import get_database

def get_users():
    """
    Retrieve all users from the collection.

    Returns:
        A cursor object containing all the users in the collection.
    """
    try:
        db = get_database()
        return db.users.find()
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
    db = get_database()
    user_doc = db.users.find_one({"user": user_id})
    if user_doc is None:
        print(f"No user found for user_id: {user_id}")
    return user_doc

def put_user(user_data):
    """
    Inserts a user into the collection.

    Args:
        user_data (dict): A dictionary containing user data, including username and password.

    Returns:
        None
    """        
    try:
        db = get_database()
        return db.users.insert_one({"user": user_data.username, "password": user_data.password})

    except Exception as e:
        print(f"An error occurred while inserting user: {e}")

