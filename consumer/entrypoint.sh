#!/bin/sh

echo "Waiting for Kafka to be ready..."
# Start the consumer service
exec python -u main.py
