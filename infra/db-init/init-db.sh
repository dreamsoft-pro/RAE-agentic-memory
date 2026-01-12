#!/bin/bash
set -e

# Call the original entrypoint script
/usr/local/bin/docker-entrypoint.sh postgres &

# Wait for postgres to be ready
until pg_isready -h localhost -U "$POSTGRES_USER"; do
  echo "Waiting for postgres..."
  sleep 1
done

# Create the database if it doesn't exist
echo "Creating database $POSTGRES_DB"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<EOSQL
    CREATE DATABASE "$POSTGRES_DB";
EOSQL
echo "Database $POSTGRES_DB created."

# Keep the original entrypoint process running
wait