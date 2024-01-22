# Use an official Python runtime as a parent image
FROM python:3.8-alpine

RUN apk add --update build-base libffi-dev git bash 
RUN apk install dos2unix

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME World

RUN dos2unix run.sh
# Run scripts to launch the app
RUN bash run.sh