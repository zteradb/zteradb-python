# -----------------------------------------------------------------------------
# File: zteradb_filter_condition_functions.py
# Description: This file provides utility functions to simplify the process of
#              creating filter conditions for ZTeraDB queries. It includes
#              functions for logical, arithmetic, and string-based filters.
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

from typing import Union, TypeVar
from .zteradb_filter_conditions import ZTeraDBFilterCondition

T = TypeVar('T', bound=int)

def ZTAND(filters: list[ZTeraDBFilterCondition]) -> ZTeraDBFilterCondition:
    """
    Creates a filter condition using the 'AND' logical operator.

    params:
        filters (list): A list of filter conditions.

    returns:
        ZTeraDBFilterCondition: The condition with 'AND' operator.
    """
    return ZTeraDBFilterCondition().set_and_filter(filters=filters)

def ZTOR(filters: list[ZTeraDBFilterCondition]) -> ZTeraDBFilterCondition:
    """
    Creates a filter condition using the 'OR' logical operator.

    params:
        filters (list): A list of filter conditions.

    returns:
        ZTeraDBFilterCondition: The condition with 'OR' operator.
    """
    return ZTeraDBFilterCondition().set_or_filter(filters=filters)

def ZTEQUAL(param: Union[str, int, float, ZTeraDBFilterCondition], result) -> ZTeraDBFilterCondition:
    """
    Creates an 'EQUAL' filter condition.

    params:
        param (Union[str, int, float, ZTeraDBFilterCondition]): The field to compare.
        result (str): The value to compare with.

    returns:
        ZTeraDBFilterCondition: The condition with 'EQUAL' operator.
    """
    return  ZTeraDBFilterCondition().set_equal_filter(param, result)

def ZTIN(key: str, values: list) -> ZTeraDBFilterCondition:
    """
    Creates an 'IN' filter condition.

    params:
        key (str): The field to check.
        values (list): The list of values to check against.

    returns:
        ZTeraDBFilterCondition: The condition with 'IN' operator.
    """
    return ZTeraDBFilterCondition().set_in_filter(field=key, values=values)

def ZTADD(values: list) -> ZTeraDBFilterCondition:
    """
    Creates an 'ADD' filter condition.

    params:
        values (list): A list of values to add in the condition.

    returns:
        ZTeraDBFilterCondition: The condition with 'ADD' operator.
    """
    return  ZTeraDBFilterCondition().set_add(values)

def ZTSUB(values: list) -> ZTeraDBFilterCondition:
    """
    Creates a 'SUB' filter condition.

    params:
        values (list): A list of values to subtract in the condition.

    returns:
        ZTeraDBFilterCondition: The condition with 'SUB' operator.
    """
    return  ZTeraDBFilterCondition().set_sub(values)

def ZTMUL(values: list) -> ZTeraDBFilterCondition:
    """
    Creates a 'MUL' filter condition.

    params:
        values (list): A list of values to multiply in the condition.

    returns:
        ZTeraDBFilterCondition: The condition with 'MUL' operator.
    """
    return  ZTeraDBFilterCondition().set_mul(values)

def ZTDIV(dividend: Union[T, str, int, float, ZTeraDBFilterCondition], divisor: Union[T, str, int, float, ZTeraDBFilterCondition]) -> ZTeraDBFilterCondition:
    """
    Creates a 'DIV' filter condition.

    params:
        dividend (Union[T, str, int, float, ZTeraDBFilterCondition]): The value to divide.
        divisor (Union[T, str, int, float, ZTeraDBFilterCondition]): The value by which to divide.

    returns:
        ZTeraDBFilterCondition: The condition with 'DIV' operator.
    """
    return  ZTeraDBFilterCondition().set_div(dividend, divisor)

def ZTMOD(numerator: Union[T, str, int, float, ZTeraDBFilterCondition], denominator: Union[T, str, int, float, ZTeraDBFilterCondition]) -> ZTeraDBFilterCondition:
    """
    Creates a 'MOD' filter condition.

    params:
        numerator (Union[T, str, int, float, ZTeraDBFilterCondition]): The numerator value (or a field).
        denominator (Union[T, str, int, float, ZTeraDBFilterCondition]): The denominator value (or a field).

    returns:
        ZTeraDBFilterCondition: The condition with 'MOD' operator.
    """
    return  ZTeraDBFilterCondition().set_mod_filter(numerator, denominator)

def ZTGT(params: list) -> ZTeraDBFilterCondition:
    """
    Creates a 'GREATER THAN' filter condition.

    params:
        params (list): The list of parameters for the condition.

    returns:
        ZTeraDBFilterCondition: The condition with 'GREATER THAN' operator.
    """
    return ZTeraDBFilterCondition().set_greater_than_filter(params=params)

def ZTGTE(params: list) -> ZTeraDBFilterCondition:
    """
    Creates a 'GREATER THAN OR EQUAL TO' filter condition.

    params:
        params (list): The list of parameters for the condition.

    returns:
        ZTeraDBFilterCondition: The condition with 'GREATER THAN OR EQUAL TO' operator.
    """
    return ZTeraDBFilterCondition().set_greater_than_or_equal_filter(params=params)

def ZTLT(params: list) -> ZTeraDBFilterCondition:
    """
    Creates a 'LESS THAN' filter condition.

    params:
        params (list): The list of parameters for the condition.

    returns:
        ZTeraDBFilterCondition: The condition with 'LESS THAN' operator.
    """
    return ZTeraDBFilterCondition().set_less_than_filter(params=params)

def ZTLTE(params: list) -> ZTeraDBFilterCondition:
    """
    Creates a 'LESS THAN OR EQUAL TO' filter condition.

    params:
        params (list): The list of parameters for the condition.

    returns:
        ZTeraDBFilterCondition: The condition with 'LESS THAN OR EQUAL TO' operator.
    """
    return ZTeraDBFilterCondition().set_less_than_or_equal_filter(params=params)

def ZTCONTAINS(field: str, value: str) -> ZTeraDBFilterCondition:
    """
    Creates a 'CONTAINS' filter condition for string matching.

    params:
        field (str): The field to check for 'contains'.
        value (str): The string to check for containment.

    returns:
        ZTeraDBFilterCondition: The condition with 'CONTAINS' operator.
    """
    return ZTeraDBFilterCondition().set_contains_filter(field=field, value=value)

def ZTICONTAINS(field: str, value: str) -> ZTeraDBFilterCondition:
    """
    Creates a case-insensitive 'CONTAINS' filter condition for string matching.

    params:
        field (str): The field to check for 'icontains'.
        value (str): The string to check for containment.

    returns:
        ZTeraDBFilterCondition: The condition with 'ICONTAINS' operator.
    """
    return ZTeraDBFilterCondition().set_icontains_filter(field=field, value=value)

def ZTSTARTSWITH(field: str, value: str) -> ZTeraDBFilterCondition:
    """
    Creates a 'STARTSWITH' filter condition for string matching.

    params:
        field (str): The field to check for 'startswith'.
        value (str): The string that the field should start with.

    returns:
        ZTeraDBFilterCondition: The condition with 'STARTSWITH' operator.
    """
    return ZTeraDBFilterCondition().set_starts_with_filter(field=field, value=value)

def ZTISTARTSWITH(field: str, value: str) -> ZTeraDBFilterCondition:
    """
    Creates a case-insensitive 'STARTSWITH' filter condition for string matching.

    params:
        field (str): The field to check for 'istartswith'.
        value (str): The string that the field should start with.

    returns:
        ZTeraDBFilterCondition: The condition with 'ISTARTSWITH' operator.
    """
    return ZTeraDBFilterCondition().set_istarts_with_filter(field=field, value=value)

def ZTENDSWITH(field: str, value: str) -> ZTeraDBFilterCondition:
    """
    Creates an 'ENDSWITH' filter condition for string matching.

    params:
        field (str): The field to check for 'endswith'.
        value (str): The string that the field should end with.

    returns:
        ZTeraDBFilterCondition: The condition with 'ENDSWITH' operator.
    """
    return ZTeraDBFilterCondition().set_ends_with_filter(field=field, value=value)

def ZTIENDSWITH(field: str, value: str) -> ZTeraDBFilterCondition:
    """
    Creates a case-insensitive 'ENDSWITH' filter condition for string matching.

    params:
        field (str): The field to check for 'iendswith'.
        value (str): The string that the field should end with.

    returns:
        ZTeraDBFilterCondition: The condition with 'IENDSWITH' operator.
    """
    return ZTeraDBFilterCondition().set_iends_with_filter(field=field, value=value)
