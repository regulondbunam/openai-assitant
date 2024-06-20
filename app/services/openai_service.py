import os
from dotenv import load_dotenv
from openai import OpenAI
from app.tools.pymongo_get_database import get_database

load_dotenv()
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI()
ASSISTANT_ID = os.environ['ASSISTANT_ID']

def get_messages(thread_id):
    """
    Retrieves and filters messages from a given thread ID.

    Args:
        thread_id (str): The ID of the thread to retrieve messages from. Defaults to TREAD_ID.

    Returns:
        list: A list of tuples containing filtered messages. Each tuple consists of a user message and the corresponding assistant message.
    """
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    ).model_dump()
    
    filtered_messages = []
    current_assistant_message = None

    # Iterar a través de los mensajes en orden inverso para encontrar el último mensaje de tipo 'assistant' para cada 'user'
    for message in messages['data']:
        if message['role'] == "assistant":
            if current_assistant_message is None or message['created_at'] > current_assistant_message['created_at']:
                current_assistant_message = message
        elif message['role'] == "user":
            if current_assistant_message is not None:
                filtered_messages.append((message, current_assistant_message))
                current_assistant_message = None   
    filtered_messages = filtered_messages[::-1] 
    return filtered_messages

def send_message(message, thread_id):
    """
    Sends a message to the OpenAI assistant and retrieves the final results.

    Args:
        message (str): The message to send to the assistant.
        thread_id (str, optional): The ID of the thread to send the message to. Defaults to TREAD_ID.

    Returns:
        str: The final results from the assistant.
    """
    thread_message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
        instructions="Por favor, dame solo los resultados finales sin explicaciones detalladas.",
    )
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        return messages.model_dump()
    else:
        return run.status
    
def evaluate_message(message_id, rating, comment, thread_id):
    """
    Updates the rating and comment for a specific message in a thread.

    Args:
        message_id (str): The ID of the message to be updated.
        rating (int): The rating to be assigned to the message.
        comment (str): The comment to be associated with the message.
        thread_id (str, optional): The ID of the thread containing the message. Defaults to TREAD_ID.

    Returns:
        str: The model dump of the updated message.
    """
    message = client.beta.threads.messages.update(
        message_id=message_id,
        thread_id=thread_id,
        metadata={
            "rating": rating,
            "userComment": comment,
        },
    )
    return message.model_dump()

def get_threads(username):
    """
    Retrieves the threads associated with a given username.

    Args:
        username (str): The username to retrieve threads for.

    Returns:
        list: A list of thread objects associated with the username.
    """
    dbname = get_database()
    user = dbname.users.find_one({"user": username})
    threads = user.get('threads', [])
    threads_obj = []
    if threads:
        for thread in threads:
            my_thread = client.beta.threads.retrieve(thread).model_dump()
            threads_obj.append(my_thread)
        threads = threads_obj
            
    return threads

def create_thread(username, prompt):
    """
    Creates a thread with the given username and prompt.

    Args:
        username (str): The username of the user creating the thread.
        prompt (str): The prompt for the thread.

    Returns:
        str: The ID of the created thread.
    """
    thread = client.beta.threads.create(
        metadata={"user": username, "name": prompt}
    )
    dbname = get_database()
    dbname.users.update_one({"user": username}, {"$push": {"threads": thread.id}})
    return thread.id

def delete_thread(username, thread_id):
    """
    Deletes a thread from the user's account.

    Args:
        username (str): The username of the user.
        thread_id (str): The ID of the thread to be deleted.

    Returns:
        bool: True if the thread is successfully deleted, False otherwise.
    """
    dbname = get_database()
    dbname.users.update_one({"user": username}, {"$pull": {"threads": thread_id}})
    client.beta.threads.delete(thread_id=thread_id)
    return True

def rename_thread(thread_id, name):
    """
    Renames a thread with the given thread_id to the specified name.

    Args:
        thread_id (str): The ID of the thread to be renamed.
        name (str): The new name for the thread.

    Returns:
        str: The model dump of the updated thread.
    """
    thread = client.beta.threads.update(
        thread_id=thread_id,
        metadata={"name": name}
    )
    return thread.model_dump()