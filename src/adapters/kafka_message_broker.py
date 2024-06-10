
from typing import Callable
from core.ports.message_broker import MessageBrokerConsumer, MessageBrokerProducer
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import TopicAlreadyExistsError
from kafka.admin import KafkaAdminClient, NewPartitions, NewTopic


class KafkaMessageBrokerProducer(MessageBrokerProducer):
    def __init__(self, bootstrap_servers: str, topic: str, value_serializer: Callable[str, bytes]):
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers, 
            value_serializer=value_serializer,
        )
        self._topic = topic
        
    def send(self, message: bytes):
        self._producer.send(self._topic, message)


class KafkaMessageBrokerConsumer(MessageBrokerConsumer):
    def __init__(self, bootstrap_servers: str, topic: str):
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset="earliest",
            group_id=f'{topic}_group' 
        )
        # TODO subscribe to a ConsumerRebalanceListener here.

    def __iter__(self):
        return self._consumer.__iter__()
    
    def __next__(self):
        # TODO here we should add an adaptation layer to not leak kafka 
        # datatypes in the core.
        return self._consumer.__next__()


def create_kafka_topic(bootstrap_servers: str, topic: str, expected_partitions_count: int):

    consumer = None
    admin_client = None
    current_partitions_count = -1
    try:
        # check the number of partitions for the topic ;
        consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)
        current_partitions_count = len(consumer.partitions_for_topic(topic))
        if current_partitions_count >= expected_partitions_count:
            return

        # or create a topic with the expected number of partitions ;
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        try:
            admin_client.create_topics(
                new_topics=[
                    NewTopic(name=topic, num_partitions=expected_partitions_count, replication_factor=1)
                ]
            )

        except TopicAlreadyExistsError:
            # Or adjust the number of partitions in the existing topic.
            admin_client.create_partitions(
                {
                    topic: NewPartitions(total_count=expected_partitions_count)
                }
            )

    finally: 
        if consumer is not None:
            consumer.close()
        if admin_client is not None:
            admin_client.close()
