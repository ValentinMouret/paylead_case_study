#!/bin/bash

# Initialises the Kafka topics.

set -euo pipefail

readonly port=9092

kafka::create_topic() {
    name=$1
    bin/kafka-topics.sh --create --topic "$name" --bootstrap-server localhost:$port
}

setup::kafka() {
    kafka::create_topic transactions
}

(cd kafka && setup::kafka)
