# -----------------------------------------------------------------------------
# File: filter-conditions.py
# Description: This file contains the test cases for various filter conditions
#              used in the query construction. The tests verify the functionality
#              of multiple filter operations, including string-based filters
#              (icontains, startswith, endswith), mathematical comparisons
#              (greater than, less than, equal to), and logical operations
#              (AND, OR). The tests ensure that the filter conditions are
#              correctly applied, that invalid inputs raise appropriate errors,
#              and that valid inputs generate the expected filter structures.
#
# The file imports unittest, a testing framework, and defines a series of tests
# that check the proper handling of different filter operations, their
# arguments, and error scenarios.
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

from zteradb import ZTeraDBConditionError
from zteradb.zteradb_filter_functions import *

class TestZTeraDBFilterConditionFunctions(unittest.TestCase):
    """
    FilterConditionsTest class contains unit tests for validating the implementation
    of various filter operations used in query construction. This class ensures that
    the filters behave as expected by testing the core functionality, edge cases,
    and error handling for each filter operation.

    The tests verify the correct behavior of string-based filters (such as icontains,
    startswith, endswith, etc.), mathematical filters (greater than, less than, equal to),
    and logical operations (AND, OR). Each filter is tested to ensure proper argument
    validation, correct query generation, and appropriate error handling when given invalid inputs.

    The test methods in this class include:
    - Tests for valid filters, ensuring they generate the expected query format.
    - Tests for invalid input cases (e.g., incorrect data types or missing arguments),
      ensuring that appropriate exceptions are raised.
    - Edge cases for boundary conditions, ensuring robustness and stability.

    This class helps ensure the reliability and correctness of the filter condition
    operations by providing comprehensive coverage for a wide variety of potential use cases.

    Inheritance:
        - Inherits from `unittest.TestCase`, which provides the testing framework
          and assertion methods used in this class.
    """

    def test_addition_operation_should_throw_error_when_params_are_not_array(self):
        """
        Test that ZTADD throws the correct errors when invalid arguments are passed for the add operation.

        This test ensures that when incorrect or invalid parameters are passed to the ZTADD function,
        appropriate errors are raised. Specifically, the following cases are covered:
        - Passing non-list types (string, dictionary, etc.).
        - Passing a list with an invalid element type.
        - Passing a number instead of a list.
        - Not passing any arguments.

        Steps:
        1. Pass a string as the argument and check if ValueError is raised with the correct message.
        2. Pass a dictionary as the argument and check if ValueError is raised with the correct message.
        3. Pass a list with an invalid element and check if ValueError is raised with the correct message.
        4. Pass a number instead of a list and check if ValueError is raised with the correct message.
        5. Call ZTADD without any arguments and check if TypeError is raised with the correct message.
        """

        # Step 1: Test with a string argument (should raise ValueError)
        arg = "invalid"
        with self.assertRaises(ValueError) as context:
            ZTADD(arg)
        self.assertEqual(str(context.exception), f"'{arg}' must be list for add operation")

        # Step 2: Test with a dictionary argument (should raise ValueError)
        arg = {"x": 1, "y": 2}
        with self.assertRaises(ValueError) as context:
            ZTADD(arg)
        self.assertEqual(str(context.exception), f"'{arg}' must be list for add operation")

        # Step 3: Test with a list containing an invalid element (should raise ValueError)
        arg = [1, {"x": 1}]
        with self.assertRaises(ValueError) as context:
            ZTADD(arg)
        self.assertEqual(str(context.exception), f"Invalid '{arg[1]}' for add operation")

        # Step 4: Test with a number instead of a list (should raise ValueError)
        with self.assertRaises(ValueError) as context:
            ZTADD(123)
        self.assertEqual(str(context.exception), "'123' must be list for add operation")

        # Step 5: Test with no arguments passed to ZTADD (should raise TypeError)
        with self.assertRaises(TypeError) as context:
            ZTADD()
        self.assertEqual(str(context.exception), "ZTADD() missing 1 required positional argument: 'values'")

    def test_addition_operation_should_work(self):
        """
        Test that the addition operation works as expected when valid parameters are passed.

        This test ensures that when a valid list of operands is passed to the `ZTADD` function,
        the function correctly performs the addition operation and returns the expected result.
        Specifically, it checks whether the returned result contains the correct operator ('+')
        and the operands.

        Steps:
        1. Call `ZTADD` with a list of operands [1, 2].
        2. Check if the result of the addition operation has the correct 'operator' ('+')
           and the 'operand' ([1, 2]).
        3. Assert that the result matches the expected result.
        """

        # Step 1: Perform the addition operation with operands [1, 2]
        result = ZTADD([1, 2]).get_fields()

        # Step 2: Define the expected result with the operator '+' and the operands [1, 2]
        expected_result = {'operator': '+', 'operand': [1, 2]}

        # Step 3: Assert that the result of the operation matches the expected result
        self.assertEqual(result, expected_result, "addition operation should work")

    def test_subtraction_operation_should_throw_error_when_params_are_not_array(self):
        """
        Test that ZTSUB throws the correct errors when invalid arguments are passed for the subtraction operation.

        This test ensures that when incorrect or invalid parameters are passed to the ZTSUB function,
        appropriate errors are raised. Specifically, the following cases are covered:
        - Passing non-list types (string, dictionary, etc.).
        - Passing a list with an invalid element type.
        - Passing a number instead of a list.
        - Not passing any arguments.

        Steps:
        1. Pass a string as the argument and check if ValueError is raised with the correct message.
        2. Pass a dictionary as the argument and check if ValueError is raised with the correct message.
        3. Pass a list with an invalid element and check if ValueError is raised with the correct message.
        4. Pass a number instead of a list and check if ValueError is raised with the correct message.
        5. Call ZTSUB without any arguments and check if TypeError is raised with the correct message.
        """

        # Step 1: Test with a string argument (should raise ValueError)
        arg = "invalid"
        with self.assertRaises(ValueError) as context:
            ZTSUB(arg)
        self.assertEqual(str(context.exception), f"'{arg}' must be list for sub operation")

        # Step 2: Test with a dictionary argument (should raise ValueError)
        arg = {"x": 1, "y": 2}
        with self.assertRaises(ValueError) as context:
            ZTSUB(arg)
        self.assertEqual(str(context.exception), f"'{arg}' must be list for sub operation")

        # Step 3: Test with a list containing an invalid element (should raise ValueError)
        arg = [1, {"x": 1}]
        with self.assertRaises(ValueError) as context:
            ZTSUB(arg)
        self.assertEqual(str(context.exception), f"Invalid '{arg[1]}' for sub operation")

        # Step 4: Test with a number instead of a list (should raise ValueError)
        with self.assertRaises(ValueError) as context:
            ZTSUB(123)
        self.assertEqual(str(context.exception), "'123' must be list for sub operation")

        # Step 5: Test with no arguments passed to ZTSUB (should raise TypeError)
        with self.assertRaises(TypeError) as context:
            ZTSUB()
        self.assertEqual(str(context.exception), "ZTSUB() missing 1 required positional argument: 'values'")

    def test_subtraction_operation_should_work(self):
        """
        Test that the subtraction operation works as expected when valid parameters are passed.

        This test ensures that when a valid list of operands is passed to the `ZTSUB` function,
        it correctly performs the subtraction operation and returns the expected result.
        Specifically, it checks whether the returned result contains the correct operator ('-')
        and the operands.

        Steps:
        1. Call `ZTSUB` with a list of operands [1, 2].
        2. Check if the result of the subtraction operation has the correct 'operator' ('-')
           and the 'operand' ([1, 2]).
        3. Assert that the result matches the expected result.
        """

        # Step 1: Perform the subtraction operation with operands [1, 2]
        result = ZTSUB([1, 2]).get_fields()

        # Step 2: Define the expected result with the operator '-' and the operands [1, 2]
        expected_result = {'operator': '-', 'operand': [1, 2]}

        # Step 3: Assert that the result of the operation matches the expected result
        self.assertEqual(result, expected_result, "subtraction operation should work")

    def test_multiplication_operation_should_throw_error_when_params_are_not_array(self):
        """
        Test that ZTMUL throws the correct errors when invalid arguments are passed for the multiplication operation.

        This test ensures that when incorrect or invalid parameters are passed to the ZTMUL function,
        appropriate errors are raised. Specifically, the following cases are covered:
        - Passing non-list types (string, dictionary, etc.).
        - Passing a list with an invalid element type.
        - Passing a number instead of a list.
        - Not passing any arguments.

        Steps:
        1. Pass a string as the argument and check if ValueError is raised with the correct message.
        2. Pass a dictionary as the argument and check if ValueError is raised with the correct message.
        3. Pass a list with an invalid element and check if ValueError is raised with the correct message.
        4. Pass a number instead of a list and check if ValueError is raised with the correct message.
        5. Call ZTMUL without any arguments and check if TypeError is raised with the correct message.
        """

        # Step 1: Test with a string argument (should raise ValueError)
        arg = "invalid"
        with self.assertRaises(ValueError) as context:
            ZTMUL(arg)
        self.assertEqual(str(context.exception), f"'{arg}' must be list for mul operation")

        # Step 2: Test with a dictionary argument (should raise ValueError)
        arg = {"x": 1, "y": 2}
        with self.assertRaises(ValueError) as context:
            ZTMUL(arg)
        self.assertEqual(str(context.exception), f"'{arg}' must be list for mul operation")

        # Step 3: Test with a list containing an invalid element (should raise ValueError)
        arg = [1, {"x": 1}]
        with self.assertRaises(ValueError) as context:
            ZTMUL(arg)
        self.assertEqual(str(context.exception), f"Invalid '{arg[1]}' for mul operation")

        # Step 4: Test with a number instead of a list (should raise ValueError)
        with self.assertRaises(ValueError) as context:
            ZTMUL(123)
        self.assertEqual(str(context.exception), "'123' must be list for mul operation")

        # Step 5: Test with no arguments passed to ZTMUL (should raise TypeError)
        with self.assertRaises(TypeError) as context:
            ZTMUL()
        self.assertEqual(str(context.exception), "ZTMUL() missing 1 required positional argument: 'values'")

    def test_multiplication_operation_should_work(self):
        """
        Test that the multiplication operation works as expected when valid parameters are passed.

        This test ensures that when a valid list of operands is passed to the `ZTMUL` function,
        it correctly performs the multiplication operation and returns the expected result.
        Specifically, it checks whether the returned result contains the correct operator ('*')
        and the operands.

        Steps:
        1. Call `ZTMUL` with a list of operands [1, 2].
        2. Check if the result of the multiplication operation has the correct 'operator' ('*')
           and the 'operand' ([1, 2]).
        3. Assert that the result matches the expected result.
        """

        # Step 1: Perform the multiplication operation with operands [1, 2]
        result = ZTMUL([1, 2]).get_fields()

        # Step 2: Define the expected result with the operator '*' and the operands [1, 2]
        expected_result = {'operator': '*', 'operand': [1, 2]}

        # Step 3: Assert that the result of the operation matches the expected result
        self.assertEqual(result, expected_result, "multiplication operation should work")

    def test_divide_operation_should_throw_error_when_dividend_is_not_number_float_or_string(self):
        """
        Test that the division operation throws errors when invalid types are passed as arguments
        for the dividend or divisor.

        This test checks the following cases for the division operation:
        1. Ensure that missing arguments for the dividend and divisor raise appropriate errors.
        2. Ensure that invalid types for the dividend (non-numeric or non-field values) raise an error.
        3. Ensure that invalid types for the divisor (non-numeric or non-field values) raise an error.

        Test Cases:
        1. ZTDIV() with no arguments should raise a TypeError.
        2. ZTDIV(args) with only the dividend should raise a TypeError.
        3. ZTDIV(dividend, 100) where dividend is an invalid type should raise a ValueError.
        4. ZTDIV("x", {"y": 1}) with invalid divisor type should raise a ValueError.
        """

        # Step 1: Test ZTDIV() with missing arguments (should raise TypeError)
        with self.assertRaises(TypeError) as context:
            ZTDIV()

        # Ensure the correct error message is raised for missing arguments
        self.assertEqual(str(context.exception),
                         "ZTDIV() missing 2 required positional arguments: 'dividend' and 'divisor'")

        # Step 2: Test ZTDIV(args) with only the dividend (should raise TypeError)
        args = {"x": 1}
        with self.assertRaises(TypeError) as context:
            ZTDIV(args)

        # Ensure the correct error message is raised for missing the divisor
        self.assertEqual(str(context.exception), "ZTDIV() missing 1 required positional argument: 'divisor'")

        # Step 3: Test ZTDIV with an invalid dividend type (should raise ValueError)
        args = ({"y": 1}, 100)
        with self.assertRaises(ValueError) as context:
            ZTDIV(*args)

        # Ensure the correct error message is raised for invalid dividend type
        self.assertEqual(str(context.exception), "'dividend' must be numeric or schema field.")

        # Step 4: Test ZTDIV with an invalid divisor type (should raise ValueError)
        args = ("x", {"y": 1})
        with self.assertRaises(ValueError) as context:
            ZTDIV(*args)

        # Ensure the correct error message is raised for invalid divisor type
        self.assertEqual(str(context.exception), "'divisor' must be numeric or schema field.")

    def test_divide_operation_should_work(self):
        """
        Test that the division operation works correctly for valid arguments.

        This test checks the following cases for the division operation (ZTDIV):
        1. Ensure that dividing a schema field (e.g., "price") by a number works as expected.
        2. Ensure that dividing two numeric values works as expected.

        Test Cases:
        1. Dividing a schema field "price" by 10 should result in a valid operator and operand.
        2. Dividing numeric values (200 and 10) should result in a valid operator and operand.
        """

        # Step 1: Test division with a schema field ("price") and a numeric value (10)
        result = ZTDIV("price", 10).get_fields()
        expected_result = {"operator": "/", "operand": ["price", 10]}
        # Ensure the result is as expected
        self.assertEqual(result, expected_result, "divide operation should work")

        # Step 2: Test division with two numeric values (200 and 10)
        result = ZTDIV(200, 10).get_fields()
        expected_result = {"operator": "/", "operand": [200, 10]}
        # Ensure the result is as expected
        self.assertEqual(result, expected_result, "divide operation should work")

    def test_modulo_operation_should_throw_error_when_dividend_is_not_number_float_or_string(self):
        """
        Test that the modulo operation (ZTMOD) throws errors when the numerator or denominator
        is invalid. The numerator and denominator must be either a number (int/float), a schema field,
        and the denominator must be greater than 0.

        This test checks the following cases:
        1. Missing arguments (numerator or denominator).
        2. Invalid types for numerator and denominator (e.g., dictionary or other non-numeric types).
        3. Invalid values for the denominator (e.g., less than or equal to 0).
        """

        # Case 1: No arguments passed, should raise TypeError
        with self.assertRaises(TypeError) as context:
            ZTMOD()  # Missing arguments: numerator and denominator
        self.assertEqual(str(context.exception),
                         "ZTMOD() missing 2 required positional arguments: 'numerator' and 'denominator'")

        # Case 2: Only numerator is passed, should raise TypeError for missing denominator
        args = {"x": 1}  # Invalid argument (non-numeric and non-schema field)
        with self.assertRaises(TypeError) as context:
            ZTMOD(args)  # Missing denominator
        self.assertEqual(str(context.exception),
                         "ZTMOD() missing 1 required positional argument: 'denominator'")

        # Case 3: Invalid numerator, should raise ValueError for invalid numerator
        args = ({"y": 1}, 100)  # Invalid numerator (dict), valid denominator (100)
        with self.assertRaises(ValueError) as context:
            ZTMOD(*args)
        self.assertEqual(str(context.exception),
                         "'numerator' must be numeric or schema field.")

        # Case 4: Invalid denominator, should raise ValueError for invalid denominator
        args = ("x", {"y": 1})  # Valid numerator ("x"), invalid denominator (dict)
        with self.assertRaises(ValueError) as context:
            ZTMOD(*args)
        self.assertEqual(str(context.exception),
                         "'denominator' must be numeric or schema field and must be greater than 0")

    def test_modulo_operation_should_work(self):
        """
        Test that the modulo operation (ZTMOD) works as expected when valid operands are provided.
        The modulo operation should take two operands, the numerator and the denominator,
        and return the correct result in the format:
        {'operator': '%', 'operand': [numerator, denominator]}.

        This test verifies that the modulo operation works with:
        1. String schema field as the numerator and a number as the denominator.
        2. Numbers as both the numerator and the denominator.
        """

        # Case 1: Valid modulo operation with a schema field ("price") as the numerator
        result = ZTMOD("price", 10).get_fields()
        expected_result = {"operator": "%", "operand": ["price", 10]}
        self.assertEqual(result, expected_result, "modulo operation should work")

        # Case 2: Valid modulo operation with numeric values for both numerator and denominator
        result = ZTMOD(200, 10).get_fields()
        expected_result = {"operator": "%", "operand": [200, 10]}
        self.assertEqual(result, expected_result, "modulo operation should work")

    def test_schema_field_contains_some_value_should_throw_error_when_schema_field_is_not_string(self):
        """
        Test that the ZTCONTAINS operation throws the appropriate errors when invalid inputs
        are provided for the field and value arguments. This test ensures that:

        1. If the `value` argument is missing, the function throws a `TypeError`.
        2. If an unexpected keyword argument is passed (such as a dictionary), the function throws a `TypeError`.
        3. If the `field` argument is not a valid field name in the `ZTCONTAINS` filter, a `ValueError` is thrown.
        4. If the `value` argument is not a string, a `ValueError` is thrown.

        This test ensures that `ZTCONTAINS` correctly validates its inputs before proceeding with the operation.
        """

        # Case 1: No 'value' argument passed, should raise TypeError with a descriptive message
        with self.assertRaises(TypeError) as context:
            ZTCONTAINS({"x": 1})  # Passing a dictionary instead of a value
        self.assertEqual(str(context.exception), "ZTCONTAINS() missing 1 required positional argument: 'value'")

        # Case 2: Passing a dictionary as keyword argument which is not expected by ZTCONTAINS
        with self.assertRaises(TypeError) as context:
            ZTCONTAINS(**{"x": 1})  # This should raise TypeError due to invalid keyword argument
        self.assertEqual(str(context.exception), "ZTCONTAINS() got an unexpected keyword argument 'x'")

        # Case 3: 'field' argument is not a valid field name, it should raise a ValueError
        with self.assertRaises(ValueError) as context:
            ZTCONTAINS(field=1, value="a")  # Field should be a string, but it's an integer
        self.assertEqual(str(context.exception), "The `field` argument must be field name in contains filter.")

        # Case 4: 'value' argument is not a string, should raise a ValueError
        with self.assertRaises(ValueError) as context:
            ZTCONTAINS(field="a", value=1)  # The value should be a string, but it's an integer
        self.assertEqual(str(context.exception), "The `value` argument must be string in contains filter.")

    def test_schema_field_contains_some_value_should_work(self):
        """
        Test that the ZTCONTAINS operation works correctly when valid inputs are provided for
        the 'field' and 'value' arguments. This test ensures that:

        1. The `ZTCONTAINS` operation correctly constructs the query with the appropriate
           operator ('%%'), operand (field), and result (value).
        2. It verifies that the function properly processes the 'field' and 'value' arguments
           and returns the expected result.

        This test ensures that the `ZTCONTAINS` operation behaves as expected when valid
        inputs are used.
        """

        # Case: Passing valid field ("name") and value ("mouse")
        result = ZTCONTAINS("name", "mouse").get_fields()

        # Expected result: The operator is '%%', operand is 'name', and result is 'mouse'
        expected_result = {"operator": "%%", "operand": "name", "result": "mouse"}

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    def test_schema_field_icontains_some_value_should_throw_error_when_schema_field_is_not_string(self):
        """
        Test that the ZTICONTAINS operation raises the correct errors when invalid inputs
        are provided for the 'field' and 'value' arguments. This test ensures that:

        1. The function raises a TypeError when the required positional argument 'value' is
           missing.
        2. The function raises a TypeError when an unexpected keyword argument is passed.
        3. The function raises a ValueError when the 'field' argument is not a valid field name
           for an 'icontains' operation.
        4. The function raises a ValueError when the 'value' argument is not a string for an
           'icontains' operation.

        This test ensures that the `ZTICONTAINS` operation enforces input validation properly.
        """

        # Case 1: Missing 'value' argument
        with self.assertRaises(TypeError) as context:
            ZTICONTAINS({"x": 1})  # Invalid argument type passed to the function
        self.assertEqual(str(context.exception), "ZTICONTAINS() missing 1 required positional argument: 'value'")

        # Case 2: Unexpected keyword argument
        with self.assertRaises(TypeError) as context:
            ZTICONTAINS(**{"x": 1})  # Unexpected keyword argument 'x'
        self.assertEqual(str(context.exception), "ZTICONTAINS() got an unexpected keyword argument 'x'")

        # Case 3: 'field' argument is not a valid field name for 'icontains' filter
        with self.assertRaises(ValueError) as context:
            ZTICONTAINS(field=1, value="a")  # 'field' argument should be a string (field name)
        self.assertEqual(str(context.exception), "The `field` argument must be field name in icontains filter.")

        # Case 4: 'value' argument is not a string
        with self.assertRaises(ValueError) as context:
            ZTICONTAINS(field="a", value=1)  # 'value' argument should be a string
        self.assertEqual(str(context.exception), "The `value` argument must be string in icontains filter.")

    def test_schema_field_icontains_some_value_should_work(self):
        """
        Test that the ZTICONTAINS operation works correctly when valid inputs are provided
        for the 'field' and 'value' arguments. This test ensures that:

        1. The function properly constructs the query with the 'operator' set to "i%%",
           the 'operand' set to the provided field name, and the 'result' set to the provided value.
        2. The query reflects the case-insensitive 'contains' operation on the given field and value.

        This test ensures that the `ZTICONTAINS` operation is correctly implemented and generates
        the expected result.
        """

        # Valid inputs for field and value arguments
        result = ZTICONTAINS("name", "mouse").get_fields()  # 'name' is the field, 'mouse' is the value

        # The expected query result with operator 'i%%' (case-insensitive contains operator)
        expected_result = {"operator": "i%%", "operand": "name", "result": "mouse"}

        # Assert that the generated result matches the expected result
        self.assertEqual(result, expected_result, "icontains operation should work correctly with valid inputs")

    def test_schema_field_starts_with_some_value_should_throw_error_when_schema_field_is_not_string(self):
        """
        Test that the ZTSTARTSWITH operation throws appropriate errors when invalid inputs are provided
        for the 'field' and 'value' arguments. This test ensures that:

        1. If the 'field' is not a valid string, a ValueError is raised indicating that the `field`
           must be the field name in the starts with filter.
        2. If the 'value' is not a valid string, a ValueError is raised indicating that the `value`
           must be a string in the starts with filter.
        3. If invalid or missing arguments are passed to the function, it raises the correct errors,
           such as TypeError or ValueError.

        This test helps ensure that the ZTSTARTSWITH function properly validates its inputs.
        """

        # Test case 1: Passing a dictionary instead of a string for the field
        with self.assertRaises(TypeError) as context:
            ZTSTARTSWITH({"x": 1})
        self.assertEqual(str(context.exception), "ZTSTARTSWITH() missing 1 required positional argument: 'value'")

        # Test case 2: Passing invalid keyword arguments
        with self.assertRaises(TypeError) as context:
            ZTSTARTSWITH(**{"x": 1})
        self.assertEqual(str(context.exception), "ZTSTARTSWITH() got an unexpected keyword argument 'x'")

        # Test case 3: Passing an invalid type for the 'field' argument
        with self.assertRaises(ValueError) as context:
            ZTSTARTSWITH(field=1, value="a")
        self.assertEqual(str(context.exception), "The `field` argument must be field name in starts with filter.")

        # Test case 4: Passing an invalid type for the 'value' argument
        with self.assertRaises(ValueError) as context:
            ZTSTARTSWITH(field="a", value=1)
        self.assertEqual(str(context.exception), "The `value` argument must be string in starts with filter.")

    def test_schema_field_starts_with_some_value_should_work(self):
        """
        Test that the ZTSTARTSWITH operation works correctly when valid inputs are provided for
        the `field` and `value` arguments. This test ensures that:

        1. If a valid field name (string) and value (string) are provided, the `ZTSTARTSWITH`
           function should correctly create the expected result.
        2. The result should have the correct operator (`^%%`) and correct operand and result fields.

        This test helps confirm that the ZTSTARTSWITH operation generates the correct query representation
        when valid inputs are used.
        """

        # Performing the starts-with operation with valid inputs for field and value
        result = ZTSTARTSWITH("name", "mouse").get_fields()

        # Expected result for a valid 'field' and 'value'
        expected_result = {"operator": "^%%", "operand": "name", "result": "mouse"}

        # Assert that the result generated by ZTSTARTSWITH matches the expected result
        self.assertEqual(result, expected_result)

    def test_schema_field_istarts_with_some_value_should_throw_error_when_schema_field_is_not_string(self):
        """
        Test that the ZTISTARTSWITH operation throws the correct errors when invalid inputs are provided for
        the `field` and `value` arguments. This test ensures the following error scenarios:

        1. If no field is provided, a missing argument error should be raised.
        2. If an unexpected keyword argument is provided, an error should be raised.
        3. If the field is not a valid field name (i.e., not a string), a ValueError should be raised.
        4. If the value is not a string, a ValueError should be raised.

        This test helps to ensure that the ZTISTARTSWITH operation is robust and handles input validation correctly.
        """

        # Test case where 'field' is not a string (invalid type)
        with self.assertRaises(TypeError) as context:
            ZTISTARTSWITH({"x": 1})  # field should be a string, but it's a dictionary.
        self.assertEqual(str(context.exception), "ZTISTARTSWITH() missing 1 required positional argument: 'value'")

        # Test case with unexpected keyword argument
        with self.assertRaises(TypeError) as context:
            ZTISTARTSWITH(**{"x": 1})  # passing a dictionary as kwargs instead of positional arguments.
        self.assertEqual(str(context.exception), "ZTISTARTSWITH() got an unexpected keyword argument 'x'")

        # Test case where field is not a valid field name (it should be a string)
        with self.assertRaises(ValueError) as context:
            ZTISTARTSWITH(field=1, value="a")  # field should be a string, but it's an integer.
        self.assertEqual(str(context.exception), "The `field` argument must be field name in istarts with filter.")

        # Test case where value is not a string
        with self.assertRaises(ValueError) as context:
            ZTISTARTSWITH(field="a", value=1)  # value should be a string, but it's an integer.
        self.assertEqual(str(context.exception), "The `value` argument must be string in istarts with filter.")

    def test_schema_field_istarts_with_some_value_should_work(self):
        """
        Test that the ZTISTARTSWITH operation works correctly when provided with valid `field` and `value` arguments.
        The following behavior is tested:

        1. The `field` argument must be a string representing the field name.
        2. The `value` argument must be a string that the field is checked against.
        3. The operator used for this filter is case-insensitive "starts with" (`^i%%`).

        This test checks that the correct operator and operands are returned by the `ZTISTARTSWITH` operation.
        """

        # Create the operation with a valid field name and value.
        result = ZTISTARTSWITH("name", "mouse").get_fields()

        # Define the expected result.
        expected_result = {"operator": "^i%%", "operand": "name", "result": "mouse"}

        # Assert that the result of the operation matches the expected result.
        self.assertEqual(result, expected_result)

    def test_schema_field_endss_with_some_value_should_throw_error_when_schema_field_is_not_string(self):
        """
        Test that the ZTENDSWITH operation throws appropriate errors when invalid `field` or `value` arguments are provided.

        This test checks the following error conditions:

        1. Missing required positional argument: `value`.
        2. Unexpected keyword argument: The `field` and `value` should be properly passed as arguments.
        3. Invalid `field`: The `field` argument must be a valid field name, not a numeric or incorrect type.
        4. Invalid `value`: The `value` argument must be a string to use in the "ends with" filter.

        The following scenarios are tested:
        - Missing value argument for ZTENDSWITH.
        - Unexpected keyword argument for ZTENDSWITH.
        - Invalid field (not a string).
        - Invalid value (not a string).
        """

        # Test 1: Missing required positional argument 'value'
        with self.assertRaises(TypeError) as context:
            ZTENDSWITH({"x": 1})
        self.assertEqual(str(context.exception), "ZTENDSWITH() missing 1 required positional argument: 'value'")

        # Test 2: Unexpected keyword argument 'x'
        with self.assertRaises(TypeError) as context:
            ZTENDSWITH(**{"x": 1})
        self.assertEqual(str(context.exception), "ZTENDSWITH() got an unexpected keyword argument 'x'")

        # Test 3: Invalid field argument (numeric instead of string)
        with self.assertRaises(ValueError) as context:
            ZTENDSWITH(field=1, value="a")
        self.assertEqual(str(context.exception), "The `field` argument must be field name in ends with filter.")

        # Test 4: Invalid value argument (not a string)
        with self.assertRaises(ValueError) as context:
            ZTENDSWITH(field="a", value=1)
        self.assertEqual(str(context.exception), "The `value` argument must be string in ends with filter.")

    def test_schema_field_starts_with_some_value_should_work(self):
        """
        Test that the ZTENDSWITH operation works correctly when valid `field` and `value` arguments are provided.

        This test ensures that the 'ZTENDSWITH' filter correctly formats and returns the expected result when:

        1. The `field` argument is a valid schema field.
        2. The `value` argument is a string.

        The operation is tested with:
        - A valid field (`"name"`) and a valid value (`"mouse"`).

        Expected result:
        The returned fields should include an operator (`%%$`), the operand (`"name"`), and the result (`"mouse"`).
        """

        result = ZTENDSWITH("name", "mouse").get_fields()
        expected_result = {"operator": "%%$", "operand": "name", "result": "mouse"}
        self.assertEqual(result, expected_result, "ZTENDSWITH operation should work correctly")

    def test_schema_field_iends_with_some_value_should_throw_error_when_schema_field_is_not_string(self):
        """
        Test that the ZTIENDSWITH operation throws errors when invalid arguments are provided for `field` or `value`.

        This test ensures that the 'ZTIENDSWITH' filter correctly raises exceptions in the following cases:

        1. When `field` is not provided.
        2. When `field` is an unexpected argument or invalid.
        3. When the `field` is not a string (non-schema field).
        4. When the `value` is not a string.

        The test verifies error handling for:
        - Missing required arguments.
        - Unexpected keyword arguments.
        - Invalid types for `field` and `value`.
        """

        # Case 1: Field argument is a dictionary instead of a string
        with self.assertRaises(TypeError) as context:
            ZTIENDSWITH({"x": 1})

        self.assertEqual(str(context.exception), "ZTIENDSWITH() missing 1 required positional argument: 'value'")

        # Case 2: Field is provided as an invalid keyword argument
        with self.assertRaises(TypeError) as context:
            ZTIENDSWITH(**{"x": 1})

        self.assertEqual(str(context.exception), "ZTIENDSWITH() got an unexpected keyword argument 'x'")

        # Case 3: Field is an integer instead of a string (invalid field name)
        with self.assertRaises(ValueError) as context:
            ZTIENDSWITH(field=1, value="a")

        self.assertEqual(str(context.exception), "The `field` argument must be field name in iends with filter.")

        # Case 4: Value is an integer instead of a string (invalid value)
        with self.assertRaises(ValueError) as context:
            ZTIENDSWITH(field="a", value=1)

        self.assertEqual(str(context.exception), "The `value` argument must be string in iends with filter.")

    def test_schema_field_iends_with_some_value_should_work(self):
        """
        Test that the 'IENDSWITH' operation (ZTENDSWITH) works correctly when valid `field` and `value` arguments are provided.

        This test checks the correct behavior of the 'IENDSWITH' operation when:

        1. The `field` argument is a valid field name (a string).
        2. The `value` argument is a valid string (for the "iends with" filter).

        The following scenarios are tested:
        - Valid field name and valid value string for the IENDSWITH operation.

        Expected result:
        - The 'IENDSWITH' operation is performed with the field and value, and the result matches the expected format:
          - operator: 'i%%$' (for case-insensitive "ends with").
          - operand: the provided field.
          - result: the provided value string.
        """
        # Case: Field is "name" and value is "mouse"
        result = ZTIENDSWITH("name", "mouse").get_fields()

        # Expected result should include the correct operator and the correct field and value
        expected_result = {"operator": "i%%$", "operand": "name", "result": "mouse"}

        # Assert that the result from the function matches the expected result
        self.assertEqual(result, expected_result, "iends with operation should work")

    def test_greater_than_operation_should_throw_error_when_params_are_invalid(self):
        """
        Test that the 'Greater Than' operation (ZTGT) throws appropriate errors when invalid parameters are provided.

        This test checks the following error conditions:

        1. Invalid parameter type: The filter params must be a list.
        2. Missing required positional argument: The params should be properly passed as arguments.
        3. Invalid type of params: The params should be a list, not a single value.

        The following scenarios are tested:
        - Invalid type for the params (e.g., passing a string instead of a list).
        - Missing params argument.
        - Incorrect type for individual items inside the params (e.g., non-list types).

        Expected error messages:
        - "The 'Greater than' filter params must be list" when an invalid type is passed.
        - "ZTGT() missing 1 required positional argument: 'params'" when the params are missing.
        """
        # Case 1: Invalid parameter type (string)
        with self.assertRaises(ValueError) as context:
            ZTGT("invalid")
        self.assertEqual(str(context.exception), "The 'Greater than' filter params must be list")

        # Case 2: Invalid parameter type (dictionary)
        with self.assertRaises(ValueError) as context:
            ZTGT({"x": 1})
        self.assertEqual(str(context.exception), "The 'Greater than' filter params must be list")

        # Case 3: Invalid parameter type (integer)
        with self.assertRaises(ValueError) as context:
            ZTGT(123)
        self.assertEqual(str(context.exception), "The 'Greater than' filter params must be list")

        # Case 4: Missing parameter (no arguments passed)
        with self.assertRaises(TypeError) as context:
            ZTGT()
        self.assertEqual(str(context.exception), "ZTGT() missing 1 required positional argument: 'params'")

    def test_greater_than_operation_should_work(self):
        """
        Test that the 'Greater Than' operation (ZTGT) works as expected with valid parameters.

        This test checks that the operation correctly processes valid inputs, including field names and numeric values.

        The following scenarios are tested:
        - Using two field names: The operation should compare two fields (e.g., "price" and "quantity").
        - Using a field name and a numeric value: The operation should compare a field against a number (e.g., "price" vs. 10).
        - Using two numeric values: The operation should compare two numeric values.

        The expected behavior is that the `get_fields` method should return the correct operator (`>`) and operands.

        Expected output for the test:
        - ZTGT(["price", "quantity"]) returns {"operator": ">", "operand": ["price", "quantity"]}.
        - ZTGT(["price", 10]) returns {"operator": ">", "operand": ["price", 10]}.
        - ZTGT([200, 100]) returns {"operator": ">", "operand": [200, 100]}.
        """
        # Case 1: Both parameters are field names (strings)
        result = ZTGT(["price", "quantity"]).get_fields()
        expected_result = {"operator": ">", "operand": ["price", "quantity"]}
        self.assertEqual(result, expected_result, "greater than operation should work")

        # Case 2: One parameter is a field name (string) and the other is a numeric value
        result = ZTGT(["price", 10]).get_fields()
        expected_result = {"operator": ">", "operand": ["price", 10]}
        self.assertEqual(result, expected_result, "greater than operation should work")

        # Case 3: Both parameters are numeric values
        result = ZTGT([200, 100]).get_fields()
        expected_result = {"operator": ">", "operand": [200, 100]}
        self.assertEqual(result, expected_result, "greater than operation should work")

    def test_greater_than_or_equal_operation_should_throw_error_when_params_are_invalid(self):
        """
        Test that the 'Greater Than or Equal' operation (ZTGTE) throws appropriate errors when invalid parameters are provided.

        This test checks the following error conditions:

        1. Invalid type for parameters: The 'Greater Than or Equal' operation should only accept a list as its parameters.
        2. Missing required positional argument: The operation should raise an error if no parameters are provided.
        3. Invalid types in the list: If the parameters provided are not a list or contain unsupported types (like dictionaries or integers), the operation should throw a ValueError.

        The following scenarios are tested:
        - Invalid parameter type (e.g., string or integer passed instead of list).
        - Missing parameters.
        - Invalid parameter types inside the list (e.g., dictionary, integers).

        The expected exceptions are:
        - `ValueError` for invalid parameter types (must be a list).
        - `TypeError` for missing required parameters.
        """
        # Case 1: Invalid parameter (string instead of list)
        with self.assertRaises(ValueError) as context:
            ZTGTE("invalid")
        self.assertEqual(str(context.exception), "The 'Greater than or equal' filter params must be list")

        # Case 2: Invalid parameter (dictionary instead of list)
        with self.assertRaises(ValueError) as context:
            ZTGTE({"x": 1})
        self.assertEqual(str(context.exception), "The 'Greater than or equal' filter params must be list")

        # Case 3: Invalid parameter (integer instead of list)
        with self.assertRaises(ValueError) as context:
            ZTGTE(123)
        self.assertEqual(str(context.exception), "The 'Greater than or equal' filter params must be list")

        # Case 4: Missing parameter (no arguments passed)
        with self.assertRaises(TypeError) as context:
            ZTGTE()
        self.assertEqual(str(context.exception), "ZTGTE() missing 1 required positional argument: 'params'")

    def test_greater_than_or_equal_operation_should_work(self):
        """
        Test that the 'Greater Than or Equal' operation (ZTGTE) works correctly when valid parameters are provided.

        This test ensures that the operation performs as expected when provided with valid operands and parameters.

        The following scenarios are tested:
        - Two valid fields (e.g., field names such as 'price' and 'quantity') are passed and processed correctly.
        - A valid field and numeric value are passed, ensuring the filter operates between a field and a numeric value.
        - Two numeric values are passed, and the operation works as expected.

        The expected output is a dictionary containing the correct operator (">=") and the operands.
        """
        # Case 1: Valid parameters with two fields
        result = ZTGTE(["price", "quantity"]).get_fields()
        expected_result = {"operator": ">=", "operand": ["price", "quantity"]}
        self.assertEqual(result, expected_result, "Greater than or equal operation should work")

        # Case 2: Valid parameters with a field and a constant
        result = ZTGTE(["price", 10]).get_fields()
        expected_result = {"operator": ">=", "operand": ["price", 10]}
        self.assertEqual(result, expected_result, "Greater than or equal operation should work")

        # Case 3: Valid parameters with two constants
        result = ZTGTE([200, 100]).get_fields()
        expected_result = {"operator": ">=", "operand": [200, 100]}
        self.assertEqual(result, expected_result, "Greater than or equal operation should work")

    def test_less_than_operation_should_throw_error_when_params_are_invalid(self):
        """
        Test that the 'Less Than' operation (ZTLT) throws appropriate errors when invalid parameters are provided.

        This test checks the following error conditions:

        1. Invalid parameter type: The params must be a list, and passing other types (such as strings, dicts, or numbers) should raise an error.
        2. Missing parameters: The operation requires two parameters to compare, and a missing parameter should trigger an error.
        3. Incorrect number of parameters: The operation expects exactly two operands for comparison.

        The following scenarios are tested:
        - Invalid parameter types (e.g., a string or dictionary is passed instead of a list).
        - Missing parameters (i.e., when no params are provided).
        - Invalid values passed as parameters (i.e., a single number passed instead of a list).
        """
        # Case 1: Invalid input of type string (not a list)
        with self.assertRaises(ValueError) as context:
            ZTLT("invalid")
        self.assertEqual(str(context.exception), "The 'Less than' filter params must be list")

        # Case 2: Invalid input of type dictionary (not a list)
        with self.assertRaises(ValueError) as context:
            ZTLT({"x": 1})
        self.assertEqual(str(context.exception), "The 'Less than' filter params must be list")

        # Case 3: Invalid input of type integer (not a list)
        with self.assertRaises(ValueError) as context:
            ZTLT(123)
        self.assertEqual(str(context.exception), "The 'Less than' filter params must be list")

        # Case 4: Missing required positional argument
        with self.assertRaises(TypeError) as context:
            ZTLT()
        self.assertEqual(str(context.exception), "ZTLT() missing 1 required positional argument: 'params'")

    def test_less_than_operation_should_work(self):
        """
        Test that the 'Less Than' operation (ZTLT) works correctly when valid parameters are provided.

        This test checks the following valid conditions:

        1. The operation should work with a list of two parameters, where both parameters can be a field or a number.
        2. The operation should correctly handle comparisons between fields and constants (numbers).
        3. The operation should handle comparisons between two numeric constants.

        The following scenarios are tested:
        - A list of two fields (e.g., "price" and "quantity") is passed.
        - A field and a numeric constant (e.g., "price" and 10) are compared.
        - Two numeric constants (e.g., 100 and 200) are compared to test the operation.
        """
        # Test case 1: Less than operation with two fields as operands
        result = ZTLT(["price", "quantity"]).get_fields()
        expected_result = {"operator": "<", "operand": ["price", "quantity"]}
        self.assertEqual(result, expected_result, "less than operation should work")

        # Test case 2: Less than operation with a field and a constant value
        result = ZTLT(["price", 10]).get_fields()
        expected_result = {"operator": "<", "operand": ["price", 10]}
        self.assertEqual(result, expected_result, "less than operation should work")

        # Test case 3: Less than operation with two constants as operands
        result = ZTLT([100, 200]).get_fields()
        expected_result = {"operator": "<", "operand": [100, 200]}
        self.assertEqual(result, expected_result, "less than operation should work")

    def test_greater_than_or_equal_operation_should_throw_error_when_params_are_invalid(self):
        """
        Test that the 'Greater Than or Equal' operation (ZTGTE) throws the appropriate errors when invalid parameters are provided.

        This test checks the following error conditions:

        1. Invalid parameter type: The `params` must be a list, not a string or dictionary.
        2. Missing required positional argument: The `params` argument is mandatory.
        3. Invalid numeric parameter: A numeric value should be part of a list, not passed alone.

        The following scenarios are tested:
        - Invalid parameter type: string passed instead of a list.
        - Invalid parameter type: dictionary passed instead of a list.
        - Invalid parameter type: numeric value passed instead of a list.
        - Missing required positional argument: no parameters provided.
        """
        with self.assertRaises(ValueError) as context:
            ZTGTE("invalid")
        self.assertEqual(str(context.exception), "The 'Greater than or equal' filter params must be list")

        with self.assertRaises(ValueError) as context:
            ZTGTE({"x": 1})
        self.assertEqual(str(context.exception), "The 'Greater than or equal' filter params must be list")

        with self.assertRaises(ValueError) as context:
            ZTGTE(123)
        self.assertEqual(str(context.exception), "The 'Greater than or equal' filter params must be list")

        with self.assertRaises(TypeError) as context:
            ZTGTE()
        self.assertEqual(str(context.exception), "ZTGTE() missing 1 required positional argument: 'params'")

    def test_less_than_or_equal_operation_should_work(self):
        """
        Test that the 'Less Than or Equal' operation (ZTLTE) works correctly when valid arguments are provided.

        This test checks that the operation correctly processes the given valid input, forming the expected result with the correct operator and operands.

        The following scenarios are tested:
        - The operation works with two field names.
        - The operation works with a field name and a numeric value.
        - The operation works with two numeric values.
        """

        # Test case 1: Less than or equal operation with two fields as operands
        result = ZTLTE(["price", "quantity"]).get_fields()
        expected_result = {"operator": "<=", "operand": ["price", "quantity"]}
        self.assertEqual(result, expected_result, "less than or equal operation should work")

        # Test case 2: Less than or equal operation with a field and a constant value
        result = ZTLTE(["price", 10]).get_fields()
        expected_result = {"operator": "<=", "operand": ["price", 10]}
        self.assertEqual(result, expected_result, "less than or equal operation should work")

        # Test case 3: Less than or equal operation with two constants as operands
        result = ZTLTE([200, 100]).get_fields()
        expected_result = {"operator": "<=", "operand": [200, 100]}
        self.assertEqual(result, expected_result, "less than or equal operation should work")

    def test_in_operation_should_throw_error_when_field_is_not_string(self):
        """
        Test that the 'IN' operation (ZTIN) throws appropriate errors when invalid `field` or `values` arguments are provided.

        This test checks the following error conditions:

        1. Missing required positional argument: `values`.
        2. Unexpected keyword argument: The `field` and `values` should be properly passed as arguments.
        3. Invalid `field`: The `field` argument must be a string (not a number or incorrect type).
        4. Invalid `values`: The `values` argument must be a list (not a dictionary, number, or any other type).

        The following scenarios are tested:
        - Missing `values` argument for ZTIN.
        - Unexpected keyword argument for ZTIN.
        - Invalid `field` (not a string).
        - Invalid `values` (not a list).
        """

        # Test case 1: Invalid argument: dictionary instead of a string
        with self.assertRaises(TypeError) as context:
            ZTIN({"x": 1})
        self.assertEqual(str(context.exception), "ZTIN() missing 1 required positional argument: 'values'")

        # Test case 2: Invalid argument: integer instead of a string
        with self.assertRaises(TypeError) as context:
            ZTIN(123)
        self.assertEqual(str(context.exception), "ZTIN() missing 1 required positional argument: 'values'")

        # Test case 3: Invalid argument: only one parameter, string for the key
        with self.assertRaises(TypeError) as context:
            ZTIN("price")
        self.assertEqual(str(context.exception), "ZTIN() missing 1 required positional argument: 'values'")

        # Test case 4: Invalid argument: missing both key and values
        with self.assertRaises(TypeError) as context:
            ZTIN()
        self.assertEqual(str(context.exception), "ZTIN() missing 2 required positional arguments: 'key' and 'values'")

        # Test case 5: Invalid values: dictionary instead of a list
        with self.assertRaises(ValueError) as context:
            ZTIN("price", {"x": 1})
        self.assertEqual(str(context.exception), "'IN' filter values must be list")

        # Test case 6: Invalid values: integer instead of a list
        with self.assertRaises(ValueError) as context:
            ZTIN("price", 123)
        self.assertEqual(str(context.exception), "'IN' filter values must be list")

    def test_in_operation_should_work(self):
        """
        Test that the 'IN' operation (ZTIN) works correctly when valid `field` and `values` are provided.

        This test checks the following scenarios:

        1. Correct usage of ZTIN with a valid `field` and a list of `values`.
        2. Proper handling of the `operator` set to "IN" and the operand being the field.
        3. The result is returned in the expected format with the `operator`, `operand`, and `result`.

        The following scenarios are tested:
        - Providing a valid field ("price") and a list of values ([10, 20, 33, 50]).
        - The result should be a dictionary containing the operator "IN", operand "price", and result as the list of values.
        """
        # Test valid input
        result = ZTIN("price", [10, 20, 33, 50]).get_fields()
        expected_result = {"operator": "IN", "operand": "price", "result": [10, 20, 33, 50]}

        # Assert that the result matches the expected output
        self.assertEqual(result, expected_result, "IN operation should work")

    def test_equal_operation_should_throw_error_when_field_is_not_string(self):
        """
        Test that the 'EQUAL' operation (ZTEQUAL) throws appropriate errors when invalid arguments are provided for the `param` and `result`.

        This test checks the following error conditions for the 'EQUAL' operation:

        1. Missing required positional arguments: `param` and `result`.
        2. Invalid argument types for `param` and `result`:
           - `param` must be a valid field name (a string).
           - `result` must be a valid value (a string, number, or other expected types).

        The following scenarios are tested:
        - Missing `param` and `result` arguments.
        - Missing the `result` argument.
        - Invalid `param` argument types (e.g., list, dictionary, or non-string values).
        - Invalid `result` argument types (e.g., lists, non-valid types).

        Expected errors:
        - If `param` is missing or invalid, a `ValueError` is raised.
        - If `result` is missing or invalid, a `ValueError` is raised.
        """
        with self.assertRaises(TypeError) as context:
            ZTEQUAL()
        self.assertEqual(str(context.exception),
                         "ZTEQUAL() missing 2 required positional arguments: 'param' and 'result'")

        with self.assertRaises(TypeError) as context:
            ZTEQUAL("x")
        self.assertEqual(str(context.exception), "ZTEQUAL() missing 1 required positional argument: 'result'")

        with self.assertRaises(ValueError) as context:
            ZTEQUAL([], [])
        self.assertEqual(str(context.exception), "Invalid 'param' argument")

        with self.assertRaises(ValueError) as context:
            ZTEQUAL([123], [])
        self.assertEqual(str(context.exception), "Invalid 'param' argument")

        with self.assertRaises(ValueError) as context:
            ZTEQUAL(["xyz"], [])
        self.assertEqual(str(context.exception), "Invalid 'param' argument")

        with self.assertRaises(ValueError) as context:
            ZTEQUAL({}, [])
        self.assertEqual(str(context.exception), "Invalid 'param' argument")

        with self.assertRaises(ValueError) as context:
            ZTEQUAL({"prince": 100}, [])
        self.assertEqual(str(context.exception), "Invalid 'param' argument")

        with self.assertRaises(ValueError) as context:
            ZTEQUAL("price", [])
        self.assertEqual(str(context.exception), "Invalid 'result' argument")

        with self.assertRaises(ValueError) as context:
            ZTEQUAL("discount", [123])
        self.assertEqual(str(context.exception), "Invalid 'result' argument")

        with self.assertRaises(ValueError) as context:
            ZTEQUAL("quantity", {})
        self.assertEqual(str(context.exception), "Invalid 'result' argument")

    def test_equal_operation_should_work(self):
        """
        Test that the 'EQUAL' operation (ZTEQUAL) works correctly when valid arguments are provided.

        This test checks that the `ZTEQUAL` operation correctly processes the following scenarios:

        1. Simple equality operation with a field and a number.
        2. Equality operation with a nested multiplication operation.
        3. Equality operation with a division operation.
        4. Equality operation with an addition operation.
        5. Equality operation with a subtraction operation.

        The following scenarios are tested:
        - ZTEQUAL("price", 100) should create an equality check between "price" and 100.
        - ZTEQUAL(ZTMUL(["price", "quantity"]), 100) should check the equality of the result of the multiplication of "price" and "quantity" with 100.
        - ZTEQUAL(ZTDIV("price", "quantity"), 200) should check the equality of the result of dividing "price" by "quantity" with 200.
        - ZTEQUAL(ZTADD(["price", "quantity"]), 20) should check the equality of the result of adding "price" and "quantity" with 20.
        - ZTEQUAL(ZTSUB(["price", "quantity"]), 0) should check the equality of the result of subtracting "quantity" from "price" with 0.

        Expected results:
        - The operator should be set to "=".
        - The operand should correctly reflect the field or operation being evaluated.
        - The result should match the expected value.
        """
        result = ZTEQUAL("price", 100).get_fields()
        expected = {"operator": "=", "operand": "price", "result": 100}
        self.assertEqual(result, expected, "equal operation should work")

        result = ZTEQUAL(ZTMUL(["price", "quantity"]), 100).get_fields()
        expected = {
            "operator": "=",
            "operand": {"operator": "*", "operand": ["price", "quantity"]},
            "result": 100
        }
        self.assertEqual(result, expected, "equal operation should work")

        result = ZTEQUAL(ZTDIV("price", "quantity"), 200).get_fields()
        expected = {
            "operator": "=",
            "operand": {"operator": "/", "operand": ["price", "quantity"]},
            "result": 200
        }
        self.assertEqual(result, expected, "equal operation should work")

        result = ZTEQUAL(ZTADD(["price", "quantity"]), 20).get_fields()
        expected = {
            "operator": "=",
            "operand": {"operator": "+", "operand": ["price", "quantity"]},
            "result": 20
        }
        self.assertEqual(result, expected, "equal operation should work")

        result = ZTEQUAL(ZTSUB(["price", "quantity"]), 0).get_fields()
        expected = {
            "operator": "=",
            "operand": {"operator": "-", "operand": ["price", "quantity"]},
            "result": 0
        }
        self.assertEqual(result, expected, "equal operation should work")

    def test_or_operation_should_work(self):
        """
        Test that the 'OR' operation (ZTOR) works correctly when multiple conditions are provided.

        This test checks that the `ZTOR` operation correctly processes the following scenarios:

        1. Combining multiple conditions using the OR operator (`||`).
        2. The OR operation should correctly combine the equality and greater-than conditions.
        3. The `ZTOR` operation should return the correct structure with the operator `||`, and the operand should contain the list of individual conditions.

        The following scenarios are tested:
        - Combining two conditions: `ZTEQUAL("price", 100)` and `ZTGT(["price", 200])` using the OR operator.

        Expected result:
        - The operator should be set to `||`.
        - The operand should be a list of the two conditions: an equality check between `"price"` and `100`, and a greater-than check between `"price"` and `200`.
        """
        # Create the OR condition combining two individual conditions: ZTEQUAL and ZTGT
        or_condition = ZTOR([
            ZTEQUAL("price", 100),  # First condition: price equals 100
            ZTGT(["price", 200]),  # Second condition: price greater than 200
        ])

        # Expected result structure for the OR operation
        expected_result = {
            "operator": "||",  # The OR operation should use the '||' operator
            "operand": [  # The operand should contain the two conditions as a list
                {"operator": "=", "operand": "price", "result": 100},  # First condition: price = 100
                {"operator": ">", "operand": ["price", 200]}  # Second condition: price > 200
            ]
        }

        # Assert that the actual result from ZTOR matches the expected result
        self.assertEqual(or_condition.get_fields(), expected_result)

    def test_and_operation_should_work(self):
        """
        Test that the 'AND' operation (ZTAND) works correctly when multiple conditions are provided.

        This test checks that the `ZTAND` operation correctly processes the following scenarios:

        1. Combining multiple conditions using the AND operator (`&&`).
        2. The AND operation should correctly combine the equality and greater-than conditions.
        3. The `ZTAND` operation should return the correct structure with the operator `&&`, and the operand should contain the list of individual conditions.

        The following scenarios are tested:
        - Combining two conditions: `ZTEQUAL("price", 100)` and `ZTGT(["quantity", 200])` using the AND operator.

        Expected result:
        - The operator should be set to `&&`.
        - The operand should be a list of the two conditions: an equality check between `"price"` and `100`, and a greater-than check between `"quantity"` and `200`.
        """
        # Create the AND condition combining two individual conditions: ZTEQUAL and ZTGT
        and_condition = ZTAND([
            ZTEQUAL("price", 100),  # First condition: price equals 100
            ZTGT(["quantity", 200]),  # Second condition: quantity greater than 200
        ])

        # Expected result structure for the AND operation
        expected_result = {
            "operator": "&&",  # The AND operation should use the '&&' operator
            "operand": [  # The operand should contain the two conditions as a list
                {"operator": "=", "operand": "price", "result": 100},  # First condition: price = 100
                {"operator": ">", "operand": ["quantity", 200]}  # Second condition: quantity > 200
            ]
        }

        # Assert that the actual result from ZTAND matches the expected result
        self.assertEqual(and_condition.get_fields(), expected_result, "AND operation should work")

    def test_multiple_combination_with_or_operation_should_work(self):
        """
        Test that multiple conditions combined with the 'OR' operator (||) work as expected.

        This test checks that the `ZTOR` operation correctly processes multiple AND conditions combined with the OR operator (`||`).

        1. The OR operator should combine multiple conditions, and each condition can be an AND operation.
        2. The AND operation itself can contain multiple conditions, such as equality and comparison operations.
        3. The test verifies the correct handling of nested AND conditions inside the OR operation.

        The following scenarios are tested:
        - First AND condition: `price` equals 100 and `quantity` is greater than 200.
        - Second AND condition: `price` equals 100 and `price` multiplied by 200 equals 300.

        Expected result:
        - The operator should be set to `||` (OR).
        - The operand should contain a list of two AND conditions, each with its respective individual conditions.
        """
        # Create the OR condition combining two AND conditions
        conditions = ZTOR([
            # First AND condition: price equals 100 and quantity greater than 200
            ZTAND([
                ZTEQUAL("price", 100),  # First condition: price = 100
                ZTGT(["quantity", 200]),  # Second condition: quantity > 200
            ]),

            # Second AND condition: price equals 100 and price multiplied by 200 equals 300
            ZTAND([
                ZTEQUAL("price", 100),  # First condition: price = 100
                ZTEQUAL(ZTMUL(["price", 200]), 300),  # Second condition: price * 200 = 300
            ])
        ])

        # Expected result structure for the OR operation containing two AND conditions
        expected_result = {
            "operator": "||",  # The operator should be '||' (OR)
            "operand": [  # The operand should contain the two AND conditions as a list
                {
                    "operator": "&&",  # The first condition uses the '&&' (AND) operator
                    "operand": [  # The operand contains the individual conditions:
                        {"operator": "=", "operand": "price", "result": 100},  # price = 100
                        {"operator": ">", "operand": ["quantity", 200]}  # quantity > 200
                    ]
                },
                {
                    "operator": "&&",  # The second condition uses the '&&' (AND) operator
                    "operand": [  # The operand contains the individual conditions:
                        {"operator": "=", "operand": "price", "result": 100},  # price = 100
                        {
                            "operator": "=",  # The second condition is an equality check
                            "operand": {
                                "operator": "*",  # price * 200
                                "operand": ["price", 200]
                            },
                            "result": 300  # The result should be 300
                        }
                    ]
                }
            ]
        }

        # Assert that the actual result from ZTOR matches the expected result
        self.assertEqual(conditions.get_fields(), expected_result)


if __name__ == '__main__':
    unittest.main()