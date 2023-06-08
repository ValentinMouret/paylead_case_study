import random

from src.model.transaction import Transaction
from src.tasks.simulation_config import FuzzerConfig


class Fuzzer:
    """
    Fuzzer will alter transactions according to the configuration to create anomalies.
    For now, only «dropout» is implemented.
    It will randomly drop a field from the record.
    """

    def __init__(self, config: FuzzerConfig = FuzzerConfig()):
        self.__config = config

    def fuzz(self, transaction: Transaction):
        return Fuzzer.__dropout(
            transaction, self.__config.dropout_fields, self.__config.dropout_probability
        )

    @staticmethod
    def __dropout(transaction: Transaction, fields: list[str], probability: float):
        return {
            key: None if (key in fields and random.random() < probability) else value
            for key, value in transaction.__dict__.items()
        }
