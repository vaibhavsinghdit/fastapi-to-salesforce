# /producer/Dockerfile

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

# Expose the port that FastAPI will run on
EXPOSE 8000

RUN pip install --no-cache-dir flake8 pytest && \
    flake8 --extend-ignore=E501 .

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
