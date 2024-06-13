
from adapters.paginated_programs_api_iterator import ProgramsPaginatedAPIIteratorBuilder
from adapters.kafka_message_broker import KafkaMessageBrokerConsumer, KafkaMessageBrokerProducer
from adapters.postgres_program_reports_count_persist import PostgresProgramReportsCountPersist
from adapters.and_program_reports_count_persist import AndProgramReportsCountPersist
from adapters.influxdb_program_reports_count_persist import InfluxDbProgramReportsCountPersist
from core.ports.message_broker import MessageBrokerConsumer, MessageBrokerProducer
from core.ports.programs_iterator import ProgramsIteratorBuilder
from core.ports.programs_report_persist import ProgramReportsCountPersist
from core.data.programs_report_count import serializer_program_reports_count
from config.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_PASSWORD, INFLUXDB_USERNAME, POSTGRESQL_URL, KAFKA_BOOTSTRAP_SERVERS, KAFKA_NB_PARTITIONS, KAFKA_TOPIC, YWH_API_URL, INFLUXDB_URL
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):

    programs_iterator_builder: ProgramsIteratorBuilder = providers.Factory(
        ProgramsPaginatedAPIIteratorBuilder,
        base_url=f"{YWH_API_URL}/programs",
    )
    
    message_broker_producer: MessageBrokerProducer = providers.Factory(
        KafkaMessageBrokerProducer,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        topic=KAFKA_TOPIC,
        expected_partitions_count=KAFKA_NB_PARTITIONS,
        value_serializer=serializer_program_reports_count
    )

    message_broker_consumer : MessageBrokerConsumer= providers.Factory(
        KafkaMessageBrokerConsumer,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        topic=KAFKA_TOPIC
    )

    postgres_program_reports_count_persist: ProgramReportsCountPersist = providers.Factory(
        PostgresProgramReportsCountPersist,
        database_url=POSTGRESQL_URL
    )

    influxdb_program_reports_count_persist: ProgramReportsCountPersist = providers.Factory(
        InfluxDbProgramReportsCountPersist,
        url=INFLUXDB_URL,
        username=INFLUXDB_USERNAME,
        password=INFLUXDB_PASSWORD,
        org=INFLUXDB_ORG,
        bucket=INFLUXDB_BUCKET
    )

    program_reports_count_persist: ProgramReportsCountPersist =  providers.Factory(
        AndProgramReportsCountPersist,
        postgres_program_reports_count_persist,
        influxdb_program_reports_count_persist
    )