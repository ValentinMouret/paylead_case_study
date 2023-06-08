from dataclasses import dataclass
from typing import Optional
from src.clickhouse.recorder import recorder


@dataclass
class User:
    name: str
    age: Optional[int]


def test_recorder():
    record = recorder(["age", "name"], defaults={"age": 0})
    users = [User("John", None), User("Jane", 20)]
    records = record(users)
    assert records == (
        [(0, "John"), (20, "Jane")],
        ["age", "name"],
    )
