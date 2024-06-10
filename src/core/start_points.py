import time
from core.data.programs_report_count import ProgramReportsCount, deserializer_program_reports_count, parse_program_reports_count
from core.ports.message_broker import MessageBrokerConsumer, MessageBrokerProducer
from core.ports.programs_report_persist import ProgramReportsCountPersist
from core.ports.programs_iterator import ProgramsIterator, ProgramsIteratorBuilder
import logging

def start_crawler(
    programs_iterator_builder: ProgramsIteratorBuilder,
    message_broker_producer: MessageBrokerProducer,
    crawl_interval_seconds: int
):
    while True:
        try:
            it : ProgramsIterator = programs_iterator_builder.build()
            for program_data in it: 
                if (prc := parse_program_reports_count(program_data)):
                    logging.info(f"Sending: {prc}")
                    message_broker_producer.send(prc)

        except Exception as e:
            logging.warning(f"Houston, we had a problem: {e}", exc_info=True)

        time.sleep(crawl_interval_seconds)


def start_consumer(
    message_broker_consumer: MessageBrokerConsumer, 
    program_reports_count_persist: ProgramReportsCountPersist
):
    while True:
        try:
            for message in message_broker_consumer:
                logging.info(f"Receiving: {message}")
                prc: ProgramReportsCount = deserializer_program_reports_count(message.value)
                program_reports_count_persist.persist(prc)
                time.sleep(1)

        except Exception as e:
            logging.warning(f"Houston, we've had a problem: {e}", exc_info=True)
