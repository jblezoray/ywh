
import os
import logging

logging.basicConfig(level=logging.INFO)

KAFKA_BOOTSTRAP_SERVERS =  os.getenv("KAFKA", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", 'program_reports_count')
DATABASE_URI = os.getenv("DATABASE_URI")
YWH_API_URL = os.getenv("YWH_API_URL")
CRAWL_INTERVAL_SECONDS = int(os.getenv("CRAWL_INTERVAL_SECONDS", 60))
KAFKA_NB_PARTITIONS = int(os.getenv("KAFKA_NB_PARTITIONS", 1))



