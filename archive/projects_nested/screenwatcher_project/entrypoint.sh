#!/bin/bash

# Czekaj na bazę danych
echo "Waiting for database..."

echo "Applying database migrations..."
# UWAGA: Makemigrations powinno być robione u dewelopera, nie w kontenerze.
# Zostawiamy tylko migrate.
python manage.py migrate --noinput

echo "Seeding default data..."
python manage.py seed_dashboards

echo "Starting server..."
exec "$@"