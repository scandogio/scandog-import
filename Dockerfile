# Use a more secure Python runtime as a parent image
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /action

# Copy the current directory contents into the container at /action
COPY . /action

# Install security updates and clean up
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Make the import.py script executable
RUN chmod +x /action/import.py

# Set the entrypoint to run the import script
ENTRYPOINT ["python", "/action/import.py"]