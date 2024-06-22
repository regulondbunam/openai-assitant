from flask import render_template, session, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from app.forms import LoginForm
from . import auth
from app.services.auth_service import authenticate_user, register_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle the login functionality.

    Returns:
        If the form is submitted and the login is successful, it redirects to the chat_user page.
        If the form is submitted and the login fails, it redirects to the index page.
        If the form is not submitted, it renders the login.html template with the login form.
    """
    login_form = LoginForm()
    context = {'login_form': login_form}
    
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        try:
            user, error = authenticate_user(username, password)
            if user:
                login_user(user)
                flash('Bienvenido de nuevo')
                return redirect(url_for('chat_user'))
            else:
                flash(error)
                return redirect(url_for('index'))
        except Exception as e:
            flash('Ocurrió un error durante el inicio de sesión')
            print(f'Error: {str(e)}')
    
    return render_template('login.html', **context)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle the signup functionality.

    Returns:
        If the form data is valid and the user is successfully signed up, it redirects to the 'chat_user' route.
        Otherwise, it renders the signup.html template with the signup form.
    """
    signup_form = LoginForm()
    context = {'signup_form': signup_form}
    
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        try:
            user, error = register_user(username, password)
            if user:
                login_user(user)
                flash('Bienvenido')
                return redirect(url_for('chat_user'))
            else:
                flash(error)
        except Exception as e:
            flash('Ocurrió un error durante el registro')
            print(f'Error: {str(e)}')
    
    return render_template('signup.html', **context)

@auth.route('/logout')
@login_required
def logout():
    """
    Log out the currently logged-in user.

    Returns:
        A redirect response to the login page.
    """
    try:
        logout_user()
        flash('Regresa pronto')
    except Exception as e:
        flash('Ocurrió un error durante la salida')
        print(f'Error: {str(e)}')
    
    return redirect(url_for('auth.login'))