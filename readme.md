# Paylead case study
The detail of the case study can be found [here](./DE_assignment.md).

I chose the second option, which consists in sending synthetic events to a Kafka topic, and then
consume them to store them in a ClickHouse Data Warehouse.

The simulator can be configured in the `config.yaml` file.
If the fuzzer is configured, it will fuzz random fields of the transactions, which should be picked
up by the ETL.

My solution is detailed in the [docs](./doc/index.md).

## Dependencies
Some UNIX system with Python 3.10+ and Poetry.

## Getting started
You will need a four terminals in total: one for the Kafka server (+ zookeeper), one for the
ClickHouse server, and one for the rest.

```sh
# Install the project, Kafka, and ClickHouse
bin/install.sh

# Run the kafka server and zookeeper
bin/run_kafka.sh

# In a new shell:
# Initialize the kafka topics
bin/init_kafka.sh

# Run the ClickHouse server
bin/run_clickhouse.sh

# In a new shell:
# Initialize ClickHouse
bin/init_clickhouse.sh

# Run the stream processor:
poetry run python -m src.etls.stream_transactions

# In a new shell:
# Run the simulator
poetry run python -m src.tasks.simulate
```

**Note**: If you need to, you can cleanup the database with `bin/cleanup_clickhouse.sh`.

## Run tests
To run the tests, run: `poetry run pytest tests`
