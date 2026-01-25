"""
Module for instantiating Flask extensions.

Also avoids circular imports.
"""

# SQL toolkit and Object Relational Mapper (ORM) for database
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object without "binding" it to a specific app yet.
db = SQLAlchemy()
