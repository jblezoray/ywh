import time
from core.data.programs_report_count import ProgramReportsCount, deserializer_program_reports_count
from core.ports.message_broker import MessageBrokerConsumer
from core.ports.programs_report_persist import ProgramReportsCountPersist
from config.containers import Container
from dependency_injector.wiring import inject, Provide
import logging

@inject
def start(
    message_broker_consumer: MessageBrokerConsumer = Provide[Container.message_broker_consumer], 
    program_reports_count_persist: ProgramReportsCountPersist = Provide[Container.program_reports_count_persist]
):
    while True:
        try:
            for message in message_broker_consumer:
                logging.info(f"Receiving: {message}")
                prc: ProgramReportsCount = deserializer_program_reports_count(message.value)
                program_reports_count_persist.persist(prc)

        except Exception as e:
            logging.warning(f"Houston, we've had a problem: {e}", exc_info=True)
            time.sleep(1)
