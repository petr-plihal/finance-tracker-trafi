"""
Define tables of database.
"""
# pylint: disable=too-few-public-methods

from datetime import datetime
import enum
from decimal import Decimal

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.extensions import db

class AccountType(enum.Enum):
    """
    General type/category of bank account.
    """
    DEPOSIT_ACCOUNT = "deposit_account"
    SAVINGS_ACCOUNT = "savings_account"
    OTHER = "other"

class Account(db.Model):
    """
    Bank account for which transactions were made. Should not contain non-user accounts - contra-accounts.

    Used to categorize and filter transactions based on from which account the transaction has been made.
    """
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column()
    bank_name: Mapped[str] = mapped_column()
    account_number: Mapped[str] = mapped_column(nullable = False)
    account_type: Mapped[AccountType] = mapped_column(
        db.Enum(AccountType),
        default=AccountType.DEPOSIT_ACCOUNT
    )

    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates = "account",
        cascade="all, delete-orphan"
    )

class Currency(db.Model):
    """
    Currency in which a transaction has been made.
    """
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column()
    sign: Mapped[str] = mapped_column()
    code: Mapped[str] = mapped_column(String(3))

    transactions: Mapped[List["Transaction"]] = relationship(back_populates = "currency")

class Category(db.Model):
    """
    Category of transactions.

    Used to group transactions together based on common attributes or manual categorization of transaction by user.
    """
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column()
    monthly_budget: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))

    transactions: Mapped[List["Transaction"]] = relationship(back_populates = "category")
    category_rules: Mapped[List["CategoryRule"]] = relationship(
        back_populates = "category",
        cascade="all, delete-orphan"
    )

class CategoryRuleMatchType(enum.Enum):
    """
    Type of matching to be used to include transactions in categories.

    Based on this the logic decides how to work with categories keyword.
    """
    REGULAR_EXPRESSION = "regular_expression"
    EXACT = "exact"
    CONTAINS = "contains"

class CategoryRule(db.Model):
    """
    Rule that dictates what transactions should be included in the category.
    """
    __tablename__ = "category_rule"

    id: Mapped[int] = mapped_column(primary_key = True)
    keyword: Mapped[str] = mapped_column()
    match_type: Mapped[CategoryRuleMatchType] = mapped_column(
        db.Enum(CategoryRuleMatchType),
        default=CategoryRuleMatchType.CONTAINS
    )

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

    category: Mapped[Category] = relationship(back_populates = "category_rules")

class Transaction(db.Model):
    """
    Any transfer of value involving a financial institution.

    Contains additional distinguishing information that make the transaction unique.
    Also contains information that could be common between transactions.
    Keeps track of finance movement from one account to another.
    """
    __tablename__ = "transaction"
    __table_args__ = (
        UniqueConstraint(
            "amount",
            "date",
            "contra_account_number",
            "account_id",
            name = "_transaction_unique_constraint"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key = True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False, index=True)
    contra_account_number: Mapped[str] = mapped_column(nullable = False, index=True)
    contra_account_name: Mapped[str] = mapped_column(nullable = False)
    my_description: Mapped[Optional[str]] = mapped_column()
    message: Mapped[Optional[str]] = mapped_column()

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))

    account: Mapped[Account] = relationship(back_populates = "transactions")
    currency: Mapped[Currency] = relationship(back_populates = "transactions")
    category: Mapped[Category] = relationship(back_populates = "transactions")
