FROM bitnami/airflow:2.9.0

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY src/dag /opt/bitnami/airflow/dag