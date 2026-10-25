# Base image / Image de base
FROM python:3.13-slim

# Environment variables / Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Working directory / Dossier de travail
WORKDIR /app

# System dependencies for psycopg / Deps système pour psycopg
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps / Copie requirements et installe les deps Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#  THIS LINE WAS MISSING / CETTE LIGNE MANQUAIT

# Copy the code / Copie le code
COPY . .
# Make entrypoint executable / Rend l'entrypoint exécutable
Run chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]