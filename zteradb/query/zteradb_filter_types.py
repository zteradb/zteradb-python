# -----------------------------------------------------------------------------
# File: filter_types.py
# Description: This file contains an enumeration (Enum) for various filter types
#              used in constructing ZTeraDB queries for advanced filtering operations.
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


class ZTeraDBFilterTypes(enum.Enum):
    """
    Enum that defines various advanced filter types used for querying filter group filter data.
    These filters can be used to construct filter group queries for advanced field filtering.

    The Enum provides common ZTeraDB operations like AND, OR, EQUAL, etc., as well as
    string operations like CONTAINS, STARTSWITH, and ENDSWITH.
    """
    OR = "||"               # OR filter type for 'OR' operation in ZTeraDB queries
    AND = "&&"              # AND filter type for 'AND' operation in ZTeraDB queries
    EQUAL = "="             # EQUAL filter type for 'equal to' operation in ZTeraDB queries
    NOTEQUAL = "!="         # NOTEQUAL filter type for 'not equal to' operation in ZTeraDB queries
    ADD = "+"               # ADD filter type for 'addition' operation in ZTeraDB queries
    SUB = "-"               # SUB filter type for 'subtract' operation in ZTeraDB queries
    MUL = "*"               # MUL filter type for 'multiplication' operation in ZTeraDB queries
    DIV = "/"               # DIV filter type for 'divide' operation in ZTeraDB queries
    MOD = "%"               # MOD filter type for 'modulo' operation in ZTeraDB queries
    GT = ">"                # GT filter type for 'greater than' operation in ZTeraDB queries
    GTE = ">="              # GTE filter type for 'greater than or equal to' operation in ZTeraDB queries
    LT = "<"                # LT filter type for 'less than' operation in ZTeraDB queries
    LTE = "<="              # LTE filter type for 'less than or equal to' operation in ZTeraDB queries
    CONTAINS = "%%"         # LIKE filter type for string 'LIKE' operation in ZTeraDB queries
    ICONTAINS = "i%%"       # ILIKE filter type for string case-insensitive 'LIKE' operation in ZTeraDB queries
    STARTSWITH = "^%%"      # STARTSWITH filter type for string 'starts with' operation in ZTeraDB queries
    ISTARTSWITH = "^i%%"    # ISTARTSWITH filter type for string case-insensitive 'starts with' operation in ZTeraDB queries
    ENDSWITH = "%%$"        # ENDSWITH filter type for string 'ends with' operation in ZTeraDB queries
    IENDSWITH = "i%%$"      # IENDSWITH filter type for string case-insensitive 'ends with' operation in ZTeraDB queries
    IN = "IN"               # IN filter type for schema field 'in' operation in ZTeraDB queries
