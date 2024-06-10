


class MessageBrokerProducer:
    def send(message: bytes):
        raise NotImplementedError()
        


class MessageBrokerConsumer:
    def __iter__(self):
        raise NotImplementedError()
    
    def __next__(self):
        raise NotImplementedError()
