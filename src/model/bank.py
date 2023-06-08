from typing import NewType, Optional

from pydantic import BaseModel


BankId = NewType("BankId", int)


class Bank(BaseModel):
    id: BankId
    name: str
    zip_code: str

    @staticmethod
    def parse_id(id: int) -> Optional[BankId]:
        return BankId(id)
