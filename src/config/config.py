
import os
import logging

logging.basicConfig(level=logging.INFO)

KAFKA_BOOTSTRAP_SERVERS =  os.getenv("KAFKA", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", 'program_reports_count')
POSTGRESQL_URL = os.getenv("POSTGRESQL_URL")
INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_USERNAME = os.getenv("INFLUXDB_USERNAME")
INFLUXDB_PASSWORD = os.getenv("INFLUXDB_PASSWORD")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")
YWH_API_URL = os.getenv("YWH_API_URL")
CRAWL_INTERVAL_SECONDS = int(os.getenv("CRAWL_INTERVAL_SECONDS", 60))
KAFKA_NB_PARTITIONS = int(os.getenv("KAFKA_NB_PARTITIONS", 1))



