from dataclasses import dataclass
from typing import NewType, Optional

MerchantId = NewType("MerchantId", int)


@dataclass
class Merchant:
    id: MerchantId
    name: str

    @staticmethod
    def parse_id(id: int) -> Optional[MerchantId]:
        return MerchantId(id)
