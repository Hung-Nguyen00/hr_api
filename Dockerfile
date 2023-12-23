# Use an official Python runtime as a parent image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

COPY .envexample /app/hr/config/.env

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

# Run migrations and start the server when the container launches
CMD ["sh", "-c", "python hr/manage.py migrate && python hr/manage.py runserver 0.0.0.0:8000"]