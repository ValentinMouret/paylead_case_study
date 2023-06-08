# Kafka
## Situation
In our case, we only have one kafka topic: `transactions`.
This topic has only one replica and one partition.
In a production environment, it should be replicated and partitioned.

## Getting started
```shell
# If needed, install kafka.
./bin/install.sh

# Run
# Note: this will run zookeeper and kafka in the same process.
#       it is noisy, but it’s fine for a case study.
./bin/run_kafka.sh

# In another shell
# Create the topic
./bin/init_kafka.sh
```

## Improvements
* Add monitoring
* Enforce stronger specs with protobuf
* Add repilcas and partitions
* Implement a process to enable reprocessing

[Index](./index.md)