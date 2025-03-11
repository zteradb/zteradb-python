# -----------------------------------------------------------------------------
# File: zteradb_query_type.py
# Description: This file defines the ZTeraDBQueryType enum, which represents
#              different types of database queries such as INSERT, SELECT,
#              UPDATE, DELETE, and NONE. These query types are used in constructing
#              and managing ZTeraDB queries. The file also provides utility methods
#              to check and retrieve query types from their respective values or names.
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

import enum

class ZTeraDBQueryType(enum.Enum):
    """
    Enum class to represent different types of ZTeraDB queries.
    This enum includes the following types:
    - INSERT: For insert operations.
    - SELECT: For select operations.
    - UPDATE: For update operations.
    - DELETE: For delete operations.
    - NONE: To represent no query type.

    The ZTeraDBQueryType class also provides methods to:
    - Check if a query type is INSERT, SELECT, UPDATE, or DELETE.
    - Retrieve the query type from a given value or string.
    """

    # Query types
    INSERT = 0X1 # Insert operation
    SELECT = 0X2 # Select operation
    UPDATE = 0X3 # Update operation
    DELETE = 0X4 # Delete operation
    NONE = None  # No query type

    def __str__(self):
        """
        Return the string representation of the query type.
        This will be the name of the enum (e.g., 'INSERT', 'SELECT').
        """
        return f"{self.name}"

    def is_insert(self):
        """
        Check if the current query type is INSERT.

        :return: True if the query type is INSERT, False otherwise.
        """
        return self.INSERT == self

    def is_select(self):
        """
        Check if the current query type is SELECT.

        :return: True if the query type is SELECT, False otherwise.
        """
        return self.SELECT == self

    def is_update(self):
        """
        Check if the current query type is UPDATE.

        :return: True if the query type is UPDATE, False otherwise.
        """
        return self.UPDATE == self

    def is_delete(self):
        """
        Check if the current query type is DELETE.

        :return: True if the query type is DELETE, False otherwise.
        """
        return self.DELETE == self

    @classmethod
    def get_query_type(cls, value):
        """
        Get the query type from a value.

        :param value: The value representing the query type (e.g., 0X1 for INSERT).
        :return: The corresponding ZTeraDBQueryType enum value, or None if not found.
        """
        return cls(value) if value else None

    @classmethod
    def get_query_type_from_string(cls, query_type):
        """
        Get the query type from a string representation.

        :param query_type: QueryType - The string representation of the query type (e.g., 'SELECT').
        :return: The corresponding ZTeraDBQueryType enum value, or None if not found.
        """
        query_type = query_type.upper()
        if hasattr(cls, query_type):
            return cls(getattr(cls, query_type))

        return None
