#!/bin/bash
set -e

if ! alembic history | grep "Base Migration"; then
    echo "Creating initial Alembic revision..."
    alembic revision --autogenerate -m "Base Migration"
fi

echo "Applying database migrations..."
alembic upgrade head


echo "Starting Flask app..."
exec "$@"
