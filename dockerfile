FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.9-slim-bookworm

EXPOSE 8000

# Install basic tools first, then setup Microsoft repo and install SQL Server driver
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl -sSL https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y unixodbc msodbcsql18 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /wordle-solver/wordle_solver

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /wordle-solver

# Make entrypoint executable (after copying project)
RUN chmod +x /wordle-solver/entrypoint.sh

ENTRYPOINT ["/wordle-solver/entrypoint.sh"] 