# syntax=docker/dockerfile:1
# Install Python image
FROM python:3.11.0a5-bullseye
# Create a directory inside the container
WORKDIR /app
# Copy package dependecies declarations
COPY requirements.txt requirements.txt
# Install dependencies inside the container
RUN pip3 install -r requirements.txt
# Add the source code inside our container
COPY src .
# Set FLASK APP
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=127.0.0.1
# Expose container port
EXPOSE 3000
# Tell docker commands to run on start
CMD [ "python3", "app.py"] 
 