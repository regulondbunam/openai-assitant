from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .config import Config
from .auth import auth
from .models import UserModel

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(username):
    user = UserModel.query(username)
    if user is None:
        return None
    return user

def create_app():
    app = Flask(__name__)
    app.config.update(
        DEBUG=True,
        ENV='development'
    )
    booststrap = Bootstrap(app)
    app.config.from_object(Config)
    login_manager.init_app(app)
    app.register_blueprint(auth)
    
    return app