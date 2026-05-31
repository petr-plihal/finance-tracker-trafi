"""Unit tests for transaction service logic"""
import pytest

# from app.exceptions import

from app.models.database import Transaction
from app.services.transaction_service import get_transaction, list_transactions

from decimal import Decimal
from datetime import datetime

class TestTransactionService:
    """
    Unit tests for basic logical operations regarding transaction records.
    """
    @pytest.fixture
    def _insert_single_transaction(self, session):
        pass

    @pytest.fixture
    def _insert_two_transactions(self, session, insert_testing_account, insert_testing_currency) -> list[Transaction]:
        transactions_list: list[Transaction] = []

        transactions_list.append(Transaction(
            amount = Decimal(10.0),
            date = datetime(year = 2020, month = 9, day = 9),
            contra_account_number = "81880926/2700",
            contra_account_name = "81880926/2700",
            my_description = None,
            message = None,

            account = insert_testing_account,
            currency = insert_testing_currency,
            category = None,
        ))
        transactions_list.append(Transaction(
            amount = Decimal(10.0),
            date = datetime(year = 2030, month = 1, day = 1),
            contra_account_number = "62908818/2700",
            contra_account_name = "62908818/2700",
            my_description = None,
            message = None,

            account = insert_testing_account,
            currency = insert_testing_currency,
            category = None,
        ))

        for transaction in transactions_list:
            session.add(transaction)

        session.flush() # commit() cannot be used, since that would break the rollback() in session fixture
        return transactions_list


    def test_get_transaction_no_transactions(self, session):
        assert get_transaction() is None

    def test_get_transaction_amount_match_one_record(self, session, insert_testing_transaction):
        test_transaction = get_transaction(amount = Decimal(10.0))

        assert test_transaction is not None
        assert test_transaction.amount == Decimal(10.0)

    def test_get_transaction_amount_match_multiple_records(self, _insert_two_transactions):
        test_transaction = get_transaction(amount = Decimal(10.0))

        assert test_transaction is not None
        assert test_transaction.amount == Decimal(10.0)


    def test_list_transactions_no_transactions(self, session):
        assert not list_transactions() # Assert list is empty

    def test_list_transactions_amount_match_one_record(self, _insert_two_transactions):
        transaction_amount = Decimal(10.0)

        test_transaction_list = list_transactions(amount = transaction_amount)

        assert test_transaction_list # Assert list is not empty
        assert len(test_transaction_list) == 1
        assert test_transaction_list[0].amount == transaction_amount


    def test_list_transactions_amount_match_multiple_records(self, _insert_two_transactions):
        transaction_amount = Decimal(10.0)

        test_transaction_list = list_transactions(amount = transaction_amount)

        assert test_transaction_list # Assert list is not empty
        assert len(test_transaction_list) == 2
        assert test_transaction_list[0].amount == transaction_amount
        assert test_transaction_list[1].amount == transaction_amount
