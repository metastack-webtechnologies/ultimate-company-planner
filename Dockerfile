# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for psycopg2 (PostgreSQL client library)
# These are necessary for psycopg2-binary to compile and run correctly
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
# --no-cache-dir prevents pip from storing cache, saving space
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose port 8000 for Django development server
EXPOSE 8000

# Command to run the Django development server
# 0.0.0.0 makes the server accessible from outside the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]