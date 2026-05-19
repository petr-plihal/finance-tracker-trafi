"""
Common fixtures for other tests.

Fixtures are used to setup common state and/or input data for tests. These specific fixtures should be reusable across multiple test suites or test cases.
If a fixture is only reusable for that specific test case, it should be in the test case file.
Fixtures are mainly for "setup" or "teardown" - they are used automatically by test case just by being specified as input argument.

If the logic you want to add needs needs to happen before the test runs, it is a fixture, otherwise use a function in test suite scope.
"""
import pytest

from app.app import app as _app, db as _db

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

    yield session # Code before this statement is considered "setup" and code after is the "teardown" portion.

    # Roll back everything after the test is done
    session.remove()
    transaction.rollback()
    connection.close()
