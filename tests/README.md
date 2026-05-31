# Unit tests

## Usage

### Run all unit tests
```bash
python -m pytest
```

### List available unit tests
```bash
python -m pytest tests --collect-only
```

### Run specific unit test
 - E.g. (`test_statement_manager.py`), class (`TestStatementManager`), and method (`test_csv_no_records`) with more information (`-v` - verbose) example:
```bash
python -m pytest tests/test_statement_manager.py::TestStatementManager::test_csv_no_records -v
```

### Options
 - `-v` - Runs in verbose format that shows additional details, not just details for failed tests
 - `-s` - Outputs print statements from test cases

## Useful resources
 - [Testing basics in `pytest`](https://realpython.com/pytest-python-testing/)
 - [Specifics of testing Flask applications](https://realpython.com/python-testing/#testing-for-web-frameworks-like-django-and-flask)