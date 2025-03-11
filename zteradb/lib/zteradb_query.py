# -----------------------------------------------------------------------------
# File: zteradb_query.py
# Description: This file defines classes and functions used to build and manage
#              ZTeraDB queries. The main class, ZTeraDBQuery, allows users to
#              construct JSON based queries using various methods such as selecting,
#              inserting, updating, and deleting records. It supports advanced
#              features like filtering, sorting, limiting results, and handling
#              related fields and conditions.
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

from dataclasses import dataclass
from .zteradb_filter_conditions import ZTeraDBFilterCondition
from .zteradb_query_type import ZTeraDBQueryType
from ..zteradb_exception import ZTeraDBQueryError

# -----------------------------------------------------------------------------
# Class Definitions:
#
# 1. Query:
#    A dataclass representing the structure of a query, including details such
#    as schema, database, query type, filters, sort order, etc.
#
# 2. Limit:
#    Represents the limit (pagination) of query results with start and end values.
#
# 3. Sort:
#    Represents sorting order of query results. Supports ascending (ASC) and
#    descending (DESC) sort orders.
#
# 4. QueryFields:
#    A container for query field names.
#
# 5. ZTeraDBQuery:
#    A core class for building ZTeraDB queries, with methods for constructing
#    SELECT, INSERT, UPDATE, and DELETE queries with customizable filters,
#    limits, sort orders, and related field conditions.
#
# -----------------------------------------------------------------------------

@dataclass
class Query:
    """
    A dataclass that represents the structure of a query. It contains attributes
    for schema, database, query type, filters, sorting, related fields, etc.
    """

    sh: str         # Schema name
    db: str         # Database ID
    qt: int         # Query type (e.g., SELECT, INSERT, etc.)
    fl: dict        # Fields to include in the query result
    rf: dict        # Related fields in the query
    fi: dict        # Filters for the query
    fc: list        # Filter conditions
    st: dict        # Sorting options
    lt: tuple       # Limit for query results (start, end)
    cnt: bool       # Flag indicating whether to count results


class Limit:
    """
    Represents a limit on query results, including the start and end points for pagination.
    """

    __slots__ = ["_start", "_end"]

    def __init__(self, start, end):
        """
        Initialize the Limit with start and end values.

        :param start: The starting index for the query results.
        :param end: The ending index for the query results.
        """
        # Start of the result set
        self._start = start

        # End of the result set
        self._end = end

    @property
    def start(self):
        """Return the start point of the limit."""
        return self._start

    @property
    def end(self):
        """Return the end point of the limit."""
        return self._end

    @property
    def limit(self):
        """Return the limit as a tuple (start, end)."""
        return self.start, self.end


class Sort:
    """
    Represents sorting order for query results. Supports ascending and descending order.
    """

    __slots__ = ["_field", "_sort_order"]
    ASC = 1         # Ascending order
    DESC = -1       # Descending order

    def __init__(self, field, order):
        """
        Initialize the Sort with a field and order.

        :param field: The field to sort by.
        :param order: The order to sort (1 for ASC, -1 for DESC).
        """
        self._field = field
        self._sort_order = self.ASC if order == self.ASC else self.DESC

    @property
    def __dict__(self):
        """Return the field and sort order as a dictionary."""
        return {self.field: self._sort_order}

    @property
    def field(self):
        """Return the field to be sorted."""
        return self._field

    @property
    def sort_order(self):
        """Return the sort order (ASC or DESC)."""
        return self._sort_order

    def is_asc(self):
        """Return True if the sort order is ascending."""
        return self._sort_order == self.ASC

    def is_desc(self):
        """Return True if the sort order is descending."""
        return self._sort_order == self.DESC


class QueryFields:
    """
    A container for the field names used in the ZTeraDBQuery class.
    """
    fields = (
        "_schema_name",
        "_database_id",
        "_query_type",
        "_fields",
        "_filters",
        "_filter_conditions",
        "_limit",
        "_sort",
        "_related_fields",
        "_count",
        "_env",
    )


class ZTeraDBQuery:
    """
    The core class for constructing ZTeraDB queries. This class supports SELECT,
    INSERT, UPDATE, and DELETE queries and allows adding fields, filters,
    related fields, sorting, and limit options.

    Methods include:
      - select(), insert(), update(), delete(): Set the query type.
      - filter(): Add filters to the query.
      - filter_condition(): Add complex filter conditions.
      - sort(): Set sorting order.
      - limit(): Set result limits (pagination).
      - related_field(): Add related field queries.
      - generate(): Generates the final query in dictionary form.

    Example usage:
    --------------
    query = ZTeraDBQuery("schema_name", "db_1")
    query.select().limit(0, 10).filter(name="John", age=30).sort(name=Sort.ASC).related_field({"related_field": ZTeraDBQuery("related_schema").select()})
    print(json.dumps(query.generate(), indent=2))
    """

    __slots__ = QueryFields.fields

    def __init__(self, schema_name, database_id=None):
        """
        Initializes the ZTeraDBQuery instance with schema name and optional database ID.

        :param schema_name: The name of the schema (string).
        :param database_id: The database ID (optional).
        """
        if schema_name is None or not isinstance(schema_name, str) or schema_name.strip() == "":
            raise ValueError("Schema name is required")

        self._schema_name = schema_name

        if database_id:
            self._database_id = database_id

        self._query_type = ZTeraDBQueryType(ZTeraDBQueryType.NONE)
        self._fields: dict = dict()
        self._filters: dict = dict()
        self._filter_conditions: list = []
        self._limit = None
        self._sort: list = []
        self._related_fields:dict = dict()
        self._count = False

    def __str__(self):
        """Return a string representation of the query (schema and database)."""
        if self.database_id:
            return f"{self.database_id}.{self.schema_name}"

        else:
            return self.schema_name

    def __dict__(self):
        """Return the query fields as a dictionary."""
        return self.fields()

    def __setattr__(self, attribute, value):
        """
        Custom setter method for attributes in the ZTeraDBQuery class.

        This method is used to customize the behavior when setting an attribute on
        an instance of the `ZTeraDBQuery` class. If the attribute is not part of
        the predefined `QueryFields.fields`, the method will add the attribute to
        the `_fields` dictionary. If the attribute is part of the predefined fields,
        it will be set using the default behavior provided by the `super()` class.

        The method ensures that attributes that are not explicitly defined in `QueryFields.fields`
        are stored dynamically in the `_fields` dictionary, which allows flexibility for
        handling arbitrary attributes that may be passed during query construction.

        :param attribute: The name of the attribute being set.
        :param value: The value to be assigned to the attribute.

        :raises ValueError: If an invalid attribute is being assigned (not part of the valid fields).

        Example:
        query = ZTeraDBQuery("example_schema")
        query.some_dynamic_field = "some_value"  # Adds 'some_dynamic_field' to the _fields dictionary.
        print(query.some_dynamic_field)  # Output: some_value
        """
        if attribute not in QueryFields.fields:
            if not self._fields:
                self._fields = dict()
            self._fields[attribute] = value

        else:
            super().__setattr__(attribute, value)

    def __getattr__(self, attribute):
        """
        Custom getter method for attributes in the ZTeraDBQuery class.

        This method is used to customize the behavior when accessing an attribute
        on an instance of the `ZTeraDBQuery` class. If the attribute is not part of
        the predefined `QueryFields.fields`, the method will look for it in the
        `_fields` dictionary. If the attribute is found there, it will return its
        value. If the attribute is not found, the method will return `None`.
        If the attribute is part of the predefined `QueryFields.fields`,
        it will be accessed using the default behavior provided by the `super()` class.

        This allows for flexible handling of dynamic attributes not explicitly
        defined in the `QueryFields.fields`.

        :param attribute: The name of the attribute being accessed.
        :return: The value of the attribute if found, or `None` if not found.

        Example:
        query = ZTeraDBQuery("example_schema")
        query.some_dynamic_field = "some_value"
        print(query.some_dynamic_field)  # Output: some_value
        print(query.undefined_field)  # Output: None (if undefined_field is not set)
        """
        if attribute not in QueryFields.fields:
            if not self._fields:
                return None

            if attribute not in self._fields:
                return None

            return self._fields[attribute]

        else:
            return super().__getattribute__(attribute)

    def __delattr__(self, attribute):
        """
        Custom method for deleting an attribute from the ZTeraDBQuery instance.

        This method customizes the behavior for deleting attributes. If the attribute
        is not part of the predefined `QueryFields.fields`, it will attempt to delete
        the attribute from the `_fields` dictionary. If the attribute does not exist
        in `_fields`, it will first initialize `_fields` as an empty dictionary
        and then delete the attribute from it.

        If the attribute is part of the predefined `QueryFields.fields`, the method
        will call the base class's `__delattr__` method to delete the attribute
        using the default behavior.

        This method allows for dynamic removal of attributes that are stored
        in the `_fields` dictionary.

        :param attribute: The name of the attribute to delete.
        :raises KeyError: If the attribute is not found in `_fields` when it
                          is not part of the predefined `QueryFields.fields`.

        Example:
        query = ZTeraDBQuery("example_schema")
        query.some_dynamic_field = "some_value"
        del query.some_dynamic_field  # This deletes 'some_dynamic_field' from _fields
        """
        if attribute not in QueryFields.fields:
            if not self._fields:
                self._fields = dict()

            del self._fields[attribute]

        else:
            super().__delattr__(attribute)

    @property
    def schema_name(self):
        """
        Property method to get the schema name of the ZTeraDBQuery instance.

        This method provides access to the private `_schema_name` attribute, which
        stores the schema name associated with the query. It allows for the retrieval
        of the schema name without directly accessing the underlying attribute.

        :return: The schema name associated with the ZTeraDBQuery instance.
        :rtype: str

        Example:
        query = ZTeraDBQuery("example_schema")
        print(query.schema_name)  # Outputs: 'example_schema'
        """
        return self._schema_name

    @property
    def database_id(self):
        """
        Property method to get the database ID of the ZTeraDBQuery instance.

        This method provides access to the private `_database_id` attribute, which
        stores the database ID associated with the query. It allows for the retrieval
        of the database ID without directly accessing the underlying attribute.

        :return: The database ID associated with the ZTeraDBQuery instance.
        :rtype: str or None

        Example:
        query = ZTeraDBQuery("example_schema", "example_db")
        print(query.database_id)  # Outputs: 'example_db'
        """
        return self._database_id

    def set_database_id(self, database_id):
        self._database_id = database_id

    def set_env(self, env):
        self._env = env

    @property
    def query_type(self):
        """
        Property method to get the query type of the ZTeraDBQuery instance.

        This method provides access to the private `_query_type` attribute, which
        stores the type of the query (e.g., SELECT, INSERT, UPDATE, DELETE). It allows
        for the retrieval of the query type without directly accessing the underlying attribute.

        :return: The query type associated with the ZTeraDBQuery instance.
        :rtype: ZTeraDBQueryType

        Example:
        query = ZTeraDBQuery("example_schema")
        query.select()  # Sets the query type to SELECT
        print(query.query_type)  # Outputs: ZTeraDBQueryType.SELECT
        """
        return self._query_type

    @property
    def is_select_query(self):
        """
        Property method to check if the query type is a SELECT query.

        This method provides a boolean check to determine if the current query type
        is of type `SELECT`. It evaluates the value of the `query_type` attribute
        and returns `True` if the query type is `SELECT`, and `False` otherwise.

        :return: True if the query type is SELECT, otherwise False.
        :rtype: bool

        Example:
        query = ZTeraDBQuery("example_schema")
        query.select()  # Sets the query type to SELECT
        print(query.is_select_query)  # Outputs: True

        query.update()  # Sets the query type to UPDATE
        print(query.is_select_query)  # Outputs: False
        """
        return self.query_type == ZTeraDBQueryType.SELECT

    @property
    def related_fields(self):
        """
        Property method to access the related fields for the query.

        This method returns the `_related_fields` attribute, which contains
        the related field names and their associated query objects. Related fields
        are used to reference other queries that are related to the current query,
        often used in scenarios such as JOINs or sub-queries.

        :return: The dictionary containing related field names and their associated queries.
        :rtype: dict

        Example:
        query = ZTeraDBQuery("example_schema")
        related_query = ZTeraDBQuery("related_schema").select()
        query.related_field(field=related_query)  # Adds related field to the query
        print(query.related_fields)  # Outputs: {'field': {...related_query_data...}}

        Note:
        - The related fields are added using the `related_field` method. This method
          populates the `_related_fields` attribute with the related field names
          and the corresponding queries.
        """
        return self._related_fields

    @property
    def filter_conditions(self):
        """
        Property method to access the filter conditions for the query.

        This method returns the `_filter_conditions` attribute, which contains a list of
        filter conditions applied to the query. Filter conditions are used to restrict
        the results based on certain criteria (e.g., value ranges, exact matches, etc.).

        :return: A list of filter conditions associated with the query.
        :rtype: list

        Example:
        query = ZTeraDBQuery("example_schema")
        filter_condition = ZTGT(field="age", operator=">", value=30)
        query.filter_condition(filter_condition)  # Adds a filter condition to the query
        print(query.filter_conditions)  # Outputs: [{'field': 'age', 'operator': '>', 'value': 30}]

        Note:
        - The filter conditions are added using the `filter_condition` method. This method
          populates the `_filter_conditions` list with the specified filter conditions.
        """
        return self._filter_conditions

    def get_limit(self):
        """
        Property to retrieve the limit (pagination) settings for the query.

        This property checks whether a limit has been set for the query, and if so,
        it returns the limit as a tuple representing the starting and ending index
        (start, end) for pagination. If no limit has been set, it returns an empty list.

        :return: A tuple (start, end) representing the pagination limit, or an empty list if no limit is set.
        :rtype: tuple or list

        Example:
        query = ZTeraDBQuery("example_schema")

        # Set limit for pagination
        query.limit(0, 10)

        # Retrieve the set limit (start, end)
        print(query.get_limit)  # Output: (0, 10)

        # If no limit is set, get_limit will return an empty list
        query_without_limit = ZTeraDBQuery("example_schema")
        print(query_without_limit.get_limit)  # Output: []
        """
        if isinstance(self._limit, Limit):
            return self._limit.limit

        return []

    def set_query_type(self, query_type):
        """
        Set the query type for the current `ZTeraDBQuery` instance.

        This method is used to set the query type of the `ZTeraDBQuery` instance to a specified
        value. It ensures that the provided query type is an instance of the `ZTeraDBQueryType` enum
        and updates the `_query_type` attribute accordingly. If the provided query type is invalid,
        a `ValueError` is raised.

        :param query_type: The query type to be set, must be an instance of `ZTeraDBQueryType`.
        :type query_type: ZTeraDBQueryType

        :raises ValueError: If the provided `query_type` is not an instance of `ZTeraDBQueryType`.

        Example:
        query = ZTeraDBQuery("example_schema")
        query.set_query_type(ZTeraDBQueryType.SELECT)  # Sets the query type to SELECT
        print(query.query_type)  # Output: ZTeraDBQueryType.SELECT
        """
        if not isinstance(query_type, ZTeraDBQueryType):
            raise ValueError(f"'{query_type}' must be an instance of ZTeraDBQueryType ")

        self._query_type = query_type

    def insert(self):
        """
        Set the query type to INSERT.

        This method is used to set the query type for the current `ZTeraDBQuery` instance to
        `INSERT`. This prepares the query to insert data into the database when it is executed.

        The method updates the query type field to `ZTeraDBQueryType.INSERT` and returns the
        current instance of `ZTeraDBQuery`, allowing for method chaining.

        :return: The current `ZTeraDBQuery` instance with the query type set to `INSERT`.
        :rtype: ZTeraDBQuery

        Example:
        query = ZTeraDBQuery("example_schema")
        query.insert()  # Sets the query type to INSERT
        print(query.query_type)  # Output: ZTeraDBQueryType.INSERT
        """
        self.set_query_type(query_type=ZTeraDBQueryType.INSERT)
        return self

    def select(self):
        """
        Set the query type to SELECT for the current `ZTeraDBQuery` instance.

        This method is used to set the query type of the `ZTeraDBQuery` instance to `SELECT`. It
        utilizes the `set_query_type` method to ensure the correct query type is set. This is helpful
        when constructing a `SELECT` query using the `ZTeraDBQuery` class.

        :return: The current `ZTeraDBQuery` instance, allowing for method chaining.
        :rtype: ZTeraDBQuery

        Example:
        query = ZTeraDBQuery("example_schema")
        query.select()  # Sets the query type to SELECT
        print(query.query_type)  # Output: ZTeraDBQueryType.SELECT
        """
        self.set_query_type(query_type=ZTeraDBQueryType.SELECT)
        return self

    def update(self):
        """
        Set the query type to UPDATE for the current `ZTeraDBQuery` instance.

        This method is used to set the query type of the `ZTeraDBQuery` instance to `UPDATE`. It
        utilizes the `set_query_type` method to ensure the correct query type is set. This is helpful
        when constructing an `UPDATE` query using the `ZTeraDBQuery` class.

        :return: The current `ZTeraDBQuery` instance, allowing for method chaining.
        :rtype: ZTeraDBQuery

        Example:
        query = ZTeraDBQuery("example_schema")
        query.update()  # Sets the query type to UPDATE
        print(query.query_type)  # Output: ZTeraDBQueryType.UPDATE
        """
        self.set_query_type(query_type=ZTeraDBQueryType.UPDATE)
        return self

    def delete(self):
        """
        Set the query type to DELETE for the current `ZTeraDBQuery` instance.

        This method is used to set the query type of the `ZTeraDBQuery` instance to `DELETE`. It
        utilizes the `set_query_type` method to ensure the correct query type is set. This is helpful
        when constructing a `DELETE` query using the `ZTeraDBQuery` class.

        :return: The current `ZTeraDBQuery` instance, allowing for method chaining.
        :rtype: ZTeraDBQuery

        Example:
        query = ZTeraDBQuery("example_schema")
        query.delete()  # Sets the query type to DELETE
        print(query.query_type)  # Output: ZTeraDBQueryType.DELETE
        """
        self.set_query_type(query_type=ZTeraDBQueryType.DELETE)
        return self

    def fields(self, **kwargs):
        """
        Sets the fields for the query.

        This method allows you to specify the fields to be included in the query.
        If no arguments are passed, it returns the current set of fields.

        You can pass keyword arguments where the keys are field names and the values
        are the corresponding field values to be used in the query.

        param: **kwargs: Arbitrary keyword arguments where each key is a field name (string)
                      and the corresponding value is the field's value.
                      These values should not be objects.

        return:
            ZTeraDBQuery: The current instance of the ZTeraDBQuery with the updated fields.

        raises:
            ValueError: If the field name is not a string or the value is an object.

        Example:
            # To set fields for a query:
            query.fields(name="John", age=30)

            # To retrieve the fields set in the query:
            fields = query.fields()  # Returns the dictionary: {"name": "John", "age": 30}
        """
        if kwargs:
            for field, value in kwargs.items():
                if not isinstance(field, str) and field.strip():
                    raise ValueError(f"'{field}' must be  a schema field")

                if not isinstance(value, (str, int, float, bool, complex, bytes)) and isinstance(value, object):
                    raise ValueError(f"'{value}' must not be any object.")

                self._fields[field] = value
            return self

        return self._fields

    def related_field(self, **kwargs):
        """
        Add one or more related fields to the current query. A related field is a field that references
        another query. This method accepts keyword arguments where the key is the related field name
        (string) and the value is the associated ZTeraDBQuery instance.

        This method updates the `_related_fields` dictionary by adding related field names with their
        generated queries. It supports multiple related fields and allows for method chaining.

        :param kwargs: A dictionary of related fields where each key is a related field name
                       (string) and each value is an instance of ZTeraDBQuery.
        :return: The current ZTeraDBQuery instance, allowing for method chaining.
        :raises ValueError: If the related field name is not a string, or the related field query is
                             not an instance of ZTeraDBQuery.

        Example:
        query = ZTeraDBQuery("example_schema")
        related_query_1 = ZTeraDBQuery("related_schema_1").select()
        related_query_2 = ZTeraDBQuery("related_schema_2").select()

        query.related_field(
            related_field_1=related_query_1,
            related_field_2=related_query_2
        )

        # In the above example, the related fields 'related_field_1' and 'related_field_2'
        # are added to the query, each associated with a respective ZTeraDBQuery instance.
        """
        # Loop over each provided related_field argument
        for related_field_name, related_field_query in kwargs.items():
            if not isinstance(related_field_name, str):
                raise ValueError(f"'{related_field_name}' must be related field name ")

            if not isinstance(related_field_query, ZTeraDBQuery):
                raise ValueError(f"'{related_field_query}' must be an instance of ZTeraDBQuery")

            # Add the related field to the _related_fields dictionary with its generated query
            self._related_fields[related_field_name] = related_field_query.generate()

        # Return the current instance to allow for method chaining
        return self

    def filter(self, **kwargs):
        """
        Method to add filter criteria to the query.

        This method allows you to specify filter criteria for the query by providing
        field-value pairs. Each field represents a schema field in the query, and the
        corresponding value is the filter value associated with that field.

        The method will add the given field-value pairs to the `_filters` attribute, which
        contains all the filter criteria applied to the query.

        :param kwargs: Field-value pairs representing the filters to be applied to the query.
                       The field is expected to be a string (schema field name), and the
                       value should not be an object.

        :return: The current `ZTeraDBQuery` instance to allow for method chaining.
        :rtype: ZTeraDBQuery

        :raises ValueError: If any field is not a valid string or if the value is an object.

        Example:
        query = ZTeraDBQuery("example_schema")
        query.filter(age=30, city="New York")  # Adds filters for age and city
        print(query.filters)  # Outputs: {'age': 30, 'city': 'New York'}

        Note:
        - The `filter` method modifies the `_filters` attribute, which holds the filter
          conditions for the query. The filters are applied during query generation to
          restrict the results based on the provided criteria.
        """
        for field, value in kwargs.items():
            if not isinstance(field, str) and field.strip():
                raise ValueError(f"'{field}' must be a schema field")

            if value and not isinstance(value, (str, int, float, bool, complex, bytes)) and isinstance(value, object):
                raise ValueError(f"'{value}' must not be any object.")

            self._filters[field] = value

        return self

    def filters(self):
        """
        Retrieve the filter criteria for the query.

        This method returns the current set of filter conditions applied to the query.
        Filters are stored in the `_filters` attribute and are used to refine the results
        based on the specified conditions.

        :return: A dictionary containing all the field-value pairs used as filters.
        :rtype: dict

        Example:
        query = ZTeraDBQuery("example_schema")
        query.filter(age=30, city="New York")
        print(query.filters())  # Outputs: {'age': 30, 'city': 'New York'}

        Note:
        - The `filters` method allows access to the filter conditions that were added
          through the `filter` method or any other filtering mechanism. It helps in
          inspecting the current filter criteria.
        """
        return self._filters

    def filter_condition(self, filter_condition):
        """
        Add a filter condition to the query.

        This method allows the addition of a custom filter condition to the query. The
        provided `filter_condition` should be an instance of `ZTeraDBFilterCondition`.
        The method appends the filter condition's fields to the internal list of filter conditions.

        :param filter_condition: An instance of `ZTeraDBFilterCondition` that defines
                                  a custom filter to be added to the query.
        :type filter_condition: ZTeraDBFilterCondition

        :return: The current `ZTeraDBQuery` instance, allowing method chaining.
        :rtype: ZTeraDBQuery

        :raises ValueError: If the `filter_condition` is not an instance of `ZTeraDBFilterCondition`.

        Example:
        query = ZTeraDBQuery("example_schema")
        filter_condition = ZTGTE("age", ">=", 30)
        query.filter_condition(filter_condition)
        print(query.filter_conditions())  # Outputs: [{'age': '>= 30'}]

        Note:
        - The `filter_condition` method allows for flexible and dynamic filter conditions
          to be added to the query using instances of `ZTeraDBFilterCondition`.
        """
        if not isinstance(filter_condition, ZTeraDBFilterCondition):
            raise ValueError("'filter_condition' must be an instance of ZTeraDBFilterCondition")

        self._filter_conditions.append(filter_condition.get_fields())
        return self

    def sort(self, **kwargs):
        """
        Add sorting to the current query based on the specified fields and their respective sort order.
        The method accepts keyword arguments (`**fields`) where the key is the field name (string) and
        the value is the desired sort order (either 1 for ascending or -1 for descending).

        The `Sort` objects created for each field are appended to the `_sort` list. This allows for
        multiple fields to be sorted in a specific order, which will later be used when generating the query.

        :param kwargs: A dictionary where each key is the field name (string) to sort by,
                       and each value is the sort order (either 1 for ascending or -1 for descending).
        :return: The current `ZTeraDBQuery` instance, allowing for method chaining.
        :raises ValueError: If the provided order is not 1 (ascending) or -1 (descending).

        Example:
        query = ZTeraDBQuery("example_schema")

        # Sorting by 'name' in ascending order and 'age' in descending order
        query.sort(name=1, age=-1)

        # In the above example, 'name' will be sorted in ascending order,
        # and 'age' will be sorted in descending order.
        """
        # Loop over each field and its associated order
        for field, order in kwargs.items():
            # Create a Sort object for the field and order
            sort_order = Sort(field, order)

            # Append the created Sort object to the _sort list
            self._sort.append(sort_order)

        # Return the current instance to allow for method chaining
        return self

    def get_sort(self):
        """
        Retrieves the sorting order for the query results.

        This method returns a dictionary of fields and their respective sort order
        (either ascending or descending) for the query. The sorting is determined
        by the fields added to the `_sort` list using the `sort()` method.

        Returns:
            dict: A dictionary where the keys are the field names, and the values are
                  the corresponding sort order (1 for ascending, -1 for descending).

        Example:
            If the following sort fields were set:
            query.sort(name=1, age=-1)

            Calling `get_sort()` will return:
            {
                "name": 1,
                "age": -1
            }
        """
        return {sort.field: sort.sort_order for sort in self._sort if isinstance(sort, Sort)}

    def limit(self, start, end):
        """
        Sets the result limit for pagination.

        This method defines the range of results to return (for implementing "offset" and "limit"
        in SQL-like queries).

        param: start (int): The starting index for the result set.
        param: end (int): The ending index for the result set.

        return:
            ZTeraDBQuery: The current `ZTeraDBQuery` instance, allowing for method chaining.

        raises:
            ValueError: If `start` or `end` is not an integer.
        """
        if not isinstance(start, int):
            raise ValueError(f"Limit '{start}' must be an instance of the Limit")

        elif start < 0:
                raise ValueError(f"Limit '{start}' must not be negative")

        if not isinstance(end, int):
            raise ValueError(f"Limit '{start}' must be an instance of the Limit")

        if end is not None and end <= start:
            raise ValueError(f"Limit '{end}' must be greater than {start}")

        self._limit = Limit(start, end)
        return self

    def count(self):
        """
        Sets the query to return the count of the results rather than the actual records.

        This method is typically used when you only want the number of matching records,
        not the data itself.

        Returns:
            ZTeraDBQuery: The current `ZTeraDBQuery` instance, allowing for method chaining.
        """
        self._count = True
        return self

    @property
    def query(self):
        """
        Generates and returns the final query in dictionary format.

        This property calls the `generate()` method to construct the full query.

        Returns:
            dict: The query as a dictionary, including all the fields, filters, sorting, related fields, etc.
        """
        return self.generate()

    def generate(self):
        """
        Generates and returns the full query as a dictionary.

        Combines all attributes such as filters, sorting, fields, and limit into a complete query.

        Returns:
            dict: A dictionary representing the full query, including all attributes like
                  `fields`, `filters`, `limit`, `sort`, `related_fields`, and `count`.

        Raises:
            Exception: If no query type has been set (i.e., if `select()`, `insert()`, `update()`,
                        or `delete()` has not been called).
        """
        if not isinstance(self.query_type, ZTeraDBQueryType) or not self.query_type.value:
            raise ZTeraDBQueryError("You forgot to call either of select(), insert(), update() or delete() method.")

        query = Query(db=self.database_id, sh=self.schema_name, qt=self.query_type.value, fl=self.fields(), fi=self.filters(),
                      fc=self.filter_conditions, rf=self.related_fields, st=self.get_sort(), lt=self.get_limit(), cnt=self._count)

        return {key: val for key, val in query.__dict__.items() if val}
