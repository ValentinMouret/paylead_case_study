from typing import NewType, Optional

from pydantic import BaseModel
from .merchant import MerchantId


ConsumerId = NewType("ConsumerId", int)


class Consumer(BaseModel):
    id: ConsumerId
    name: str
    preferred_merchants: list[MerchantId]

    @staticmethod
    def parse_id(id: int) -> Optional[ConsumerId]:
        # There might be rules here to check whether the ID is valid.
        # Here, we always return a valid ID.
        return ConsumerId(id)
