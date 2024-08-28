#!/bin/sh
set -x

until kafka-topics.sh --bootstrap-server kafka:9092 --list; do
  echo 'Waiting for Kafka to be reachable...'
  sleep 5
done

echo 'Kafka is reachable. Creating topics...'
kafka-topics.sh --bootstrap-server kafka:9092 --create --if-not-exists --topic contact-topic --replication-factor 1 --partitions 1
echo 'Successfully created the following topics:'
kafka-topics.sh --bootstrap-server kafka:9092 --list
