from flask import render_template, session, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm

from . import auth
from app.services.mongodb_service import get_user, put_user
from app.models import UserModel, UserData

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle the login functionality.

    This function renders the login form and handles the login process when the form is submitted.
    It validates the form data, checks if the user exists, and verifies the password.
    If the login is successful, it creates a user session and redirects to the chat_user page.
    If the login fails, appropriate flash messages are displayed.

    Returns:
        If the form is submitted and the login is successful, it redirects to the chat_user page.
        If the form is submitted and the login fails, it redirects to the index page.
        If the form is not submitted, it renders the login.html template with the login form.
    """
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        
        user_doc = get_user(username)
        
        if user_doc: 
            if check_password_hash(user_doc['password'], password):
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo')
                return redirect(url_for('chat_user'))
            else:
                flash('Contraseña incorrecta')
        else:
            flash('El usuario no existe')
            return redirect(url_for('index'))
            
    
    return render_template('login.html', **context)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    View function for the signup page.

    This function handles the GET and POST requests for the '/signup' route.
    It renders the signup.html template and processes the form data when the form is submitted.

    Returns:
        If the form data is valid and the user is successfully signed up, it redirects to the 'chat_user' route.
        Otherwise, it renders the signup.html template with the signup form.
    """
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        
        user_doc = get_user(username)
        
        if user_doc:
            flash('El usuario ya existe')
        else:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            put_user(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido')
            return redirect(url_for('chat_user'))
        
    return render_template('signup.html', **context)

@auth.route('/logout')
@login_required
def logout():
    """
    Log out the currently logged-in user.

    Returns:
        A redirect response to the login page.
    """
    logout_user()
    flash('Regresa pronto')
    
    return redirect(url_for('auth.login'))