#!/bin/bash

# Runs Zookeeper and Kafka servers with the same process for simplicity.
# In production, these would be two separate processes.

set -euo pipefail

cd kafka
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties
