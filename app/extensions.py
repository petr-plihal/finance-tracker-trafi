"""
Module for instantiating Flask extensions.

Also avoids circular imports.
"""
# pylint: disable=too-few-public-methods

# SQL toolkit and Object Relational Mapper (ORM) for database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

class Base(DeclarativeBase, MappedAsDataclass):
    """Base class for all classes that represent entities in database."""

# Initialize the SQLAlchemy object without "binding" it to a specific app yet.
db = SQLAlchemy(model_class = Base)
