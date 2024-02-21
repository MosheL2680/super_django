# Use the official Python image as a base image
FROM python:3.10-alpine AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file separately to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . /app/

# Expose the port on which the Django development server will run
EXPOSE 8000

# Specify the command to run on container start
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
