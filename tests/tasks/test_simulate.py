from datetime import datetime

import orjson
from src.model.bank import BankId
from src.model.consumer import ConsumerId
from src.model.merchant import MerchantId
from src.model.transaction import Transaction, TransactionId


def test_serde():
    transaction = Transaction(
        id=TransactionId("id"),
        amount=1,
        bank_id=BankId(1),
        consumer_id=ConsumerId(1),
        merchant_id=MerchantId(1),
        creation_date=datetime.now(),
        execution_date=datetime.now(),
    )
    message = orjson.dumps(transaction.__dict__)
    assert Transaction(**orjson.loads(message)) == transaction
