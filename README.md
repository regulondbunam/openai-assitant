# Make Phrases Manual

welcome n.n/
version 0.1.0

## Description
This manual provides comprehensive instructions for the installation, configuration, and maintenance of the chatbot web application developed using Flask, HTML, and CSS. The application allows users to interact with a chatbot, either without logging in or by creating an account. Users can start new chats, rate the chatbot's responses, and manage their chat history.

## Hardware requirements

### Client
- Any modern computer or device capable of running a web browser.
- Minimum 2 GB of RAM.
- Minimum 1 GHz processor.

### Server
- A server with at least 4 GB of RAM.
- At least 2 GHz dual-core processor.
- Minimum 20 GB of free disk space.

## Software Requirements

### server:
- Operating System: Linux (Ubuntu 18.04+ recommended), Windows 10+, or macOS 10.14+.
- Python 3.9 or higher.
- A web server like Nginx or Apache (optional, for production deployment).
- MongoDB for database services.

## Installation

**Step 1 download project**
You need to download this repository, in its master branch,

```shell
git clone https://github.com/regulondbunam/regulondb-gpt.git
cd regulondb-gpt/openai_assistant
```

You can also download the zip file from the repository and unzip it to a designated location

**Step 2 install venv**
1. install venv python library
```shell
sudo apt install python3-venv
```
on Windows
```sell
pip install virtualenv
```

2. Creates the virtual runtime environment
```shell
python3 -m venv venv
```
on Windows
```shell
virtualenv venv

```

**Step 3 activate venv**
1. Activate the virtual environment:
- On macOS/Linux:
```shell
. venv/bin/activate
```

- On Windows:
```shell
./venv/Scripts/activate
```
On windows you need to modify about_Execution_Policies to allow the execution of the venv script, visit https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2.
for more information

**Step 4 install project dependencies**

```shell
pip install -r requirements.txt
```

**Step 5 configuration**

At the **app** folder, you will find the .envExample file where you will find the information to declare the environment variables so that the application can connect to mongoDB and OpenAI.

duplicate the .envEXAMPLE file and rename it to .env and add the information requested in the .envExample file.

``` 
#rename this file to '.env' when the fields have been filled
# OPENAI_API_KEY = "API KEY of OpenAI"

OPENAI_API_KEY=your_openai_api_key
MONGODB_CONNECTION_URI=your_mongodb_connection_uri
DATABASE_NAME=your_database_name
ASSISTANT_ID=your_assistant_id_of_openai
```


**Step 6 start service**

1. Run the Flask application:
```shell
gunicorn --bind 0.0.0.0:8000 wsgi:app
```
2. Access the application by navigating to http://127.0.0.1:5000 in your web browser.

Note: For production deployment, it is recommended to use a production-ready web server like Nginx or Apache and configure it to serve the Flask application using a WSGI server like Gunicorn. Additionally, secure the application using HTTPS.