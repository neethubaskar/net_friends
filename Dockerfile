# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the project
COPY . /code/

# Install psycopg2 (if not in requirements.txt)
RUN pip install psycopg2-binary

# Copy the wait-for-it script
COPY scripts/wait-for-it.sh /code/
RUN chmod +x /code/wait-for-it.sh

