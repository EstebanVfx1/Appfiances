from pydantic import BaseModel
from datetime import date
from enum import Enum as PydanticEnum

class TransactionType(str, PydanticEnum):
    revenue ="revenue"
    expenses ="expenses"


class TransactionBase(BaseModel):
    user_id: str
    category_id: int
    amount: float
    t_description: str
    t_type: TransactionType

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    transactions_id: int

class TransactionUpdate(TransactionBase):
    pass

class TransactionDelete(BaseModel):
    transactions_id: int
