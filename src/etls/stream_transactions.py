"""
stream_transactions is an ETL which processes transaction messages in the `transactions`
topic and records them to ClickHouse.
"""
from dataclasses import dataclass
from typing import Any, Iterable, Optional

import clickhouse_connect
import orjson as json

from clickhouse_connect.driver.client import Client
from kafka import KafkaConsumer
from src.clickhouse import recorder
from src.model.transaction import RejectionReason, Transaction, rejection_reason
from src.utils import batched


@dataclass
class Config:
    """
    Configuration for the ETL.
    In the real world, some of these configs would be extracted (e.g. clickhouse and kafka)
    to be reused across jobs.
    Here, we have only one ETL, it would be silly to split it.
    """

    kafka_url: str
    clickhouse_host: str
    clickhouse_username: str
    clickhouse_password: str

    batch_size: int = 1000


def parse_transaction(message: bytes) -> Optional[Transaction]:
    """
    Reads messages sent through Kafka (JSONs) and tries to parse them as transactions.
    For whatever reason, this parsing can fail and its fine.

    We want to know about it, and they will be dealt with later.
    """
    try:
        return Transaction(**json.loads(message))
    except Exception as e:
        # Structured logging would be preferable here.
        print(f"failed to parse transaction: {message}, {e}")
        return None


def segregate_transactions(
    messages: Iterable[bytes],
) -> tuple[list[Transaction], list[tuple[str, RejectionReason]]]:
    parsed = ((message, parse_transaction(message)) for message in messages)
    valid_transactions: list[Transaction] = []
    rejected_transactions: list[tuple[str, RejectionReason]] = []

    for message, transaction in parsed:
        if transaction is None:
            rejected_transactions.append((message, "parsing_failed"))
        elif reason := rejection_reason(transaction):
            rejected_transactions.append((message, reason))
        else:
            valid_transactions.append(transaction)

    return valid_transactions, rejected_transactions


def run(config: Config, topic: KafkaConsumer, db: Client):
    # Processes messages in batches.
    messages = (message.value for message in topic)

    for batch in batched(messages, config.batch_size):
        valid_transactions, rejected_transactions = segregate_transactions(batch)
        print(f"Recording valid transactions: {len(valid_transactions)}")
        db.insert(
            "transactions",
            *recorder.transaction_default(valid_transactions),
            "events",
        )
        db.insert(
            "transactions",
            [(message, reason) for (message, reason) in rejected_transactions],
            ["message", "reason"],
            "rejected_events",
        )


if __name__ == "__main__":
    CONFIG = Config(
        kafka_url="localhost:9092",
        clickhouse_host="localhost",
        clickhouse_username="default",
        clickhouse_password="",
    )
    CONSUMER = KafkaConsumer(
        "transactions",
        bootstrap_servers=CONFIG.kafka_url,
    )
    CLIENT = clickhouse_connect.get_client(
        host=CONFIG.clickhouse_host,
        username=CONFIG.clickhouse_username,
        password=CONFIG.clickhouse_password,
    )
    run(CONFIG, CONSUMER, CLIENT)
