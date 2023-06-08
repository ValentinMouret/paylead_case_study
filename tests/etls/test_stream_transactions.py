from datetime import datetime

import orjson as json

from src.etls.stream_transactions import segregate_transactions
from src.model.transaction import Transaction


def test_seggregation():
    messages = [
        json.dumps(m)
        for m in (
            {
                "id": "id",
                "merchant_id": 1,
                "consumer_id": 1,
                "bank_id": 1,
                "amount": 1,
                "creation_date": datetime.now(),
                "execution_date": datetime.now(),
            },
            {
                "id": "id",
                "amount": None,
                "bank_id": 1,
                "consumer_id": 1,
                "merchant_id": 1,
                "creation_date": datetime.now(),
                "execution_date": datetime.now(),
            },
            {
                "id": "id",
                "amount": -100,
                "bank_id": 1,
                "consumer_id": 1,
                "merchant_id": 1,
                "creation_date": datetime.now(),
                "execution_date": datetime.now(),
            },
        )
    ]

    segregated = segregate_transactions(messages)
    assert len(segregated) == 2

    valid, rejected = segregated
    assert len(valid) == 1
    assert len(rejected) == 2

    assert valid[0] == Transaction(**json.loads(messages[0]))

    # The order should be preserved.
    assert rejected[0] == (messages[1], "parsing_failed")
    assert rejected[1] == (messages[2], "amount_negative")
