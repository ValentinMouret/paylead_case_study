from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional

import dateutil.parser as dateutil
import yaml


@dataclass
class TransactionsConfig:
    # For simplification purposes, we assume that the times are all provided in UTC.
    start_date: datetime = datetime(2023, 1, 1, tzinfo=UTC)
    simulation_days: int = 20
    average_transactions_per_day: int = 1_000

    @staticmethod
    def from_dict(d: dict) -> TransactionsConfig:
        return TransactionsConfig(
            start_date=dateutil.parse(d["start_date"], tzinfos={"UTC": UTC}),
            simulation_days=d["simulation_days"],
            average_transactions_per_day=d["average_transactions_per_day"],
        )


@dataclass
class FuzzerConfig:
    dropout_fields: list[str] = field(default_factory=lambda: ["amount", "merchant_id"])
    # Probability that a random field gets dropped.
    dropout_probability: float = 0.1

    @staticmethod
    def from_dict(d: dict) -> FuzzerConfig:
        return FuzzerConfig(
            dropout_fields=d["dropout_fields"],
            dropout_probability=d["dropout_probability"],
        )


@dataclass
class SimulationConfig:
    merchants: int = 10
    consumers: int = 10
    banks: int = 10
    average_favorite_merchants_per_user: int = 3
    transactions: TransactionsConfig = field(default_factory=TransactionsConfig)
    fuzzer: Optional[FuzzerConfig] = field(default=None)

    @staticmethod
    def from_dict(d: dict) -> SimulationConfig:
        return SimulationConfig(
            merchants=d["merchants"],
            consumers=d["consumers"],
            banks=d["banks"],
            average_favorite_merchants_per_user=d[
                "average_favorite_merchants_per_user"
            ],
            transactions=TransactionsConfig.from_dict(d["transactions"]),
            fuzzer=FuzzerConfig.from_dict(d["fuzzer"]) if d.get("fuzzer") else None,
        )


def parse_config(path: str) -> SimulationConfig:
    with open(path, "r") as f:
        return SimulationConfig.from_dict(yaml.safe_load(f))
