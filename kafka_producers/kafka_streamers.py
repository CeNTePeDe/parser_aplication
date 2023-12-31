import json
import logging

from config.settings import settings
from kafka import KafkaConsumer, KafkaProducer
from parsers.parse_streamer import get_data_streams

logger = logging.getLogger(__name__)


def send_data_to_kafka_streamers(url):
    producer = KafkaProducer(bootstrap_servers=settings.KAFKA_URL)
    logger.info(f"{producer}")
    streamers = get_data_streams()
    for stream in streamers:
        streamer_str = json.dumps(stream)
        streamer_bytes = streamer_str.encode("utf-8")
        producer.send(topic=settings.TOPIC_STREAMER, value=streamer_bytes)


consumer_streamer = KafkaConsumer(
    settings.TOPIC_STREAMER,
    auto_offset_reset=settings.AUTO_OFFSET_RESET,
    bootstrap_servers=settings.KAFKA_URL,
    consumer_timeout_ms=settings.CONSUMER_TIMEOUT_MS,
)
