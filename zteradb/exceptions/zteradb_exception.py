# -----------------------------------------------------------------------------
# File: zteradb_exceptions.py
# Description: This file defines custom exception classes used in the ZTeraDB
#              system. The base exception class `ZTeraBaseError` is extended by
#              more specific exceptions like `NoDataError` and `QueryComplete`
#              for handling particular error cases related to the TeraDB database.
#
# License: ZTeraDB
# Copyright (c) 2025 ZTeraDB
#
# The code in this file is proprietary and confidential. It may not be shared,
# re-engineered, reverse-engineered, modified, or distributed in any way without
# express written permission from the copyright holder.
#
# All rights are reserved to the copyright holder.
#
# License URL: https://zteradb.com/licence
# -----------------------------------------------------------------------------

class ZTeraBaseError(Exception):
    """
    Base exception class for TeraDB-related errors.

    This class serves as the base for all custom exceptions related to TeraDB.
    It extends the built-in Python Exception class and allows setting a custom
    message that can be used when the exception is raised.

    Attributes:
        message (str): The error message associated with the exception.
    """

    def __init__(self, message):
        """
        Initializes the ZTeraBaseError with a custom message.

        :param message: str - The error message to be associated with the exception.
        """
        self.message = message
        super().__init__(self.message)

    def __dict__(self):
        """
        Return the error message when the exception is serialized to a dictionary.

        :return: str - The error message associated with the exception.
        """
        return self.message


class ZTeraDBError(ZTeraBaseError):
    """
    Exception raised when any error occurs during a database query.

    This exception inherits from ZTeraBaseError and is raised when a query or
    operation does not return any data. It is commonly used when an expected query error occurs.

    Example usage:
        raise ZTeraDBError("An error occurred while executing error")
    """
    def __init__(self, message):
        """
        Initializes the ZTeraDBError with a custom message.

        :param message: str - The error message to be associated with the exception.
        """
        super().__init__(message)


class ZTeraDBQueryError(ZTeraDBError):
    """
    Exception raised when any error occurs during a database query.

    This exception inherits from ZTeraDBError and is raised when a query or
    operation does not return any data. It is commonly used when an expected query error occurs.

    Example usage:
        raise ZTeraDBQueryError("An error occurred while executing error")
    """
    def __init__(self, message):
        """
        Initializes the ZTeraDBQueryError with a custom message.

        :param message: str - The error message to be associated with the exception.
        """
        super().__init__(message)


class ZTeraDBConditionError(ZTeraDBError):
    """
    Exception raised when any error occurs during a database query.

    This exception inherits from ZTeraDBError and is raised when a query or
    operation does not return any data. It is commonly used when an expected query error occurs.

    Example usage:
        raise ZTeraDBQueryError("An error occurred while executing error")
    """
    def __init__(self, message):
        """
        Initializes the ZTeraDBQueryError with a custom message.

        :param message: str - The error message to be associated with the exception.
        """
        super().__init__(message)


class NoResponseDataError(ZTeraBaseError):
    """
    Exception raised when no data is found or available during a database query.

    This exception inherits from ZTeraBaseError and is raised when a query or
    operation does not return any data. It is commonly used when the expected data
    does not exist in the database.

    Example usage:
        raise NoDataError("No data available for the query.")
    """

    def __init__(self, message):
        """
        Initializes the NoDataError with a custom message.

        :param message: str - The error message to be associated with the exception.
        """
        super().__init__(message)


class QueryComplete(ZTeraBaseError):
    """
    Exception raised when a database query completes successfully.

    This exception inherits from ZTeraBaseError and is used to indicate that a query
    has been successfully executed. It serves as a signal that the query completed
    without errors.

    Example usage:
        raise QueryComplete("Query completed successfully.")
    """

    def __init__(self, message):
        """
        Initializes the QueryComplete exception with a custom message.

        :param message: str - The error message to be associated with the exception.
        """
        super().__init__(message)


class AuthenticationFailed(ZTeraBaseError):
    """
    Exception raised when a database query completes successfully.

    This exception inherits from ZTeraBaseError and is used to indicate that a query
    has been successfully executed. It serves as a signal that the query completed
    without errors.

    Example usage:
        raise AuthenticationFailed("An error occurred while authenticating.")
    """

    def __init__(self, message):
        """
        Initializes the AuthenticationFailed exception with a custom message.

        :param message: str - The error message to be associated with the exception.
        """
        super().__init__(message)
