from datetime import datetime

from src.fuzzer import Fuzzer
from src.model.bank import BankId
from src.model.consumer import ConsumerId
from src.model.merchant import MerchantId
from src.model.transaction import Transaction, TransactionId
from src.tasks.simulation_config import FuzzerConfig


def test_fuzzer():
    fuzzer = Fuzzer(FuzzerConfig(dropout_fields=["amount"], dropout_probability=1))
    transaction = Transaction(
        id=TransactionId("id"),
        amount=1,
        bank_id=BankId(1),
        consumer_id=ConsumerId(1),
        merchant_id=MerchantId(1),
        creation_date=datetime.now(),
        execution_date=datetime.now(),
    )
    fuzzed = fuzzer.fuzz(transaction)
    assert fuzzed.get("id") == "id"
    assert fuzzed.get("bank_id") == 1
    assert fuzzed.get("amount") is None
