# -----------------------------------------------------------------------------
# File: zteradb_filter_conditions.py
# Description: This file defines the classes that encapsulate the logic for constructing
#              and managing filter conditions in ZTeraDB queries. It contains base
#              functionality for arithmetic, logical, and string-based filters.
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

from .zteradb_filter_types import ZTeraDBFilterTypes


class ZTeraDBCommonCondition:
    """
    Base class to handle common filtering operations for ZTeraDB.

    Contains basic arithmetic operations (add, subtract, multiply, divide)
    that modify the filter condition and store them in the 'filters' list.
    """

    def __init__(self):
        self.filters = []

    def is_valid_value(self, value):
        """
        Returns True if the value is not an instance of dict, list, tuple, set, function
        """
        return not isinstance(value, (dict, list, tuple, set, type(lambda x: x)))

    def get_fields(self):
        """
        Placeholder method to be implemented by a subclass.

        Raises:
            Exception: This method should be implemented by a subclass.
        """
        raise Exception("The method 'getFields' must be implemented by a subclass.")

    def set_add(self, values):
        """
        Set an 'addition' operation in the filter condition.

        params:
            values (list): A list of values to be added in the filter.

        returns:
            self: The current instance of ZTeraDBCommonCondition.
        """
        if not isinstance(values, list):
            raise ValueError(f"'{values}' must be list for add operation")

        for value in values:
            if not self.is_valid_value(value):
                raise ValueError(f"Invalid '{value}' for add operation")

        operand = [value if isinstance(value, type(self)) else value for value in values]
        self.filters.append(dict(operator=ZTeraDBFilterTypes.ADD.value, operand=operand))
        return self

    def set_sub(self, values):
        """
        Set a 'subtraction' operation in the filter condition.

        params:
            values (list): A list of values to be subtracted in the filter.

        returns:
            self: The current instance of ZTeraDBCommonCondition.
        """
        if not isinstance(values, list):
            raise ValueError(f"'{values}' must be list for sub operation")

        for value in values:
            if not self.is_valid_value(value):
                raise ValueError(f"Invalid '{value}' for sub operation")

        operand = [value if isinstance(value, type(self)) else value for value in values]
        self.filters.append(dict(operator=ZTeraDBFilterTypes.SUB.value, operand=operand))
        return self

    def set_mul(self, values):
        """
        Set a 'multiplication' operation in the filter condition.

        params:
            values (list): A list of values to be multiplied in the filter.

        returns:
            self: The current instance of ZTeraDBCommonCondition.
        """
        if not isinstance(values, list):
            raise ValueError(f"'{values}' must be list for mul operation")

        for value in values:
            if not self.is_valid_value(value):
                raise ValueError(f"Invalid '{value}' for mul operation")

        operand = [value if isinstance(value, type(self)) else value for value in values]
        self.filters.append(dict(operator=ZTeraDBFilterTypes.MUL.value, operand=operand))
        return self

    def set_div(self, dividend, divisor):
        """
        Set a 'division' operation in the filter condition.

        params:
            dividend (Union[T, str, int, float, ZTeraDBFilterCondition]): The value to be divided.
            divisor (Union[T, str, int, float, ZTeraDBFilterCondition]): The value by which to divide.

        returns:
            self: The current instance of ZTeraDBCommonCondition.
        """
        if not self.is_valid_value(dividend):
            raise ValueError("'dividend' must be numeric or schema field.")

        if not self.is_valid_value(divisor):
            raise ValueError("'divisor' must be numeric or schema field.")

        if not divisor:
            raise ValueError("'divisor' must be numeric or schema field and it should be greater than 0.")

        dividend = dividend.get_fields() if isinstance(dividend, ZTeraDBFilterCondition) else dividend
        divisor = divisor.get_fields() if isinstance(divisor, ZTeraDBFilterCondition) else divisor
        self.filters.append(dict(operator=ZTeraDBFilterTypes.DIV.value, operand=[dividend, divisor]))
        return self


class ZTeraDBFilterCondition(ZTeraDBCommonCondition):
    """
    Subclass that extends ZTeraDBCommonCondition to handle more specific filter conditions.
    Provides methods for equality, modulo, logical operators, and string filters.
    """
    def __init__(self):
        super().__init__()

    def get_fields(self):
        """
        Retrieve the all filters used in the current filter condition.

        returns:
            The filter conditions (list of dicts).
        """
        return self.filters[0] if len(self.filters) == 1 else self.filters

    def set_equal_filter(self, param, result):
        """
        Set an 'equal' operation in the filter condition.

        params:
            param (str): The field to compare.
            result (str): The value to compare with.

        returns:
            self: The current instance of ZTeraDBFilterCondition.
        """
        if not self.is_valid_value(param):
            raise ValueError("Invalid 'param' argument")

        if not self.is_valid_value(result):
            raise ValueError("Invalid 'result' argument")

        param = param.get_fields() if isinstance(param, ZTeraDBFilterCondition) else param
        result = result.get_fields() if isinstance(result, ZTeraDBFilterCondition) else result
        self.filters.append(dict(operator=ZTeraDBFilterTypes.EQUAL.value, operand=param, result=result))
        return self

    def set_mod_filter(self, numerator, denominator):
        """
        Set a 'modulo' operation in the filter condition.

        params:
            numerator (Union[T, str, int, float, ZTeraDBFilterCondition]): The numerator value (or a field).
            denominator (Union[T, str, int, float, ZTeraDBFilterCondition]): The denominator value (or a field).

        returns:
            self: The current instance of ZTeraDBFilterCondition.
        """
        if not self.is_valid_value(numerator):
            raise ValueError("'numerator' must be numeric or schema field.")

        if not self.is_valid_value(denominator):
            raise ValueError("'denominator' must be numeric or schema field and must be greater than 0")

        if not denominator:
            raise ValueError("'divisor' must be numeric or schema field and it should be greater than 0.")

        numerator = numerator.get_fields() if isinstance(numerator, ZTeraDBFilterCondition) else numerator
        denominator = denominator.get_fields() if isinstance(denominator, ZTeraDBFilterCondition) else denominator
        self.filters.append(dict(operator=ZTeraDBFilterTypes.MOD.value, operand=[numerator, denominator]))
        return self

    def set_in_filter(self, field, values):
        """
        Set an 'IN' operation in the filter condition.

        params:
            field (str): The field to check.
            values (list): The list of values to check against.

        returns:
            self: The current instance of ZTeraDBFilterCondition.
        """
        if not isinstance(field, str) or not field.strip():
            raise ValueError("'IN' filter field must be schema field name")

        if not isinstance(values, list):
            raise ValueError("'IN' filter values must be list")

        operand = [value.get_fields() if isinstance(value, type(self)) else value for value in values]
        self.filters.append(dict(operator=ZTeraDBFilterTypes.IN.value, operand=field, result=operand))
        return self

    def set_or_filter(self, filters):
        """
        Sets the 'OR' logical operator for a filter condition.

        params:
            filters (list): A list of filter conditions to apply the 'OR' logic.

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'OR' applied.
        """
        if not isinstance(filters, list):
            raise ValueError("The 'OR' filter must be list")

        operand = [filter.get_fields() if isinstance(filter, type(self)) else filter for filter in filters]
        self.filters.append(dict(operator=ZTeraDBFilterTypes.OR.value, operand=operand))
        return self

    def set_and_filter(self, filters):
        """
        Sets the 'AND' logical operator for a filter condition.

        params:
            filters (list): A list of filter conditions to apply the 'AND' logic.

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'AND' applied.
        """
        if not isinstance(filters, list):
            raise ValueError("The 'AND' filter must be list")

        operand = [filter.get_fields() if isinstance(filter, type(self)) else filter for filter in filters]
        self.filters.append(dict(operator=ZTeraDBFilterTypes.AND.value, operand=operand))
        return self

    def set_contains_filter(self, field, value):
        """
        Sets a 'CONTAINS' string operation for the filter condition.

        params:
            field (str): The field to check for the 'contains' condition.
            value (str): The string value to check if the field contains.

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'CONTAINS' applied.
        """
        if not isinstance(field, str) or not field.strip():
            raise ValueError("The `field` argument must be field name in contains filter.")

        if not isinstance(value, str) or not value.strip():
            raise ValueError("The `value` argument must be string in contains filter.")

        self.filters.append(dict(operator=ZTeraDBFilterTypes.CONTAINS.value, operand=field, result=value))
        return self

    def set_icontains_filter(self, field, value):
        """
        Sets a case-insensitive 'CONTAINS' string operation for the filter condition.

        params:
            field (str): The field to check for the 'icontains' condition.
            value (str): The string value to check if the field contains (case-insensitive).

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'ICONTAINS' applied.
        """
        if not isinstance(field, str) or not field.strip():
            raise ValueError("The `field` argument must be field name in icontains filter.")

        if not isinstance(value, str) or not value.strip():
            raise ValueError("The `value` argument must be string in icontains filter.")

        self.filters.append(dict(operator=ZTeraDBFilterTypes.ICONTAINS.value, operand=field, result=value))
        return self

    def set_starts_with_filter(self, field, value):
        """
        Sets a 'STARTSWITH' string operation for the filter condition.

        params:
            field (str): The field to check for the 'startswith' condition.
            value (str): The string value to check if the field starts with.

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'STARTSWITH' applied.
        """
        if not isinstance(field, str) or not field.strip():
            raise ValueError("The `field` argument must be field name in starts with filter.")

        if not isinstance(value, str) or not value.strip():
            raise ValueError("The `value` argument must be string in starts with filter.")

        self.filters.append(dict(operator=ZTeraDBFilterTypes.STARTSWITH.value, operand=field, result=value))
        return self

    def set_istarts_with_filter(self, field, value):
        """
        Sets a case-insensitive 'STARTSWITH' string operation for the filter condition.

        params:
            field (str): The field to check for the 'istartswith' condition.
            value (str): The string value to check if the field starts with (case-insensitive).

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'ISTARTSWITH' applied.
        """
        if not isinstance(field, str) or not field.strip():
            raise ValueError("The `field` argument must be field name in istarts with filter.")

        if not isinstance(value, str) or not value.strip():
            raise ValueError("The `value` argument must be string in istarts with filter.")

        self.filters.append(dict(operator=ZTeraDBFilterTypes.ISTARTSWITH.value, operand=field, result=value))
        return self

    def set_ends_with_filter(self, field, value):
        """
        Sets an 'ENDSWITH' string operation for the filter condition.

        params:
            field (str): The field to check for the 'endswith' condition.
            value (str): The string value to check if the field ends with.

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'ENDSWITH' applied.
        """
        if not isinstance(field, str) or not field.strip():
            raise ValueError("The `field` argument must be field name in ends with filter.")

        if not isinstance(value, str) or not value.strip():
            raise ValueError("The `value` argument must be string in ends with filter.")

        self.filters.append(dict(operator=ZTeraDBFilterTypes.ENDSWITH.value, operand=field, result=value))
        return self

    def set_iends_with_filter(self, field, value):
        """
        Sets a case-insensitive 'ENDSWITH' string operation for the filter condition.

        params:
            field (str): The field to check for the 'iendswith' condition.
            value (str): The string value to check if the field ends with (case-insensitive).

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'IENDSWITH' applied.
        """
        if not isinstance(field, str) or not field.strip():
            raise ValueError("The `field` argument must be field name in iends with filter.")

        if not isinstance(value, str) or not value.strip():
            raise ValueError("The `value` argument must be string in iends with filter.")

        self.filters.append(dict(operator=ZTeraDBFilterTypes.IENDSWITH.value, operand=field, result=value))
        return self

    def set_greater_than_filter(self, params):
        """
        Sets a 'GREATER THAN' filter condition.

        params:
            params (list): A list of parameters to compare.

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'GREATER THAN' applied.
        """
        if not isinstance(params, list):
            raise ValueError("The 'Greater than' filter params must be list")

        if len(params) < 2:
            raise ValueError("The 'Greater than' filter params must contains at-least two element in the list")

        operand = [param.get_fields() if isinstance(param, type(self)) else param for param in params]
        self.filters.append(dict(operator=ZTeraDBFilterTypes.GT.value, operand=operand))
        return self

    def set_greater_than_or_equal_filter(self, params):
        """
        Sets a 'GREATER THAN OR EQUAL TO' filter condition.

        params:
            params (list): A list of parameters to compare.

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'GREATER THAN OR EQUAL TO' applied.
        """
        if not isinstance(params, list):
            raise ValueError("The 'Greater than or equal' filter params must be list")

        if len(params) < 2:
            raise ValueError("The 'Greater than or equal' filter params must contains at-least two element in the list")

        operand = [param.get_fields() if isinstance(param, type(self)) else param for param in params]
        self.filters.append(dict(operator=ZTeraDBFilterTypes.GTE.value, operand=operand))
        return self

    def set_less_than_filter(self, params):
        """
        Sets a 'LESS THAN' filter condition.

        params:
            params (list): A list of parameters to compare.

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'LESS THAN' applied.
        """
        if not isinstance(params, list):
            raise ValueError("The 'Less than' filter params must be list")

        if len(params) < 2:
            raise ValueError("The 'Less than' filter params must contains at-least two element in the list")

        operand = [param.get_fields() if isinstance(param, type(self)) else param for param in params]
        self.filters.append(dict(operator=ZTeraDBFilterTypes.LT.value, operand=operand))
        return self

    def set_less_than_or_equal_filter(self, params):
        """
        Sets a 'LESS THAN OR EQUAL TO' filter condition.

        params:
            params (list): A list of parameters to compare.

        returns:
            self: The current instance of ZTeraDBFilterCondition with 'LESS THAN OR EQUAL TO' applied.
        """
        if not isinstance(params, list):
            raise ValueError("The 'Less than or equal' filter params must be list")

        if len(params) < 2:
            raise ValueError("The 'Less than or equal' filter params must contains at-least two element in the list")

        operand = [param.get_fields() if isinstance(param, type(self)) else param for param in params]
        self.filters.append(dict(operator=ZTeraDBFilterTypes.LTE.value, operand=operand))
        return self
