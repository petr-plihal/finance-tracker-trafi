"""
Business logic of transaction.
"""

from app.extensions import db
from app.models.database import Transaction

from app.business_logic.business_entities import TransactionBusinessEntity

from sqlalchemy import select

from datetime import datetime
from decimal import Decimal

def get_transaction(
        amount: Decimal | None = None,
        date: datetime | None = None
        ) -> TransactionBusinessEntity | None:

    stmt = select(Transaction)

    # Filters cannot be applied at once, since passing None value would translate to "... AND WHERE attribute IS NULL"
    if amount is not None:
        stmt = stmt.where(Transaction.amount == amount)

    if date is not None:
        stmt = stmt.where(Transaction.date == date)

    transaction_object = db.session.scalars(stmt).first()

    if transaction_object:
        return TransactionBusinessEntity(
            id = transaction_object.id,
            amount = transaction_object.amount,
            date = transaction_object.date,
            contra_account_number = transaction_object.contra_account_number,
            contra_account_name = transaction_object.contra_account_name,
            my_description = transaction_object.my_description,
            message = transaction_object.message,

            account_id = transaction_object.account_id,
            currency_id = transaction_object.currency_id,
            category_id = transaction_object.category_id,
        )
    return None

def list_transactions(
        amount: Decimal | None = None,
        date: datetime | None = None
    ) -> list[TransactionBusinessEntity]:

    stmt = select(Transaction)

    # Filters cannot be applied at once, since passing None value would translate to "... AND WHERE attribute IS NULL"
    if amount is not None:
        stmt = stmt.where(Transaction.amount == amount)

    if date is not None:
        stmt = stmt.where(Transaction.date == date)

    transaction_records = db.session.scalars(stmt).all()

    return [
        TransactionBusinessEntity(
            id = transaction_record.id,
            amount = transaction_record.amount,
            date = transaction_record.date,
            contra_account_number = transaction_record.contra_account_number,
            contra_account_name = transaction_record.contra_account_name,
            my_description = transaction_record.my_description,
            message = transaction_record.message,
            account_id = transaction_record.account_id,
            currency_id = transaction_record.currency_id,
            category_id = transaction_record.category_id,
        )
        for transaction_record in transaction_records
    ]
