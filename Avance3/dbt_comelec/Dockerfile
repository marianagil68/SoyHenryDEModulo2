FROM python:3.10-slim

WORKDIR /usr/app

# Instalar dependencias del sistema necesarias para PostgreSQL y dbt
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar dbt y dbt-postgres
RUN pip install --upgrade pip && \
    pip install --no-cache-dir dbt-postgres==1.5.0

# Configurar variables de entorno
ENV DBT_PROFILES_DIR=/usr/app
ENV PYTHONUNBUFFERED=1
