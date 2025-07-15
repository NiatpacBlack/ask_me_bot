# ./Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Creation of a working directory
WORKDIR /app

# requirements.txt is in the root
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all the contents
COPY . .

# We will make sure that the socket can be created
RUN mkdir -p /tmp

# The default command
CMD ["gunicorn", "--config", "gunicorn_conf.py", "wsgi:app"]
