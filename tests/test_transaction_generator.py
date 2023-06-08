from src.transaction_generator import TransactionGenerator
from src.tasks.simulation_config import SimulationConfig, TransactionsConfig


def test_transaction_generator():
    generator = TransactionGenerator(
        SimulationConfig(
            transactions=TransactionsConfig(
                simulation_days=2, average_transactions_per_day=10
            )
        )
    )
    assert len(generator.banks) == 10
    assert len(generator.merchants) == 10
    assert len(generator.consumers) == 10

    assert len({bank.id for bank in generator.banks}) == 10
    assert len({merchant.id for merchant in generator.merchants}) == 10
    assert len({consumer.id for consumer in generator.consumers}) == 10

    transactions = list(generator)
    assert len(transactions) > 2
    assert len({t.creation_date.date() for t in transactions}) == 2
