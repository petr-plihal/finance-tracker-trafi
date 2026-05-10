"""Unit tests for StatementManager class"""
import pytest

from app.app import app as _app, db as _db

from app.exceptions import StatementFileNotFoundError, StatementFileEmptyError
from app.models.statement_manager import StatementManager

from app.models.database import Transaction, Account, Currency
from sqlalchemy import select

class TestStatementManager:
    """
    Tests methods and their outputs of class responsible for working with the main dataframe.
    """

    def test_csv_non_existent(self):
        with pytest.raises(StatementFileNotFoundError):
            StatementManager("tests/data/nonexistent_file.csv")

    def test_csv_empty(self):
        with pytest.raises(StatementFileEmptyError):
            StatementManager("tests/data/csv_empty.csv")

    def test_csv_no_records(self):
        StatementManager("tests/data/csv_no_records.csv")

    def test_csv_simple_records(self):
        StatementManager("tests/data/csv_simple_records.csv")

    def test_csv_store_statements_simple(self, app, session):
        """
        Tests if the StatementManager correctly parses a CSV and 
        saves the records into the database.
        """

        csv_path = "tests/data/csv_simple_records.csv"
        manager = StatementManager(csv_path)

        manager.store_statements(csv_path)

        stmt = select(Transaction)
        results = session.scalars(stmt).all()

        assert len(results) > 0, "No transactions were saved to the database."

        first_record = results[0]
        assert first_record.amount is not None
        assert first_record.account is not None
        assert first_record.currency is not None

        assert session.query(Account).count() >= 1
        assert session.query(Currency).count() >= 1

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
    """Creates a new database session for a test."""
    connection = _db.engine.connect()
    transaction = connection.begin()

    # Bind the session to the connection
    session = _db.session

    yield session

    # Roll back everything after the test is done
    session.remove()
    transaction.rollback()
    connection.close()
