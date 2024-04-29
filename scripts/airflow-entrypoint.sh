#!/bin/bash

set -e

if [ -e "/opt/airflow/requirements.txt" ]; then
    echo "Installing additional dependencies..."
    python -m pip install --upgrade pip
    python -m pip install -r /opt/airflow/requirements.txt
fi

if [ ! -f "/opt/airflow/airflow.db" ]; then
    echo "Initializing database..."
    airflow db init && \
    airflow users create \
        --username admin \
        --firstname admin \
        --lastname admin \
        --role Admin \
        --email admin@admin.com \
        --password admin
fi

$(command -v airflow) db upgrade

exec airflow webserver
