# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Instalar git
RUN apt-get update && apt-get install -y git

# Clonar el repositorio de GitHub
RUN git clone https://github.com/regulondbunam/openai-assitant.git .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]