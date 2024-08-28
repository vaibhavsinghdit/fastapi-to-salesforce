import json
import os
import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer

app = FastAPI()

TOPIC_NAME = "contact-topic"
SASL_MECHANISM = "SCRAM-SHA-256"
producer = KafkaProducer(
    bootstrap_servers=os.environ.get("ROUND_2_KAFKA_BROKER_URL"),
    sasl_mechanism=SASL_MECHANISM,
    sasl_plain_username=os.environ.get("ROUND_2_KAFKA_USERNAME"),
    sasl_plain_password=os.environ.get("ROUND_2_KAFKA_PASSWORD"),
    security_protocol="SASL_SSL",
    ssl_cafile="ca.pem",
)


# Pydantic model for Salesforce Contact data
class Contact(BaseModel):
    first_name: str
    last_name: str
    email: str


@app.get("/")
async def root():
    return {
        "message": f"Customer creation api v1 is up and running: {datetime.datetime.now()}"
    }


@app.post("/customer/")
async def create_contact(contact: Contact):
    try:
        # Produce the message to the Kafka topic
        print("=============== START Producer=================")
        print(f"For key={str(contact.email)} - value = {json.dumps(contact.dict())} ")
        # producer.produce(topic_name, key=str(contact.email), value=json.dumps(contact.dict()), callback=delivery_report)
        producer.send("contact-topic", json.dumps(contact.dict()).encode("utf-8"))
        print("=============== END SENDING=================")
        return {
            "message": f"Customer details received: {contact.first_name} {contact.last_name}"
        }
    except Exception as e:
        print(f"Error while sending data to Producer : {e}")
        raise HTTPException(status_code=500, detail=str(e))
