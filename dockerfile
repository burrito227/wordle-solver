# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.9.10-slim-buster

EXPOSE 8000

# Install tools
RUN apt-get update && apt-get install -y gnupg curl unixodbc

# Install Microsoft repo for Microsoft ODBC Driver 18 for SQL Server
RUN apt-get update
RUN apt-get install -y curl gnupg
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl -sSL https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
#ENV DJANGO_SECRET_KEY=''
ARG DB_PASSWORD
ENV DB_PASSWORD=$DB_PASSWORD
#ENV DB_PASSWORD=""

# Copy project
COPY . /wordle-solver

# Set work directory
WORKDIR /wordle-solver/wordle_solver

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh /wordle-solver/entrypoint.sh
RUN chmod +x /wordle-solver/entrypoint.sh
ENTRYPOINT ["/wordle-solver/entrypoint.sh"] 