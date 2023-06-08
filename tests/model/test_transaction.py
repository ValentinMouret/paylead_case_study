from datetime import datetime
from src.model.bank import BankId
from src.model.consumer import ConsumerId
from src.model.merchant import MerchantId
from src.model.transaction import Transaction, TransactionId, rejection_reason


def test_no_rejection_reason():
    transaction = Transaction(
        id=TransactionId("id"),
        amount=1,
        bank_id=BankId(1),
        consumer_id=ConsumerId(1),
        merchant_id=MerchantId(1),
        creation_date=datetime.now(),
        execution_date=datetime.now(),
    )
    reason = rejection_reason(transaction)
    assert reason is None


def test_amount_negative():
    transaction = Transaction(
        id=TransactionId("id"),
        amount=-100,
        bank_id=BankId(1),
        consumer_id=ConsumerId(1),
        merchant_id=MerchantId(1),
        creation_date=datetime.now(),
        execution_date=datetime.now(),
    )
    reason = rejection_reason(transaction)
    assert reason == "amount_negative"


def test_amount_too_high():
    transaction = Transaction(
        id=TransactionId("id"),
        amount=int(1e9),
        bank_id=BankId(1),
        consumer_id=ConsumerId(1),
        merchant_id=MerchantId(1),
        creation_date=datetime.now(),
        execution_date=datetime.now(),
    )
    reason = rejection_reason(transaction)
    assert reason == "amount_too_high"
