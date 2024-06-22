from werkzeug.security import generate_password_hash, check_password_hash
from app.services.mongodb_service import get_user, put_user
from app.models import UserModel, UserData

def authenticate_user(username, password):
    """
    Authenticate a user by username and password.
    
    Args:
        username (str): The username of the user.
        password (str): The password of the user.
    
    Returns:
        UserModel: The authenticated user model if authentication is successful.
        str: An error message if authentication fails.
    """
    user_doc = get_user(username)
    
    if user_doc and check_password_hash(user_doc['password'], password):
        user_data = UserData(username, password)
        user = UserModel(user_data)
        return user, None
    elif user_doc:
        return None, "Contraseña incorrecta"
    else:
        return None, "El usuario no existe"

def register_user(username, password):
    """
    Register a new user.
    
    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.
    
    Returns:
        UserModel: The registered user model.
        str: An error message if registration fails.
    """
    user_doc = get_user(username)
    
    if user_doc:
        return None, "El usuario ya existe"
    
    password_hash = generate_password_hash(password)
    user_data = UserData(username, password_hash)
    put_user(user_data)
    return UserModel(user_data), None
