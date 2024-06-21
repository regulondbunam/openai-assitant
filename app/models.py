from flask_login import UserMixin

from .services.mongodb_service import get_user

class UserData:
    """
    Represents user data with a username and password.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
class UserModel(UserMixin):
    def __init__(self, user_data):
        """
        Args:
            user_data (UserData): A class that contains the username and password of the user.
        """
        self.id = user_data.username
        self.password = user_data.password
        
    @staticmethod
    def query(user_id):
        """
        Args:
            user_id (str): The username of the user.
        """
        user_doc = get_user(user_id)
        user_data = UserData(
            username=user_doc.get("user"), 
            password=user_doc.get("password"))
        return UserModel(user_data)