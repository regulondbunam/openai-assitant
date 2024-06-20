from flask import Flask , request, make_response, redirect, render_template, session, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
import requests
from app import create_app
from app.forms import MessageForm, EvaluationForm
from app.services.openai_service import get_messages, send_message, evaluate_message, get_threads, create_thread, delete_thread, rename_thread

app = create_app()

@app.errorhandler(404)
def not_found(error):
    """
    Error handler for 404 status code.

    Args:
        error: The error message.

    Returns:
        The rendered template for the 404.html page with the error message.
    """
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    """
    Error handler for internal server errors.

    Args:
        error: The error object representing the internal server error.

    Returns:
        The rendered template for the '500.html' error page.
    """
    return render_template('500.html')

@app.route('/')
def index():
    """
    This function is the handler for the root URL ('/').
    It redirects the user to the 'chat_ui' endpoint.
    """
    response = make_response(redirect(url_for('chat_user')))
    return response

@app.route('/leo', methods=['GET','POST'])
def api():
    """
    API endpoint for Leo chatbot.

    Parameters:
    - message: The message to send to the chatbot.
    - message_id: The ID of the message to evaluate.
    - comment: The comment for the evaluated message.
    - rating: The rating for the evaluated message.

    Returns:
    - If message is provided, returns the response from the chatbot.
    - If message_id, rating, and comment are provided, returns the evaluation response.
    """
    message = request.args.get('message')
    message_id = request.args.get('message_id')
    comment = request.args.get('comment')
    rating = request.args.get('rating')
    response = None
    
    if message:
        response = send_message(message)
    elif message_id and rating and comment:
        response = evaluate_message(message_id, str(rating), comment)
    
    return response
    
@app.route('/chatbot', methods=['GET','POST'])    
@login_required
def chat_user():
    """
    Renders the chat user chatbot page.

    This function handles the '/chatbot' route and is decorated with the 'login_required' decorator.
    It retrieves the current user's ID, initializes message and evaluation forms, and fetches the threads
    associated with the user. It also retrieves any stored messages from the session and determines if a
    new chat is requested or if a specific thread ID is provided. If a thread ID is provided, it retrieves
    the messages associated with that thread.

    Returns:
        The rendered 'chat_user.html' template with the necessary context variables.
    """
    username = current_user.id
    message_form = MessageForm()
    evaluation_form = EvaluationForm()
    threads = get_threads(username)
    messages = session.pop('messages', [])
    new_chat = request.args.get('new_chat') or False
    current_thread_id = request.args.get('thread_id') or ""
    if current_thread_id:
        messages = get_messages(current_thread_id)
    
    context = {
        'message_form': message_form,
        'evaluation_form': evaluation_form,
        'threads': threads,
        'username': username,
        'messages': messages,
        'new_chat': new_chat,
        'thread_id': current_thread_id
    }
    return render_template('chat_user.html', **context)

@app.route('/new_thread', methods=['POST'])
def new_thread():
    """
    Creates a new thread for the current user.

    Returns:
        A redirect to the 'chat_user' route.
    """
    username = current_user.id
    create_thread(username)
    return redirect(url_for('chat_user'))

@app.route('/thread', methods=['GET','POST'])
def view_thread():
    """
    View a thread and retrieve messages for the specified thread ID.

    Args:
        None

    Returns:
        Redirects to the 'chat_user' route with the specified thread ID.

    """
    thread_id = request.args.get('thread_id')
    if thread_id:
        messages = get_messages(thread_id)
        session['messages'] = messages
    return redirect(url_for('chat_user',thread_id=thread_id))
    
@app.route('/send_message', methods=['POST'])
def send_message_thread():
    """
    Sends a message in a thread.

    This function is called when a POST request is made to the '/send_message' endpoint.
    It retrieves the username, thread ID, and message from the request.
    If a thread ID is provided, it sends the message in the existing thread.
    Otherwise, it creates a new thread and sends the message in that thread.
    Finally, it redirects the user to the 'view_thread' endpoint with the thread ID.

    Returns:
        A redirect response to the 'view_thread' endpoint with the thread ID.
    """
    username = current_user.id
    thread_id = request.args.get('thread_id')
    message = request.form['prompt']
    if thread_id:
        send_message(message, thread_id)
    else:
        thread_id = create_thread(username, message)
        send_message(message, thread_id)

    return redirect(url_for('view_thread', thread_id=thread_id))

@app.route('/select_prompt', methods=['POST'])
def select_prompt():
    """
    Handles the POST request to select a prompt.

    Retrieves the username and prompt from the request form.
    Creates a thread with the username and prompt.
    Sends a message with the prompt to the created thread.
    Redirects the user to the view_thread page for the created thread.

    Returns:
        A redirect response to the view_thread page for the created thread.
    """
    username = current_user.id
    prompt = request.form['prompt']

    thread_id = create_thread(username, prompt)
    send_message(prompt, thread_id)
    
    return redirect(url_for('view_thread',thread_id=thread_id))

@app.route('/threads/<thread_id>/rename', methods=['POST'])
def rename_thread_route(thread_id):
    """
    Renames a thread with the given thread_id.

    Args:
        thread_id (str): The ID of the thread to be renamed.

    Returns:
        dict: A dictionary containing the status and message of the operation.
            - status (str): The status of the operation ('success' or 'error').
            - message (str): A message indicating the result of the operation.
    """
    new_name = request.json.get('new_name')
    rename_thread(thread_id, new_name)
    return jsonify({'status': 'success', 'message': 'Thread renamed successfully'})

@app.route('/threads/<thread_id>/delete', methods=['GET','DELETE'])
def delete_thread_route(thread_id):
    """
    Delete a thread based on the provided thread_id.

    Args:
        thread_id (str): The ID of the thread to be deleted.

    Returns:
        redirect: A redirect response to the 'chat_user' route.
    """
    username = current_user.id
    response = delete_thread(username, thread_id)
    return redirect(url_for('chat_user'))

if __name__ == '__main__':
    app.run()
    
# flask run
# set FLASK_APP=main.py
# set FLASK_DEBUG=1
# set FLASK_ENV=development