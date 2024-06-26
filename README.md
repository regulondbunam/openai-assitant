# openAI assistant Manual

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
- [Docker](https://docs.docker.com/engine/install) 

## Installation

**Step 1 download project**
You need to download this repository, in its master branch,

```shell
git clone https://github.com/regulondbunam/openai-assitant.git
cd openai-assitant
```

You can also download the zip file from the repository and unzip it to a designated location

**Step 2 configuration**

At the root folder, you will find the .env file where you will find the information to declare the environment variables so that the application can connect to OpenAI.

Fill the .env file adding the information requested in the .env file.

``` 
# OPENAI_API_KEY = "API KEY of OpenAI"
# ASSISTANT_ID = "your assistant ID of openAI"

OPENAI_API_KEY=<your_openai_api_key>
ASSISTANT_ID=<your_assistant_id_of_openai>
```
or you can fill the file .env with the next commands but first change the value of the vars:
```shell
echo "OPENAI_API_KEY=<your_openai_api_key>" >> .env
echo "ASSISTANT_ID=<your_assistant_id_of_openai>" >> .env
``` 

**Step 3 start service**

1. Run the Flask application:

On linux:
```shell
sudo docker compose up -d --build
```
On windows:
```shell
sudo docker-compose up -d --build
```
The -d in the command sudo docker compose up -d --build stands for "detached mode," which runs the containers in the background.

2. Access the application by navigating to http://0.0.0.0 in your web browser.
if not working, you must put your IPv4 Address, to know your Ip, run the next command:

On linux:
```shell
ip addr
```
On windows:
```shell
ipconfig
```

3. To view the logs:

On linux:
```shell
sudo docker compose logs -f
```
On windows:
```shell
sudo docker-compose logs -f
```

if you can view the logs of a specific container, you only have to put the container's name after of the preview command