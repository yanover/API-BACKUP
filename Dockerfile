# syntax=docker/dockerfile:1
# Install Python image
FROM python:3.8-slim-buster
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
# Tell docker commands to run on start
CMD [ "python3", "app.py"] 
 