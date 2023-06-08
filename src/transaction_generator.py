import random
from datetime import datetime, timedelta
from uuid import uuid4

from faker import Faker
from faker.providers import lorem

from src.model.bank import Bank
from src.model.consumer import Consumer
from src.model.merchant import Merchant, MerchantId
from src.model.transaction import Transaction
from src.tasks.simulation_config import SimulationConfig

fake = Faker()
fake.add_provider(lorem)

minutes_per_day = 24 * 60


class TransactionGenerator:
    """
    TransactionGenerator is an iterator which yields valid transactions
    for testing purposes.

    It will start by generating the list of all merchants, consumers, and banks and record
    them to ClickHouse. (In the real world, these entities would already be present or
    accessed via connections to PostgreSQL or other databases.)

    Then, it will generate transactions, ordered by day but unordered within a day.
    The number of transactions per day is random but configurable.

    It can be parameterized with `config.yaml`.
    Look up the `SimulationConfig` for more details.
    """

    def __init__(self, config: SimulationConfig):
        self.__config = config
        # In our simulation, these collections are created and left untouched.
        # We can consider them as immutable.
        # If it were not the case, we would have to handle synchronization.
        self.merchants = [
            self.__generate_merchant(i) for i in range(1, config.merchants + 1)
        ]
        self.consumers = [
            self.__generate_consumer(i, [m.id for m in self.merchants])
            for i in range(1, config.consumers + 1)
        ]
        self.banks = [self.__generate_bank(i) for i in range(1, config.banks + 1)]

        # Pre-compute the lists of all possible IDs.
        self._merchant_ids = [m.id for m in self.merchants]
        self._consumer_ids = [c.id for c in self.consumers]
        self._bank_ids = [b.id for b in self.banks]

        self.start_day: datetime = config.transactions.start_date

    def __iter__(self):
        return (
            self.__generate_transaction(self.start_day + timedelta(days=dt))
            for dt in range(self.__config.transactions.simulation_days)
            for _ in range(self.__draw_daily_number_of_transactions())
        )

    def __draw_daily_number_of_transactions(self):
        return random.randint(
            1, self.__config.transactions.average_transactions_per_day * 2
        )

    def __generate_merchant(self, id: int) -> Merchant:
        _id = Merchant.parse_id(id)
        if not _id:
            raise ValueError("Merchant ID must be valid")

        return Merchant(_id, fake.unique.company())

    def __generate_consumer(self, id: int, merchant_ids: list[MerchantId]) -> Consumer:
        n_favorite_merchants = random.randint(
            0, self.__config.average_favorite_merchants_per_user
        )
        _id = Consumer.parse_id(id)
        if not _id:
            raise ValueError("Consumer ID must be valid")
        return Consumer(
            id=_id,
            name=fake.unique.name(),
            preferred_merchants=random.sample(merchant_ids, n_favorite_merchants),
        )

    def __generate_bank(self, id: int) -> Bank:
        _id = Bank.parse_id(id)
        if not _id:
            raise ValueError("Bank ID must be valid")

        return Bank(
            id=_id,
            name=fake.unique.company(),
            zip_code=fake.unique.zipcode(),
        )

    def __generate_transaction(self, day: datetime) -> Transaction:
        _id = Transaction.parse_id(str(uuid4()))
        if not _id:
            raise ValueError("Transaction ID must be valid")

        # To be more lifelike, we randomize the minutes of the timestamp.
        # Note that, since it occurs during the generation of a transaction,
        # transactions are unordered by timestamp within a day.
        #
        # If the order really matters, we could wrap the generator with `sorted`.
        _day = day + timedelta(minutes=random.randint(0, minutes_per_day))

        return Transaction(
            id=_id,
            merchant_id=random.choice(self._merchant_ids),
            consumer_id=random.choice(self._consumer_ids),
            bank_id=random.choice(self._bank_ids),
            amount=random.randint(1, 100_000),
            country_code=fake.country_code(),
            label=fake.sentence(),
            creation_date=_day,
            execution_date=_day + timedelta(days=1),
        )
