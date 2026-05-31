"""
Common fixtures for other tests.

Fixtures are used to setup common state and/or input data for tests. These specific fixtures should be reusable across multiple test suites or test cases.
If a fixture is only reusable for that specific test case, it should be in the test case file.
Fixtures are mainly for "setup" or "teardown" - they are used automatically by test case just by being specified as input argument.

If the logic you want to add needs needs to happen before the test runs, it is a fixture, otherwise use a function in test suite scope.
"""
import pytest

from app.app import app as _app, db as _db

from app.models.database import Currency, Account, Transaction

from datetime import datetime
from decimal import Decimal

@pytest.fixture
def app():
    _app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with _app.app_context():
        _db.create_all()
        yield _app
        _db.drop_all()

@pytest.fixture
def session(app):
    """
    Creates a new database session for a test.
    
    Importantly, it rolls back any changes made. BUT only if they are not committed.

    This fixture is mandatory for any unit tests interacting with database in any direct or indirect way.
    """
    connection = _db.engine.connect()
    transaction = connection.begin()

    # Bind the session to the connection
    session = _db.session

    yield session # Code before this statement is considered "setup" and code after is the "teardown" portion.

    # Roll back everything after the test is done
    session.remove()
    transaction.rollback()
    connection.close()

@pytest.fixture
def insert_testing_currency(session) -> Currency:
    """Adds a testing currency record to database."""

    currency_record = Currency(
        name = "TEST_CURRENCY",
        sign = "test_cur",
        code = "TST",
    )
    session.add(currency_record)
    session.flush() # commit() cannot be used, since that would break the rollback() in session fixture
    return currency_record

@pytest.fixture
def insert_testing_account(session) -> Account:
    """Adds a testing account record to database."""

    account_record = Account(
        name = "test_account",
        bank_name = "test_bank",
        account_number = "12345678/9012",
    )
    session.add(account_record)
    session.flush() # commit() cannot be used, since that would break the rollback() in session fixture
    return account_record

@pytest.fixture
def insert_testing_transaction(session, insert_testing_currency, insert_testing_account) -> Transaction:
    transaction_record = Transaction(
        amount = Decimal(10.0),
        date = datetime(year = 2020, month = 9, day = 9),
        contra_account_number = "81880926/2700",
        contra_account_name = "81880926/2700",
        my_description = None,
        message = None,

        account = insert_testing_account,
        currency = insert_testing_currency,
        category = None,
    )
    stmt = session.add(transaction_record)
    session.flush() # commit() cannot be used, since that would break the rollback() in session fixture
    return transaction_record
