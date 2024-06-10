

import sys
import logging

from adapters.paginated_programs_api_iterator import ProgramsPaginatedAPIIteratorBuilder
from adapters.kafka_message_broker import KafkaMessageBrokerConsumer, KafkaMessageBrokerProducer, create_kafka_topic
from adapters.postgres_program_reports_count_persist import PostgresProgramReportsCountPersist
from core.start_points import start_consumer, start_crawler
from core.data.programs_report_count import serializer_program_reports_count
from config.config import CRAWL_INTERVAL_SECONDS, DATABASE_URI, KAFKA_BOOTSTRAP_SERVERS, KAFKA_NB_PARTITIONS, KAFKA_TOPIC, YWH_API_URL

CRAWLER_ARG="-crawler"
CONSUMER_ARG="-consumer"
ARGS=[
    CRAWLER_ARG,
    CONSUMER_ARG,
]

def main():
    
    if len(sys.argv)<2 or ((run_type := sys.argv[1]) not in ARGS):
        args_list = ", ".join(ARGS)
        print(f"This program requires an argument in {args_list}.") 
        exit(1)

    elif run_type == CRAWLER_ARG:
        logging.info("Crawler started.")
        programs_iterator_builder = ProgramsPaginatedAPIIteratorBuilder(
            YWH_API_URL + "/programs"
        )
        create_kafka_topic(KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, KAFKA_NB_PARTITIONS)
        message_broker_producer = KafkaMessageBrokerProducer(
            KAFKA_BOOTSTRAP_SERVERS,
            KAFKA_TOPIC,
            serializer_program_reports_count
        )
        start_crawler(
            programs_iterator_builder, 
            message_broker_producer, 
            CRAWL_INTERVAL_SECONDS
        )

    elif run_type == CONSUMER_ARG:
        logging.info("Consumer started.")
        message_broker_consumer = KafkaMessageBrokerConsumer(
            KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
        )
        program_reports_count_persist = PostgresProgramReportsCountPersist(
            DATABASE_URI
        )
        start_consumer(message_broker_consumer, program_reports_count_persist)

if __name__ == "__main__":
    main()
