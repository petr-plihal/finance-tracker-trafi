"""Unit tests for StatementManager class"""
import pytest

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
