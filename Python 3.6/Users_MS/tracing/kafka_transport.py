from kafka import SimpleProducer, KafkaClient

from py_zipkin.transport import BaseTransportHandler


class KafkaTransport(BaseTransportHandler):

    def get_max_payload_bytes(self):
        # By default Kafka rejects messages bigger than 1000012 bytes.
        return 1000012

    def send(self, message):
        kafka_client = KafkaClient('{}:{}'.format('localhost', 9092))
        producer = SimpleProducer(kafka_client)
        producer.send_messages('zipkin', message)
