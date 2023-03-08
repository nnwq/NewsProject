# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /NewsProject

# Copy the current directory contents into the container at /app
COPY . /NewsProject

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Port the Django app will listen on
EXPOSE 8000


ENV DJANGO_SETTINGS_MODULE=NewsProject.settings

# Command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]