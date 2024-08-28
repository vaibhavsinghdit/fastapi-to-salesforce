#!/bin/bash

# Check if a path argument is provided
if [ $# -eq 0 ]; then
    echo "Please provide the path to Kafka directory as an argument."
    echo "Usage: $0 /path/to/kafka"
    exit 1
fi

# Store the provided path
KAFKA_PATH="$1"

# Function to stop Kafka and Zookeeper
stop_services() {
    echo "Stopping Kafka and Zookeeper..."
    "$KAFKA_PATH"/bin/kafka-server-stop.sh
    "$KAFKA_PATH"/bin/zookeeper-server-stop.sh
    exit 0
}

# Trap Ctrl+C (SIGINT) and SIGTERM
trap stop_services SIGINT SIGTERM

# Start Zookeeper
"$KAFKA_PATH"/bin/zookeeper-server-start.sh "$KAFKA_PATH"/config/zookeeper.properties &

# Wait for Zookeeper to start
sleep 10

# Start Kafka server
"$KAFKA_PATH"/bin/kafka-server-start.sh "$KAFKA_PATH"/config/server.properties &

# Wait for Kafka to start
sleep 10

# List topics
"$KAFKA_PATH"/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Create contact-topic
"$KAFKA_PATH"/bin/kafka-topics.sh --create --topic contact-topic --bootstrap-server localhost:9092

# Create topic-name with partitions and replication factor
"$KAFKA_PATH"/bin/kafka-topics.sh --create --topic contact-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

echo "Kafka and Zookeeper are running. Press Ctrl+C to stop."

# Keep the script running and wait for signals
wait