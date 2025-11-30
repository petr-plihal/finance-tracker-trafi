"""Custom errors/exceptions for the project"""

class BaseCustomError(Exception):
    """Base class for custom exceptions in this project."""

# --------------------------------------------------------------

class DataProcessingError(BaseCustomError):
    """Base class for data loading / cleaning issues."""


class AnalysisError(BaseCustomError):
    """Base class for errors during computations, grouping, statistics, etc."""


class ConfigurationError(BaseCustomError):
    """Base class for configuration or environment problems."""


class ValidationError(BaseCustomError):
    """Base class for user input / API argument issues."""

# --------------------------------------------------------------
