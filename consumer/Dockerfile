# /consumer/Dockerfile

# Use the official Python image as a base
FROM python:3.11-slim

# Set the working directory in the container (you can customize this)
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh


RUN pip install --no-cache-dir flake8 pytest && \
    flake8 --extend-ignore=E501 .

# Expose the port that FastAPI will run on (if needed)
EXPOSE 8000

# Set the entrypoint to the script that waits for Kafka
ENTRYPOINT ["/app/entrypoint.sh"]
