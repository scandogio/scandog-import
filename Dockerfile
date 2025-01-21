# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /action

# Copy the current directory contents into the container at /action
COPY . /action

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir requests

# Make the import.py script executable
RUN chmod +x /action/import.py

# Set the entrypoint to run the import script
ENTRYPOINT ["python", "/action/import.py"]