# Unit tests

## How to run
```bash
python -m pytest
```

 - Run specific test file (`test_statement_manager.py`), class (`TestStatementManager`), and method (`test_csv_no_records`) with more information (`-v` - verbose) example:
```bash
python -m pytest tests/test_statement_manager.py::TestStatementManager::test_csv_no_records -v
```

## Options
 - `-s` - Outputs print statements from test cases

## Useful resources
 - [Testing basics in `pytest`](https://realpython.com/pytest-python-testing/)
 - [Specifics of testing Flask applications](https://realpython.com/python-testing/#testing-for-web-frameworks-like-django-and-flask)