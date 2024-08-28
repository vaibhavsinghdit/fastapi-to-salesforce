import logging
import os
import json
from kafka import KafkaConsumer
from sf_contacts_oauth import create_or_update_contact

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to DEBUG for verbose output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

TOPIC_NAME = "contact-topic"
SASL_MECHANISM = 'SCRAM-SHA-256'

consumer = KafkaConsumer(
    TOPIC_NAME,
    auto_offset_reset="earliest",
    bootstrap_servers=f"kafka-2de5c86c-reecegordan398-18d9.k.aivencloud.com:10983",
    client_id="CONSUMER_CLIENT_ID",
    group_id="CONSUMER_GROUP_ID",
    sasl_mechanism=SASL_MECHANISM,
    sasl_plain_username=os.environ.get('KAFKA_USERNAME'),
    sasl_plain_password=os.environ.get('KAFKA_PASSWORD'),
    security_protocol="SASL_SSL",
    ssl_cafile="ca.pem"
)

try:
    logger.info("======= Starting Consumer... ======")

    while True:
        try:
            for message in consumer.poll().values():
                try:
                    logger.debug(f"Received raw message object: {message}")
                    message_value = message[0].value.decode('utf-8')
                    logger.debug(f"Decoded message: {message_value}")

                    # Parse the JSON message to extract contact information
                    contact_data = json.loads(message_value)
                    first_name = contact_data.get('first_name')
                    last_name = contact_data.get('last_name')
                    email = contact_data.get('email')

                    logger.info(
                        f"Extracted Contact Info - First Name: {first_name}, Last Name: {last_name}, Email: {email}")
                    create_or_update_contact(first_name, last_name, email)

                except Exception as ee:
                    logger.error(f"Error occurred reading individual message in loop: {ee}", exc_info=True)

        except Exception as e:
            logger.error(f"Error occurred while consuming message in loop: {e}", exc_info=True)

except KeyboardInterrupt:
    logger.info("Consumer interrupted by user")
finally:
    consumer.close()
    logger.info("Consumer connection closed")
