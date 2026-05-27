"""Defines transaction object returned by Data Access Layer (service)"""

import enum

from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True)
class TransactionBusinessEntity:
    """
    Object representing transaction after retrieval from database. Returned from DAL.
    """
    id: int
    amount: Decimal
    date: datetime
    contra_account_number: str
    contra_account_name: str
    my_description: str | None
    message: str | None

    account_id: int
    currency_id: int
    category_id: int | None

class AccountTypeBusinessEntity(enum.Enum):
    """
    General type/category of bank account.
    """
    DEPOSIT_ACCOUNT = "deposit_account"
    SAVINGS_ACCOUNT = "savings_account"
    OTHER = "other"

@dataclass(frozen=True)
class AccountBusinessEntity:
    """
    Object representing account after retrieval from database. Returned from DAL.
    """
    id: int
    name: str
    bank_name: str
    account_number: str
    account_type: AccountTypeBusinessEntity | None

    # transactions TODO: have no idea how to connect these at this point. Just adding an array of business entity objects seems possible but is it ideal for the logical layer?
