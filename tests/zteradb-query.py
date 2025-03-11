# -----------------------------------------------------------------------------
# File: zteradb_query.py
# Description: This file contains the test cases for the ZTeraDBQuery class.
#              The tests verify the functionality of query construction,
#              setting fields, filters, limits, sorting, and handling various
#              edge cases. It ensures that the ZTeraDBQuery class correctly
#              handles different types of queries (SELECT, INSERT, UPDATE, DELETE)
#              and validates input arguments, query generation, and error handling.
#
# The file imports unittest, a testing framework, and other components that
# provide utilities for asserting conditions and checking the correctness
# of the ZTeraDBQuery class.
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

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from zteradb import ZTeraDBQuery, Sort, ZTeraDBQueryError
from zteradb.lib.zteradb_query_type import ZTeraDBQueryType

# Test Class for ZTeraDBQuery
# This test suite is designed to test the functionalities of the ZTeraDBQuery class,
# which is used to construct database queries with specific filters, fields,
# limits, and sorts. The tests verify if the methods work correctly and handle
# edge cases and errors.

class TestZTeraDBQuery(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        Initializes an instance of ZTeraDBQuery with a schema hash and database ID.
        """
        self.query = ZTeraDBQuery('my_schema_hash', 'database_id')

    def test_query_type_select(self):
        """
        Test that the `select()` method sets the query type to SELECT.

        This test checks if calling the `select()` method on the `query` object
        correctly updates the `query_type` attribute to the `ZTeraDBQueryType.SELECT`.
        It verifies that the `query_type` is set properly to the expected value, ensuring
        that the `select()` method functions as intended.
        """
        # Call the select() method on the query object
        self.query.select()

        # Assert that the query_type has been correctly set to SELECT
        # This will raise an assertion error if the query_type is not equal to ZTeraDBQueryType.SELECT
        self.assertEqual(self.query.query_type, ZTeraDBQueryType.SELECT, "should set query type to SELECT")

    def test_query_type_insert(self):
        """
        Test that the `insert()` method sets the query type to INSERT.

        This test verifies that calling the `insert()` method on the `query` object
        correctly updates the `query_type` attribute to `ZTeraDBQueryType.INSERT`.
        It ensures that the `insert()` method properly sets the query type to INSERT
        and functions as intended.

        Steps:
        1. Call the `insert()` method on the `query` object.
        2. Assert that the `query_type` is equal to `ZTeraDBQueryType.INSERT`.
        3. If the assertion fails, the test will raise an error with the message "should set query type to INSERT".
        """
        # Call the insert() method on the query object
        self.query.insert()

        # Assert that the query_type has been correctly set to INSERT
        # If query_type is not equal to ZTeraDBQueryType.INSERT, the test will fail
        self.assertEqual(self.query.query_type, ZTeraDBQueryType.INSERT, "should set query type to INSERT")

    def test_query_type_update(self):
        """
        Test that the `update()` method sets the query type to UPDATE.

        This test ensures that calling the `update()` method on the `query` object
        correctly updates the `query_type` attribute to `ZTeraDBQueryType.UPDATE`.
        It verifies that the `update()` method properly sets the query type to UPDATE
        and functions as intended.

        Steps:
        1. Call the `update()` method on the `query` object.
        2. Assert that the `query_type` is equal to `ZTeraDBQueryType.UPDATE`.
        3. If the assertion fails, the test will raise an error with the message "should set query type to UPDATE".
        """
        # Call the update() method on the query object
        self.query.update()

        # Assert that the query_type has been correctly set to UPDATE
        # If query_type is not equal to ZTeraDBQueryType.UPDATE, the test will fail
        self.assertEqual(self.query.query_type, ZTeraDBQueryType.UPDATE, "should set query type to UPDATE")

    def test_query_type_delete(self):
        """
        Test that the `delete()` method sets the query type to DELETE.

        This test ensures that calling the `delete()` method on the `query` object
        correctly updates the `query_type` attribute to `ZTeraDBQueryType.DELETE`.
        It verifies that the `delete()` method properly sets the query type to DELETE
        and functions as intended.

        Steps:
        1. Call the `delete()` method on the `query` object.
        2. Assert that the `query_type` is equal to `ZTeraDBQueryType.DELETE`.
        3. If the assertion fails, the test will raise an error with the message "should set query type to DELETE".
        """
        # Call the delete() method on the query object
        self.query.delete()

        # Assert that the query_type has been correctly set to DELETE
        # If query_type is not equal to ZTeraDBQueryType.DELETE, the test will fail
        self.assertEqual(self.query.query_type, ZTeraDBQueryType.DELETE, "should set query type to DELETE")

    def test_set_fields(self):
        """
        Test that the `fields()` method sets the fields correctly.

        This test ensures that calling the `fields()` method with keyword arguments
        correctly sets the fields in the query object. The test verifies that after
        calling `fields()`, the `fields()` method returns the correct dictionary with
        the expected field names and values.

        Steps:
        1. Call the `fields()` method on the `query` object with keyword arguments (field1=1, field2=1).
        2. Assert that the `fields()` method returns a dictionary with the correct field names and values.
        3. If the assertion fails, the test will raise an error with the message "should set the fields".
        """
        # Call the fields() method with field1 and field2 set to 1
        self.query.fields(field1=1, field2=1)

        # Assert that the fields() method returns a dictionary with the correct fields and values
        # If the fields dictionary does not match, the test will fail
        self.assertEqual(self.query.fields(), dict(field1=1, field2=1), "should set the fields")

    def test_set_fields_with_invalid_argument(self):
        """
        Test that the `fields()` method raises a TypeError when given invalid arguments.

        This test checks that the `fields()` method raises a `TypeError` when passed
        an incorrect number of positional arguments. It verifies that the method is
        expecting a specific number of arguments and will raise an error if that
        expectation is violated.

        Steps:
        1. Attempt to call the `fields()` method with a list containing one argument.
        2. Assert that a TypeError is raised with the expected error message.
        3. Attempt to call the `fields()` method with a list containing two arguments.
        4. Assert that a TypeError is raised again with the expected error message.
        """
        # Case 1: Pass a list with one argument to the fields method
        args = ["field"]
        with self.assertRaises(TypeError) as context:
            # Expecting TypeError when passing one positional argument
            self.query.fields(*args)

        # Assert that the exception message matches the expected error message
        self.assertEqual(str(context.exception), f"fields() takes 1 positional argument but {len(args) + 1} were given")

        # Case 2: Pass a list with two arguments to the fields method
        args = ["field1", "field2"]
        with self.assertRaises(TypeError) as context:
            # Expecting TypeError when passing two positional arguments
            self.query.fields(*args)

        # Assert that the exception message matches the expected error message
        self.assertEqual(str(context.exception), f"fields() takes 1 positional argument but {len(args) + 1} were given")

    def test_set_filters(self):
        """
        Test that the `filter()` method sets the filters correctly.

        This test ensures that calling the `filter()` method with keyword arguments
        correctly sets the filters in the query object. It verifies that after
        calling `filter()`, the `filters()` method returns the correct dictionary with
        the expected filter names and values.

        Steps:
        1. Call the `filter()` method on the `query` object with keyword arguments (field1=1, field2="hello").
        2. Assert that the `filters()` method returns a dictionary with the correct filter names and values.
        3. If the assertion fails, the test will raise an error with the message "should set the fields".
        """
        # Call the filter() method with field1 set to 1 and field2 set to "hello"
        self.query.filter(field1=1, field2="hello")

        # Assert that the filters() method returns a dictionary with the correct filters and values
        # If the filters dictionary does not match, the test will fail
        self.assertEqual(self.query.filters(), dict(field1=1, field2="hello"), "should set the fields")

    def test_set_filters_with_invalid_argument(self):
        """
        Test that the `filter()` method raises a TypeError when given invalid arguments.

        This test checks that the `filter()` method raises a `TypeError` when passed
        an incorrect number of positional arguments. It ensures that the method is
        expecting a specific number of arguments and will raise an error if that
        expectation is violated.

        Steps:
        1. Attempt to call the `filter()` method with a list containing one argument.
        2. Assert that a TypeError is raised with the expected error message.
        3. Attempt to call the `filter()` method with a list containing two arguments.
        4. Assert that a TypeError is raised again with the expected error message.
        """
        # Case 1: Pass a list with one argument to the filter method
        args = ["field"]
        with self.assertRaises(TypeError) as context:
            # Expecting TypeError when passing one positional argument
            self.query.filter(*args)

        # Assert that the exception message matches the expected error message
        self.assertEqual(str(context.exception), f"filter() takes 1 positional argument but {len(args) + 1} were given")

        # Case 2: Pass a list with two arguments to the filter method
        args = ["field1", "field2"]
        with self.assertRaises(TypeError) as context:
            # Expecting TypeError when passing two positional arguments
            self.query.filter(*args)

        # Assert that the exception message matches the expected error message
        self.assertEqual(str(context.exception), f"filter() takes 1 positional argument but {len(args) + 1} were given")

    def test_set_filters_empty(self):
        """
        Test that the `filter()` method sets empty filters correctly.

        This test checks that when the `filter()` method is called without any
        arguments, it correctly sets the filters to an empty dictionary. The test
        verifies that after calling `filter()` with no arguments, the `filters()`
        method returns an empty dictionary.

        Steps:
        1. Call the `filter()` method on the `query` object without any arguments.
        2. Assert that the `filters()` method returns an empty dictionary.
        3. If the assertion fails, the test will raise an error with the message "should set empty filters".
        """
        # Call the filter() method without any arguments
        self.query.filter()

        # Assert that the filters() method returns an empty dictionary
        # If the filters dictionary is not empty, the test will fail
        self.assertEqual(self.query.filters(), dict(), "should set empty filters")

    def test_set_sort(self):
        """
        Test that the `sort()` method sets the sort order correctly.

        This test ensures that calling the `sort()` method with keyword arguments
        correctly sets the sort order for the query. The test verifies that after
        calling `sort()`, the `get_sort()` method returns the correct dictionary
        with the expected sorting field names and values.

        Steps:
        1. Call the `sort()` method on the `query` object with one sort field (`field1=1`).
        2. Assert that the `get_sort()` method returns a dictionary with the correct field and sort order.
        3. Call the `sort()` method again with an additional sort field (`field2=-1`).
        4. Assert that the `get_sort()` method returns the updated dictionary with both fields and their sort orders.
        5. If any assertion fails, the test will raise an error with the message "should set sort order correctly".
        """
        # Case 1: Call sort() with field1 set to 1 (ascending order)
        self.query.sort(field1=1)
        # Assert that the sort order is correctly set to {field1: 1}
        self.assertEqual(self.query.get_sort(), dict(field1=1), "should set sort order correctly")

        # Case 2: Call sort() with field2 set to -1 (descending order)
        self.query.sort(field2=-1)
        # Assert that the sort order is updated to include field2 with -1 (descending)
        self.assertEqual(self.query.get_sort(), dict(field1=1, field2=-1), "should set sort order correctly")

    def test_set_limit(self):
        """
        Test that the `limit()` method sets the limit correctly.

        This test ensures that the `limit()` method is setting the limit for the query
        correctly. It verifies that calling `limit()` with different valid arguments
        updates the limit correctly and raises an error when invalid arguments are provided.

        Steps:
        1. Call the `limit()` method on the `query` object with valid limits (0, 10) and assert that `get_limit()` returns the correct value.
        2. Call the `limit()` method again with different valid limits (1000, 2000) and assert the returned value.
        3. Call the `limit()` method with invalid limits (0, 0), which should raise an exception.
        4. Assert that the exception raised has the correct message indicating the invalid limit.
        """
        # Case 1: Call limit() with valid limits (0, 10)
        self.query.limit(0, 10)
        # Assert that the limit is correctly set to (0, 10)
        self.assertEqual(self.query.get_limit(), (0, 10), "should set limit correctly")

        # Case 2: Call limit() with valid limits (1000, 2000)
        self.query.limit(1000, 2000)
        # Assert that the limit is correctly set to (1000, 2000)
        self.assertEqual(self.query.get_limit(), (1000, 2000), "should set limit correctly")

        # Case 3: Call limit() with invalid limits (0, 0)
        with self.assertRaises(Exception) as context:
            # Expecting an exception to be raised when limits are 0
            self.query.limit(0, 0)

        # Assert that the exception message is the expected one
        self.assertEqual(str(context.exception), "Limit '0' must be greater than 0")

    def test_invalid_limit_argument_types(self):
        """
        Test that the `limit()` method raises a ValueError when given invalid argument types.

        This test ensures that when the `limit()` method is called with incorrect argument types
        (i.e., arguments that are not instances of the expected `Limit` type), it raises a `ValueError`
        with the appropriate error message.

        Steps:
        1. Call the `limit()` method with invalid argument types (strings instead of integers or Limit objects).
        2. Assert that a `ValueError` is raised.
        3. Assert that the error message matches the expected message indicating the invalid argument type.
        """
        # Case 1: Call limit() with invalid argument types (strings instead of integers or Limit objects)
        with self.assertRaises(ValueError) as context:
            # Expecting a ValueError when non-numeric arguments are passed to limit()
            self.query.limit('invalid', 'value')

        # Assert that the exception message matches the expected message
        self.assertEqual(str(context.exception), "Limit 'invalid' must be an instance of the Limit")

    def test_generate_query(self):
        """
        Test that the `generate()` method correctly generates a query object based on method calls.

        This test ensures that when the `select()`, `fields()`, `filter()`, `sort()`, and `limit()` methods
        are chained together, the `generate()` method correctly produces the expected query object.

        Steps:
        1. Call the `select()` method to set the query type to SELECT.
        2. Call the `fields()` method to specify the fields to retrieve.
        3. Call the `filter()` method to set the filters for the query.
        4. Call the `sort()` method to set the sorting order.
        5. Call the `limit()` method to set the limit on the query.
        6. Generate the final query using `generate()`.
        7. Assert that the generated query matches the expected query object.
        """
        # Step 1: Call select() to set the query type to SELECT
        self.query.select()

        # Step 2: Set the fields to retrieve
        self.query.fields(field1=1)

        # Step 3: Set the filters for the query
        self.query.filter(field1="value")

        # Step 4: Set the sorting order
        self.query.sort(field1=1)

        # Step 5: Set the limit for the query
        self.query.limit(0, 10)

        # Step 6: Generate the final query object
        result = self.query.generate()

        # Expected query object
        expected_result = {
            'db': 'database_id',  # schema name
            'sh': 'my_schema_hash',  # schema name
            'qt': ZTeraDBQueryType.SELECT.value,  # Query type set to SELECT
            'fl': {'field1': 1},  # Fields (field1 set to 1)
            'fi': {'field1': 'value'},  # Filters (field1 set to 'value')
            'st': {'field1': Sort.ASC},  # Sort order (field1 sorted in ascending order)
            'lt': (0, 10)  # Limit (0 to 10)
        }

        # Step 7: Assert that the generated query matches the expected result
        self.assertEqual(result, expected_result, "should generate correct query")

    def test_throw_error_if_schema_name_not_set(self):
        """
        Test that an exception is raised if the schema name is not set when generating a query.

        This test ensures that if the `schema_name` is not provided during the instantiation of the query object,
        an exception is raised when the `generate()` method is called.

        Steps:
        1. Create a `ZTeraDBQuery` object without setting the `schema_name`.
        2. Attempt to call the `generate()` method on the query object.
        3. Assert that an exception is raised.
        4. Assert that the exception message correctly indicates that the `schema_name` argument is missing.
        """
        # Step 1: Create a ZTeraDBQuery object without setting the schema_name
        with self.assertRaises(Exception) as context:
            # Step 2: Attempt to generate a query without the schema_name set
            query = ZTeraDBQuery()
            query.generate()

        # Step 3: Assert that the exception raised is the one we expect
        # The expected exception message indicates that 'schema_name' is missing
        self.assertEqual(str(context.exception), "__init__() missing 1 required positional argument: 'schema_name'")

    def test_throw_error_if_query_type_not_set(self):
        """
        Test that a ZTeraDBQueryError is raised if the query type is not set before calling `generate()`.

        This test ensures that if the query type (e.g., SELECT, INSERT, UPDATE, DELETE) is not set
        by calling one of the methods like `select()`, `insert()`, `update()`, or `delete()`,
        an exception of type `ZTeraDBQueryError` is raised when attempting to generate the query.

        Steps:
        1. Create a `ZTeraDBQuery` object without setting the query type.
        2. Attempt to call the `generate()` method.
        3. Assert that a `ZTeraDBQueryError` exception is raised.
        4. Assert that the exception message is relevant to missing query type.
        """
        # Step 1: Create a ZTeraDBQuery object without setting the query type
        with self.assertRaises(ZTeraDBQueryError) as context:
            # Step 2: Attempt to generate a query without setting the query type
            self.query.generate()

        # Step 3: Assert that the exception raised is of type ZTeraDBQueryError
        # Step 4: Assert that the exception message matches the expected message about missing query type
        self.assertIsInstance(context.exception, ZTeraDBQueryError,
                              "You forgot to call either of select(), insert(), update() or delete() method.")

    def test_set_fields_for_select(self):
        """
        Test that fields are set correctly when the query type is SELECT.

        This test ensures that when the `select()` method is called, followed by `fields()`,
        the fields are correctly set for a SELECT query.

        Steps:
        1. Call `select()` to set the query type to SELECT.
        2. Call `fields()` to set the fields for the query.
        3. Assert that the fields are correctly set.
        4. Assert that the query type is correctly set to SELECT.
        """
        # Step 1: Call select() to set the query type to SELECT and then set fields
        self.query.select().fields(field1=1, field2=1)

        # Step 2: Assert that the fields were correctly set to {'field1': 1, 'field2': 1}
        self.assertEqual(self.query.fields(), dict(field1=1, field2=1), "should set fields correctly for SELECT")

        # Step 3: Assert that the query type is correctly set to SELECT
        self.assertEqual(self.query.query_type, ZTeraDBQueryType.SELECT, "should set fields correctly for SELECT")

    def test_set_fields_for_insert(self):
        """
        Test that fields are set correctly when the query type is INSERT.

        This test ensures that when the `insert()` method is called, followed by `fields()`,
        the fields are correctly set for an INSERT query.

        Steps:
        1. Call `insert()` to set the query type to INSERT.
        2. Call `fields()` to set the fields for the query.
        3. Assert that the fields are correctly set.
        4. Assert that the query type is correctly set to INSERT.
        """
        # Step 1: Call insert() to set the query type to INSERT and then set fields
        self.query.insert().fields(field1="hello", field2="world")

        # Step 2: Assert that the fields were correctly set to {'field1': 'hello', 'field2': 'world'}
        self.assertEqual(self.query.fields(), dict(field1="hello", field2="world"),
                         "should set fields correctly for INSERT")

        # Step 3: Assert that the query type is correctly set to INSERT
        self.assertEqual(self.query.query_type, ZTeraDBQueryType.INSERT,
                         "should set fields correctly for INSERT")

    def test_set_fields_for_update(self):
        """
        Test that fields are set correctly when the query type is UPDATE.

        This test ensures that when the `update()` method is called, followed by `fields()`,
        the fields are correctly set for an UPDATE query.

        Steps:
        1. Call `update()` to set the query type to UPDATE.
        2. Call `fields()` to set the fields for the query.
        3. Assert that the fields are correctly set.
        4. Assert that the query type is correctly set to UPDATE.
        """
        # Step 1: Call update() to set the query type to UPDATE and then set fields
        self.query.update().fields(field1="hello", field2="world")

        # Step 2: Assert that the fields were correctly set to {'field1': 'hello', 'field2': 'world'}
        self.assertEqual(self.query.fields(), dict(field1="hello", field2="world"),
                         "should set fields correctly for UPDATE")

        # Step 3: Assert that the query type is correctly set to UPDATE
        self.assertEqual(self.query.query_type, ZTeraDBQueryType.UPDATE,
                         "should set fields correctly for UPDATE")

    def test_set_fields_for_delete(self):
        """
        Test that fields are set correctly when the query type is DELETE.

        This test ensures that when the `delete()` method is called, followed by `fields()`,
        the fields are correctly set for a DELETE query.

        Steps:
        1. Call `delete()` to set the query type to DELETE.
        2. Call `fields()` to set the fields for the query.
        3. Assert that the fields are correctly set.
        4. Assert that the query type is correctly set to DELETE.
        """
        # Step 1: Call delete() to set the query type to DELETE and then set fields
        self.query.delete().fields(field1="hello", field2="world")

        # Step 2: Assert that the fields were correctly set to {'field1': 'hello', 'field2': 'world'}
        self.assertEqual(self.query.fields(), dict(field1="hello", field2="world"),
                         "should set fields correctly for DELETE")

        # Step 3: Assert that the query type is correctly set to DELETE
        self.assertEqual(self.query.query_type, ZTeraDBQueryType.DELETE,
                         "should set fields correctly for DELETE")

    def test_handle_nested_object_fields_for_insert(self):
        """
        Test that a ValueError is raised when nested objects are provided as fields for an INSERT query.

        This test ensures that if a nested object (e.g., dictionary) is passed as a field when performing
        an INSERT query, a ValueError is raised indicating that nested objects are not allowed.

        Steps:
        1. Call `insert()` to set the query type to INSERT.
        2. Call `fields()` with a nested object (e.g., dictionary) as one of the fields.
        3. Assert that a ValueError is raised with the correct error message.
        """
        # Step 1: Try to call insert() and set fields with a nested object (dictionary)
        with self.assertRaises(ValueError) as context:
            self.query.insert().fields(field1=dict(nestedField="value"))

        # Step 2: Assert that the exception is a ValueError with the correct message
        self.assertEqual(str(context.exception), "'{'nestedField': 'value'}' must not be any object.")

    def test_handle_complex_filters_for_select(self):
        """
        Test that ValueErrors are raised when complex filters (e.g., lists or dictionaries)
        are used as filter values for a SELECT query.

        This test ensures that when a filter field contains a list or dictionary as its value,
        a ValueError is raised indicating that these types of objects are not allowed in filters.

        Steps:
        1. Try to use a list as a filter value.
        2. Try to use a dictionary as a filter value.
        3. Assert that a ValueError is raised with the correct error message for each case.
        """
        # Step 1: Try using a list as a filter value and expect a ValueError
        with self.assertRaises(ValueError) as context:
            self.query.select().filter(field1=['value1', 'value2'], field2=dict(gt=10))

        # Assert that the exception is a ValueError with the correct message for lists in filters
        self.assertEqual(str(context.exception), "'['value1', 'value2']' must not be any object.")

        # Step 2: Try using a dictionary as a filter value and expect a ValueError
        with self.assertRaises(ValueError) as context:
            self.query.select().filter(**{'field1': 'value2', 'field2': {'gt': 10}})

        # Assert that the exception is a ValueError with the correct message for dictionaries in filters
        self.assertEqual(str(context.exception), "'{'gt': 10}' must not be any object.")

        # Step 3: Try using a combination of a list and a dictionary in filters and expect a ValueError
        with self.assertRaises(ValueError) as context:
            self.query.select().filter(**{'field1': ['value1', 'value2'], 'field2': {'$gt': 10}})

        # Assert that the exception is a ValueError with the correct message for lists in filters
        self.assertEqual(str(context.exception), "'['value1', 'value2']' must not be any object.")

    def test_handle_delete_with_complex_filters(self):
        """
        Test that a ValueError is raised when complex filters (e.g., dictionaries with operators like $in)
        are used in a DELETE query.

        This test ensures that when a filter contains a dictionary with complex operators like `$in`,
        a ValueError is raised indicating that such complex filter types are not allowed in DELETE queries.

        Steps:
        1. Try using a dictionary filter with the `$in` operator for a DELETE query.
        2. Assert that a ValueError is raised with the correct error message.
        """
        # Step 1: Try using a complex filter with the `$in` operator in a DELETE query
        with self.assertRaises(ValueError) as context:
            self.query.delete().filter(**{'field1': {'$in': ['value1', 'value2']}})

        # Step 2: Assert that the exception is a ValueError with the correct message for complex filters
        self.assertEqual(str(context.exception), "'{'$in': ['value1', 'value2']}' must not be any object.")

    def test_handle_update_with_nested_filters(self):
        """
        Test that a ValueError is raised when nested filters (e.g., dictionaries with operators like `lt`)
        are used in an UPDATE query.

        This test ensures that when a filter contains a nested dictionary (such as `{'lt': 100}`) in the `filter()`
        method for an UPDATE query, a ValueError is raised indicating that such filters are not allowed in UPDATE queries.

        Steps:
        1. Try using a nested dictionary filter (e.g., `{'lt': 100}`) in an UPDATE query.
        2. Assert that a ValueError is raised with the correct error message.
        """
        # Step 1: Try using a filter with a nested dictionary (`{'lt': 100}`) in an UPDATE query
        with self.assertRaises(ValueError) as context:
            self.query.update().fields(**{'field1': 'new_value'}).filter(**{'field2': {'lt': 100}})

        # Step 2: Assert that the exception is a ValueError with the correct message for nested filters
        self.assertEqual(str(context.exception), "'{'lt': 100}' must not be any object.")

    def test_handle_insert_with_null_fields(self):
        """
        Test that a ValueError is raised when `None` is used as a field value in an INSERT query.

        This test ensures that when a field is set to `None` (i.e., a NULL value) in an `INSERT` query,
        a ValueError is raised indicating that `None` is not allowed as a field value.

        Steps:
        1. Try setting a field (`field1`) to `None` in an `INSERT` query.
        2. Assert that a ValueError is raised with the correct error message.
        """
        # Step 1: Try using `None` as a field value in an INSERT query
        with self.assertRaises(ValueError) as context:
            self.query.insert().fields(**{'field1': None})

        # Step 2: Assert that the exception is a ValueError with the correct message for NULL fields
        self.assertEqual(str(context.exception), "'None' must not be any object.")

    def test_throw_error_with_null_schema_name(self):
        """
        Test that a ValueError is raised when the schema name is set to `None` while initializing a `ZTeraDBQuery`.

        This test ensures that when the schema name is not provided (i.e., `None`), a ValueError is raised with
        a message indicating that a schema name is required.

        Steps:
        1. Try initializing a `ZTeraDBQuery` with `None` as the schema name.
        2. Assert that a ValueError is raised with the correct error message.
        """
        # Step 1: Try initializing a ZTeraDBQuery with None as the schema name
        with self.assertRaises(ValueError) as context:
            ZTeraDBQuery(None)

        # Step 2: Assert that the exception is a ValueError with the correct message for null schema name
        self.assertEqual(str(context.exception), 'Schema name is required')

    def test_throw_error_with_integer_schema_name(self):
        """
        Test that a ValueError is raised when the schema name is provided as an integer while initializing a `ZTeraDBQuery`.

        This test ensures that when the schema name is an integer, a ValueError is raised indicating that the schema name
        must be a valid string and not an integer.

        Steps:
        1. Try initializing a `ZTeraDBQuery` with an integer schema name (`123`).
        2. Assert that a ValueError is raised with the correct error message.
        """
        # Step 1: Try initializing a ZTeraDBQuery with an integer as the schema name
        with self.assertRaises(ValueError) as context:
            ZTeraDBQuery(123)

        # Step 2: Assert that the exception is a ValueError with the correct message for invalid schema name
        self.assertEqual(str(context.exception), 'Schema name is required')

    def test_throw_error_with_schema_name_is_list(self):
        """
        Test that a ValueError is raised when the schema name is provided as a list while initializing a `ZTeraDBQuery`.

        This test ensures that when the schema name is provided as a list, a ValueError is raised indicating that the schema name
        must be a valid string and not a list.

        Steps:
        1. Try initializing a `ZTeraDBQuery` with a list as the schema name (`[123]`).
        2. Assert that a ValueError is raised with the correct error message.
        """
        # Step 1: Try initializing a ZTeraDBQuery with a list as the schema name
        with self.assertRaises(ValueError) as context:
            ZTeraDBQuery([123])

        # Step 2: Assert that the exception is a ValueError with the correct message for invalid schema name
        self.assertEqual(str(context.exception), 'Schema name is required')

    def test_throw_error_with_schema_name_is_dict(self):
        """
        Test that a ValueError is raised when the schema name is provided as a dictionary while initializing a `ZTeraDBQuery`.

        This test ensures that when the schema name is provided as a dictionary, a ValueError is raised indicating that the schema name
        must be a valid string and not a dictionary.

        Steps:
        1. Try initializing a `ZTeraDBQuery` with a dictionary as the schema name (`dict(schema_name="test")`).
        2. Assert that a ValueError is raised with the correct error message.
        """
        # Step 1: Try initializing a ZTeraDBQuery with a dictionary as the schema name
        with self.assertRaises(ValueError) as context:
            ZTeraDBQuery(dict(schema_name="test"))

        # Step 2: Assert that the exception is a ValueError with the correct message for invalid schema name
        self.assertEqual(str(context.exception), 'Schema name is required')

    def test_throw_error_for_insert_with_invalid_field_type(self):
        """
        Test that a ValueError is raised when an invalid field type is used in an `INSERT` query.

        This test ensures that when an invalid field type (such as a function) is provided for the fields in an `INSERT` query,
        a ValueError is raised.

        Steps:
        1. Try inserting a field with an invalid type (a lambda function).
        2. Assert that a ValueError is raised.
        """
        # Step 1: Try inserting a field with an invalid type (a lambda function)
        with self.assertRaises(ValueError) as context:
            self.query.insert().fields(**{'field1': lambda: {}})

        # Step 2: Assert that the exception raised is a ValueError
        self.assertTrue(isinstance(context.exception, ValueError))

    def test_handle_large_number_of_fields(self):
        """
        Test that the system can handle a large number of fields in a query.

        This test ensures that when a large number of fields (in this case, 1000 fields) are added to a query,
        the query can still generate the correct result, and the number of fields is accurately reflected.

        Steps:
        1. Create a large dictionary of fields (1000 fields).
        2. Add the fields to the query using the `fields` method.
        3. Generate the query and verify that the number of fields in the result is correct.
        """
        # Step 1: Create a large dictionary of fields (1000 fields)
        large_fields = {f'field{i}': 1 for i in range(1000)}

        # Step 2: Add the fields to the query
        self.query.select().fields(**large_fields)

        # Step 3: Generate the query and verify that the number of fields is correct
        result = self.query.generate()

        # Assert that the number of fields in the generated query is 1000
        self.assertEqual(len(result['fl']), 1000)

    def test_handle_large_number_of_filters(self):
        """
        Test that the system can handle a large number of filters in a query.

        This test ensures that when a large number of filters (in this case, 1000 filters) are added to a query,
        the query can still generate the correct result, and the number of filters is accurately reflected.

        Steps:
        1. Create a large dictionary of filters (1000 filters).
        2. Add the filters to the query using the `filter` method.
        3. Generate the query and verify that the number of filters in the result is correct.
        """
        # Step 1: Create a large dictionary of filters (1000 filters)
        large_fields = {f'field{i}': 1 for i in range(1000)}

        # Step 2: Add the filters to the query
        self.query.select().filter(**large_fields)

        # Step 3: Generate the query and verify that the number of filters is correct
        result = self.query.generate()

        # Assert that the number of filters in the generated query is 1000
        self.assertEqual(len(result['fi']), 1000)

    def test_not_accept_negative_limit_values(self):
        """
        Test that negative values for the limit are not accepted in the query.

        This test ensures that when negative values are passed for the limit, a `ValueError` is raised,
        and the correct error message is provided.

        Steps:
        1. Try setting the limit with a negative value for the first parameter.
        2. Try setting the limit with a negative value for the second parameter.
        3. Try setting the limit with negative values for both parameters.
        4. Assert that the correct `ValueError` is raised with the appropriate error message for each case.
        """
        # Step 1: Test that negative values for the first limit parameter raise an error
        with self.assertRaises(ValueError) as context:
            self.query.select().limit(-1, 5)
        self.assertEqual(str(context.exception), "Limit '-1' must not be negative")

        # Step 2: Test that negative values for the second limit parameter raise an error
        with self.assertRaises(ValueError) as context:
            self.query.select().limit(1, -5)
        self.assertEqual(str(context.exception), "Limit '-5' must be greater than 1")

        # Step 3: Test that negative values for both limit parameters raise an error
        with self.assertRaises(ValueError) as context:
            self.query.select().limit(-1, -5)
        self.assertEqual(str(context.exception), "Limit '-1' must not be negative")

    def test_handle_invalid_operator_in_select_filter(self):
        """
        Test that an invalid operator in a select filter raises an appropriate error.

        This test ensures that when an invalid operator (not supported by the system) is used in a filter
        for a `SELECT` query, a `ValueError` is raised with the correct error message.

        Steps:
        1. Try applying a filter with an invalid operator (e.g., `$unknownOp`).
        2. Assert that a `ValueError` is raised with the appropriate error message.
        """
        # Step 1: Try applying a filter with an invalid operator ('$unknownOp')
        with self.assertRaises(ValueError) as context:
            self.query.select().filter(**{'field1': {'$unknownOp': 'value'}})

        # Step 2: Assert that the exception raised is a ValueError with the correct message
        self.assertEqual(str(context.exception), "'{'$unknownOp': 'value'}' must not be any object.")

    def test_handle_combined_select_with_multiple_limits_and_sorts(self):
        """
        Test that the system correctly handles multiple limits and sorts in a SELECT query.

        This test ensures that when multiple `limit()` and `sort()` methods are called in succession,
        the query correctly handles the most recent values for sorting and limiting.

        Steps:
        1. Apply a `SELECT` query with a sort on 'field1' and a limit of (0, 10).
        2. Apply another limit (10, 20), which should override the previous one.
        3. Assert that the sort remains as expected.
        4. Assert that the final limit is correctly set to (10, 20).
        """
        # Step 1: Apply a SELECT query with a sort on 'field1' and a limit of (0, 10)
        self.query.select().sort(**{'field1': 1}).limit(0, 10).limit(10, 20)

        # Step 2: Assert that the sort order is still the one set initially ('field1' ASC)
        self.assertEqual(self.query.get_sort(), {'field1': Sort.ASC})

        # Step 3: Assert that the final limit is (10, 20), as the second limit call overrides the first
        self.assertEqual(self.query.get_limit(), (10, 20))


if __name__ == '__main__':
    unittest.main()
