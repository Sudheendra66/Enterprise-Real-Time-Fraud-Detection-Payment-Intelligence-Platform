import json
import os

from dotenv import load_dotenv
from kafka import KafkaProducer

from src.utils.logger import get_logger

# Load environment variables
load_dotenv()

logger = get_logger("KafkaProducer")


class FraudKafkaProducer:

    def __init__(self):

        self.topic = os.getenv("KAFKA_TOPIC")

        self.producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),

            security_protocol="SASL_SSL",
            sasl_mechanism="PLAIN",
            sasl_plain_username=os.getenv("KAFKA_API_KEY"),
            sasl_plain_password=os.getenv("KAFKA_API_SECRET"),

            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        )

        logger.info(f"Connected to Kafka topic: {self.topic}")

    def send(self, event: dict):

        self.producer.send(self.topic, value=event)

    def flush(self):

        self.producer.flush()

    def close(self):

        self.producer.flush()
        self.producer.close()

        logger.info("Kafka Producer closed successfully.")