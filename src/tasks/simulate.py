"""
Simulates transactions following `config.yaml` and sends them to Kafka.

It starts by creating the banks, merchants, and consumers and sending them to the corresponding
topics for creation in ClickHouse.

Then, it creates transactions and sends them to the corresponding topic for creation in ClickHouse.

A fuzzer can be configured to create anomalies in the transactions to see how the ETL behaves.
"""

from __future__ import annotations

from pprint import pprint

import clickhouse_connect
import orjson as json
from clickhouse_connect.driver.client import Client
from kafka import KafkaProducer

from src.clickhouse import recorder
from src.fuzzer import Fuzzer
from src.tasks.simulation_config import SimulationConfig, parse_config
from src.transaction_generator import TransactionGenerator
from src.utils import batched


def load_config() -> SimulationConfig:
    config = parse_config("config.yaml")
    print("Configuration:")
    pprint(config)
    if config.fuzzer:
        print("- Fuzzing is enabled")
    return config


def record_entities(generator: TransactionGenerator, client: Client):
    # Banks, merchants, and consumers are created once and for all.
    # Here, we push them through Kafka, but they would probably be created differently.
    # I chose to put the focus on the processing of transactions.
    client.insert(
        "banks",
        *recorder.bank_default(generator.banks),
        "entities",
    )
    client.insert(
        "merchants",
        *recorder.merchant_default(generator.merchants),
        "entities",
    )
    client.insert(
        "consumers",
        *recorder.consumer_default(generator.consumers),
        "entities",
    )


if __name__ == "__main__":
    config = load_config()

    generator = TransactionGenerator(config)
    fuzzer = Fuzzer(config.fuzzer) if config.fuzzer else None

    transactions = (
        transaction.__dict__ if not fuzzer else fuzzer.fuzz(transaction)
        for transaction in generator
    )

    # The URL can be moved to the config on production.
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092", compression_type="zstd"
    )
    client = clickhouse_connect.get_client(
        host="localhost", username="default", password=""
    )
    record_entities(generator, client)

    for batch in batched(transactions, 1_000):
        for transaction in batch:
            # By using the transaction as the key, we ensure that transactions with the same ID
            # are sent to the same partition. This is important for the deduplication.
            producer.send(
                topic="transactions",
                value=json.dumps(transaction),
                key=(transaction["id"] or "missing").encode("utf-8"),
            )
        producer.flush()
