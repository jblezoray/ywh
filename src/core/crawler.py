import time
from core.data.programs_report_count import parse_program_reports_count
from core.ports.message_broker import MessageBrokerProducer
from core.ports.programs_iterator import ProgramsIterator, ProgramsIteratorBuilder
from config.containers import Container
from dependency_injector.wiring import inject, Provide
import logging

@inject
def start(
    crawl_interval_seconds: int,
    programs_iterator_builder: ProgramsIteratorBuilder = Provide[Container.programs_iterator_builder],
    message_broker_producer: MessageBrokerProducer = Provide[Container.message_broker_producer]
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

