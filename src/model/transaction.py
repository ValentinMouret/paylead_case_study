from datetime import datetime, timedelta
from functools import reduce
from typing import Literal, NewType, Optional

from pydantic import BaseModel

from .bank import BankId
from .consumer import ConsumerId
from .merchant import MerchantId

TransactionId = NewType("TransactionId", str)


class Transaction(BaseModel):
    id: TransactionId
    merchant_id: Optional[MerchantId]
    consumer_id: ConsumerId
    bank_id: BankId
    amount: int
    country_code: Optional[str] = None
    label: Optional[str] = None
    creation_date: datetime
    execution_date: datetime

    @staticmethod
    def parse_id(id: str) -> Optional[TransactionId]:
        return TransactionId(id)


"""
We want to define a list of rules which will assert the validity of a transaction.
Passed the typing, we may want to check some business logic, for instance that the amount
is greater than 0.
"""

RejectionReason = Literal[
    "parsing_failed",
    "amount_negative",
    "amount_too_high",
    "old_transaction",
    "future_transaction",
]


def check_amount_not_too_high(
    transaction: Transaction,
) -> Optional[Literal["amount_too_high"]]:
    return "amount_too_high" if transaction.amount > 1000000 else None


def check_amount_positive(
    transaction: Transaction,
) -> Optional[Literal["amount_negative"]]:
    return "amount_negative" if transaction.amount < 0 else None


def check_recent_transaction(
    transaction: Transaction,
) -> Optional[Literal["old_transaction"]]:
    return (
        "old_transaction"
        if transaction.creation_date < datetime.now() - timedelta(days=365 * 2)
        else None
    )


def check_not_future_transaction(
    transaction: Transaction,
) -> Optional[Literal["future_transaction"]]:
    return (
        "future_transaction"
        if transaction.creation_date > datetime.now() + timedelta(days=1)
        else None
    )


validity_checks = [
    check_amount_not_too_high,
    check_amount_positive,
    check_recent_transaction,
    check_not_future_transaction,
]


def rejection_reason(transaction: Transaction) -> RejectionReason | None:
    """
    Sequentially checks the different rules which assert the validity of a transaction.
    As soon as we find a reason to reject the transaction, we return it.
    If no reason is found, we return None.
    """
    return reduce(
        lambda reason, f: reason or f(transaction),
        validity_checks,
        None,
    )
