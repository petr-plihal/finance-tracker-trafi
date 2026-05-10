"""Unit tests for StatementManager class"""
import pytest

from app.app import app as _app, db as _db

from app.exceptions import StatementFileNotFoundError, StatementFileEmptyError
from app.models.statement_manager import StatementManager

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
