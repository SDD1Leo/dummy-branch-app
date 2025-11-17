FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add wait script
COPY wait-for-postgres.sh /usr/local/bin/wait-for-postgres
RUN chmod +x /usr/local/bin/wait-for-postgres

EXPOSE 8000

CMD wait-for-postgres db alembic upgrade head && \
    gunicorn wsgi:app -b 0.0.0.0:8000 --workers 4 --timeout 120
