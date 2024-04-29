# TODO
* [x] Data Ingestion -> raw data from HN API using Kafka
* [ ] Data Processing -> Spark job to run on the data
  * [ ] Find the ones interesting to me
  * [ ] Categorize them
  * [ ] Do some aggregations based on category
* [ ] Data Storage -> either Postgres or NoSQL DB
* [x] Orchestration -> Docker
* [ ] Visualization -> a simple webapp


# Architecture

HN -> Airflow -> stream to Kafka -> stream to Spark -> show 