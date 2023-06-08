"""
ClickHouse favors inserts in batches, does not support None in the values, and
values must be tuples (as opposed to dictionaries with key).

This is not very convenient, so we have to do some gymnastics to make it work.

This is why we define recorders to make it easier to record entities, by providing
the dataclasses and have the recorders provide values the ClickHouse driver can
work with.
"""


from typing import Any, Iterable, TypeVar

T = TypeVar("T")


def recorder(ordered_columns: list[str], defaults: dict[str, Any] = {}):
    def record(batch: Iterable[T]) -> tuple[list[tuple[Any, ...]], list[str]]:
        values = [
            tuple(
                item.__getattribute__(column) or defaults.get(column)
                for column in ordered_columns
            )
            for item in batch
        ]
        return values, ordered_columns

    return record


bank_default = recorder(["id", "name", "zip_code"])
merchant_default = recorder(["id", "name"])
consumer_default = recorder(
    ["id", "name", "preferred_merchants"], {"preferred_merchants": []}
)
transaction_default = recorder(
    [
        "id",
        "merchant_id",
        "consumer_id",
        "bank_id",
        "amount",
        "country_code",
        "label",
        "creation_date",
        "execution_date",
    ],
    {"label": "", "merchant_id": 0, "country_code": ""},
)
