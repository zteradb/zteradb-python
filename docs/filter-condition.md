# ZTeraDB Filter Complex Condition Functions
Filter condition functions enable the creation of complex filter conditions. These functions support various operations, including multiplication, addition, equality checks, logical operations like `AND`, `OR`, `>`, `<`, `>=`, `<=`, `in`, and string operations like `contains`, `starts with`, `ends with`. Errors are triggered when invalid parameters or missing values are encountered.


## Table of Contents
1. [Equal filter](#ztequalkey-any-value-any)
2. [Addition Filter](#ztaddparams-list)
3. [Substraction Filter](#ztsubparams-list)
4. [Multiplication Filter](#ztmulparams-list)
5. [Division Filter](#ztdivdividend-divisor)
6. [Modulo Filter](#ztmoddividend-divisor)
7. [Filed in list Filter](#ztinfield-string-values-list)
8. [String Contains Filter](#ztcontainsfield-string-value-string)
9. [String Case-insensitive contains Filter](#zticontainsfield-string-value-string)
10. [String Starts with Filter](#ztstartswithfield-string-value-string)
11. [String Case-insensitive Starts with Filter](#ztistartswithfield-string-value-string)
12. [String Ends with Filter](#ztendswithfield-string-value-string)
13. [String Case-insensitive Ends with Filter](#ztiendswithfield-string-value-string)
14. [Greater than Filter](#ztgtvalues-list)
15. [Greater than or equal to Filter](#ztgtevalues-list)
16. [Less than Filter](#ztltvalues-list)
17. [Less than or equal to Filter](#ztltevalues-list)
18. [AND Filter](#ztandfilters-list)
19. [OR Filter](#ztorfilters-list)



### `ZTEQUAL(key: any, value: any)`
- **Description**: The `ZTEQUAL` function applies an equality filter to compare the `key` (left side) and `value` (right side) arguments, then returns a new `FilterCondition` instance. This `FilterCondition` will later be used to build and execute a query. You can combine this filter with other filters to create more complex queries.

- **Parameters**:
  - `key` (Any): The field (or expression) to be compared on the left side of the equation.
    - **Value**: A constants.
    - **Field**: Schema field.
    - **FilterCondition**: any ZT* function.

    - **Example**: A field name (e.g., `"age"`) or an expression (e.g., `ZTMUL("price", 2)` which multiplies the "price" field by 2).
    - **Usage**: You can use any valid field or expression that you want to compare.
  
  - `value` (Any): The value (or expression) to be compared to the `key` on the right side of the equation.
    - **Value**: A constants.
    - **Field**: Schema field.
    - **FilterCondition**: Any ZT* function.

    - **Example**: A field value (e.g., `30` or `"active"`) or an expression (e.g., `ZTMUL("quantity", 5)`).
    - **Usage**: This is the value or result of an expression that you want to compare against the `key`.

- **Returns**: 
  - **`FilterCondition`**: A new instance of `FilterCondition` with the equality filter applied. This `FilterCondition` will be passed as an argument to `ZTeraDBQuery.FilterCondition()` or other functions that support filter conditions, allowing you to apply your filter to a query.

- **Throws**: 
  - **`ZTeraDBError`**: If invalid parameters are passed (e.g., the `key` or `value` is missing or of an incorrect type), the function will throw an error.

- **Use Case**:
  - Use `ZTEQUAL` when you need to find records based on a comparison between two fields or between a field and a specific value.
  - **Example Use Case**: To find all users with an "age" equal to 30, you can write: `ZTEQUAL('age', 30)`. Or to check if a field’s value is equal to another field’s calculated value, like `ZTEQUAL(ZTMUL('price', 2), 100)`, where you compare twice the price to 100.

### Example

```python

from zteradb import ZTeraDBQuery, ZTMUL, ZTEQUAL

# Example 1: Simple equality check
filterCondition = ZTEQUAL("age", 30) 
# This checks if the "age" field is equal to 30

# Generate the query.
query = ZTeraDBQuery("users") \
  .select() \
  .filterCondition(filterCondition)
# This query fetches all users where age is 30

# Example 2: Using expressions in the equality filter
filterCondition2 = ZTEQUAL(
  ZTMUL(["price", 2]),
  100
)
# This checks if 2 times the value of "price" equals 100

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)
# This query fetches all products where "price * 2" equals 100


# Example 3: Suppose you have a table called "product" with the fields "name", "price", and "quantity".
# To retrieve all products where the name is "Tea", you can use the following approach:

# Apply the equality filter on the 'name' field to check if it matches "Tea"
filterCondition = ZTEQUAL('name', 'Tea')  # Interpreted as name = 'Tea'

# Generate the query.
query3 = ZTeraDBQuery("product") \
  .select() \
  .filterCondition(filterCondition) # Attach the filter conditions to the query      

# The query will now fetch all products from the "product" table where the "name" is "Tea"

```

---

### `ZTADD(params: list)`
- **Description**: The `ZTADD` function creates a addition filter for the values provided in the `params` list. It returns a new `FilterCondition` instance that can be used later to build and execute a query. This filter is often used in combination with other filters, such as `ZTEQUAL`, to create more complex queries.
- **Parameters**:
  - `params` (list): List of values, fields, or filter conditions (any ZT* function) to addition. The addition can occur between:
    - **Values**: List of constants.
    - **Fields**: List of schema fields.
    - **FilterCondition**: List of ZT* functions.
    - **Field, Value, FilterCondition**: A combination of list of schema field, constant, and ZT* functions.

    - **Example**: `["price", "discount"]` (price + discount) or `[200, "price"]` (price + 200). here price, discount are schema fields.

- **Returns**:
  - A new `FilterCondition` instance with the addition filter applied. This can later be used in query-building methods like `ZTeraDBQuery.FilterCondition()`.

- **Throws**:
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported combinations of fields or data types.

- **Use Case**:
  - Use `ZTSUB` when you need to filter records based on the difference between two fields, a field and a constant, or even between ZT* functions. You can combine `ZTSUB` with other filters (e.g., `ZTEQUAL`) to match the subtraction result against another field or constant.

  - **Example**: Subtract the `discount` from `price` and check if the result equals a specific value using `ZTSUB` and `ZTEQUAL`.

- **Note**:
  - Based on your use case, you pass n number of fields / values / FilterCondition to add with each other.

### Example:

```python

from zteradb import ZTeraDBQuery, ZTADD, ZTEQUAL

# Example 1: Subtract two fields - "price" and "discount"
filterCondition = ZTEQUAL(ZTADD(["price", "discount"]), 150)
# This checks if price + discount equals 150

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

# Example 2: Subtract a constant from a field
filterCondition2 = ZTEQUAL(ZTADD(["price", 200]), 50)
# This checks if price + 200 equals 50

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)

```

---


### `ZTSUB(params: list)`
- **Description**: The `ZTSUB` function creates a subtraction filter for the values provided in the `params` list. It returns a new `FilterCondition` instance that can be used later to build and execute a query. This filter is often used in combination with other filters, such as `ZTEQUAL`, to create more complex queries.
  
- **Parameters**:
  - `params` (List): A list of values, fields, or any ZT* functions to subtract. The subtraction can occur between:
    - **Values**: List of constants.
    - **Fields**: List of schema fields.
    - **FilterCondition**: List of ZT* functions.
    - **Field, Value, FilterCondition**: A combination of list of schema field, constant, and ZT* functions.

    - **Example**: `["price", "discount"]` (price - discount) or `[200, "price"]` (200 - price). here price, discount are schema fields.
  
- **Returns**: 
  - Based on your use case, you pass n number of fields / values / ZT* functions to substract from each other.
  
- **Throws**: 
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported combinations of fields or data types.

- **Use Case**:
  - Use `ZTSUB` when you need to filter records based on the difference between two fields, a field and a constant, or even between filter conditions. You can combine `ZTSUB` with other filters (e.g., `ZTEQUAL`) to match the subtraction result against another field or constant.

  - **Example**: Subtract the `discount` from `price` and check if the result equals a specific value using `ZTSUB` and `ZTEQUAL`.

- **Note**:
  - if you pass n number of fields / values / ZT* functions to substract from each other. 


### Example:

```python

from zteradb import ZTeraDBQuery, ZTSUB, ZTEQUAL


# Example 1: Subtract two fields - "price" and "discount"
filterCondition = ZTEQUAL(ZTSUB(["price", "discount"]), 150)
# This checks if price - discount equals 150

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

# Example 2: Subtract a constant from a field
filterCondition2 = ZTEQUAL(ZTSUB(["price", 200]), 50)
# This checks if price - 200 equals 50

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)

```

---


### `ZTMUL(params: list)`
- **Description**: The `ZTMUL` function creates a multiplication filter for the values provided in the `params` list. It returns a new `FilterCondition` instance that can later be used in query-building, often in combination with other filters like `ZTEQUAL`.
  
- **Parameters**:
  - `params` (List): A list of values, fields, or any ZT* functions to multiply together.
    - **Values**: List of constants.
    - **Fields**: List of schema fields.
    - **FilterCondition**: List of ZT* functions.
    - **Field, Value, FilterCondition**: A combination of list of schema field, constant, and ZT* function.

    - **Example**: `["price", "quantity"]` or `[2, 5]` or `[ZTSUB("price", "discount"), 10]`. The price, quantity and discount are schema fields.
  
- **Returns**:
  - A new `FilterCondition` instance with the multiplication filter applied. This can be used as part of a query to filter records based on the result of the multiplication.
  
- **Throws**: 
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - Use `ZTMUL` when you need to filter records based on the product of two or more fields, or a combination of fields and constants.

### Example:

```python

from zteradb import ZTeraDBQuery, ZTMUL, ZTEQUAL

# Example 1: Multiply two fields - "price" and "quantity"
filterCondition = ZTEQUAL(ZTMUL(["price", "quantity"]), 10000)
# This checks if price * quantity equals 10,000

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

# Example 2: Multiply a constant and a field
filterCondition2 = ZTEQUAL(ZTMUL([2, "price"]), 100)
# This checks if 2 times the price equals 100

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)

```

---

### `ZTDIV(dividend, divisor)`
- **Description**: Applies a division filter to dividend and divisor and returns a new `FilterCondition` instance which will be later used to prepare the filter conditions query. It will be used with some other combination.

- **Parameters**:
  - `dividend` (any): The divisor can be a constant, schema field, or any filter conditions (ZT* function).
    - **Value**: A constant.
    - **Field**: A schema field.
    - **FilterCondition**: A ZT* function.

  - `divisor` (any): The divisor can be a constant, schema field, or any filter conditions (ZT* function).
    - **Value**: A constant.
    - **Field**: A schema field.
    - **FilterCondition**: A ZT* function.

- **Returns**:
  - A new `FilterCondition` instance with the division filter applied. This can be used as part of a query to filter records based on the result of the division.

- **Throws**:
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - If you need to find records based on the division of two schema fields or values, and the result must match a specific field's value or a constant, you can use the ZTDIV filter in conjunction with the ZTEQUAL function.

- **Example**:

```python

from zteradb import ZTeraDBQuery, ZTDIV, ZTEQUAL

# Example 1: Divide two fields - "price" and "quantity"
filterCondition = ZTEQUAL(ZTDIV("price", "quantity"), 10000)
# This checks if price / quantity equals 10,000

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

# Example 2: Divide a constant and a field
filterCondition2 = ZTEQUAL(ZTDIV("price", 2), 100)
# This checks if the price dived by 2 equals 100

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)

```

---

### `ZTMOD(dividend, divisor)`
- **Description**: Applies a modulo filter to dividend and divisor and returns a new `FilterCondition` instance which will be later used to prepare the filter conditions query. It will be used with some other combination.

- **Parameters**:
  - `dividend` (any): The divisor can be a constant, schema field, or any filter conditions (ZT* function).
    - **Value**: A constant.
    - **Field**: A schema field.
    - **FilterCondition**: A ZT* function.

  - `divisor` (any): The divisor can be a constant, schema field, or any filter conditions (ZT* function).
    - **Value**: A constant.
    - **Field**: A schema field.
    - **FilterCondition**: A ZT* function.

- **Returns**:
  - A new `FilterCondition` instance with the modulo filter applied. This can be used as part of a query to filter records based on the result of the modulo.

- **Throws**:
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - If you need to find records based on the modulo of two schema fields or values, and the result must match a specific field's value or a constant, you can use the ZTMOD filter in conjunction with the ZTEQUAL, ZTLT, ZTGT, etc functions.

- **Example**:

```python

from zteradb import ZTeraDBQuery, ZTMOD, ZTEQUAL, ZTGT

# Example 1: Modulo two fields - "price" and "discount"
filterCondition = ZTEQUAL(ZTMOD("price", "discount"), 1)
# This checks if price % discount equals 1

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)
# ... pass the query to connection.run() method.

# Example 2: Modulo a constant and a field
filterCondition2 = ZTGT([ZTMOD("price", 21), 18])
# This checks if the (price % 21) > 18

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)

# ... pass the query2 to connection.run() method.
```

---


### `ZTIN(field: string, values: list)`
- **Description**: Applies a schema field in filter to the values and returns a new `FilterCondition` instance which will be later used to prepare the filter conditions query.
- **Parameters**:
  - `field` (string): The field is schema field name.
  - `values` (list): A list of values, fields, or any ZT* functions to multiply together.
    - **Values**: A list of constants.
    - **Fields**: A list of schema fields.
    - **FilterCondition**: A list of ZT* functions.
    - **Field, Value, FilterCondition**: A combination of list of schema field, constant, and ZT* function.

    - **Example**: `["price", "quantity"]` or `[2, 5]` or `[ZTSUB("price", "discount"), 10]`. The price, quantity and discount are schema fields.

- **Returns**:
  - A new `FilterCondition` instance with the `in` filter applied. This can be used as part of a query to filter records.

- **Throws**:
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - To find records based on a combination of schema fields and constants.

- **Example**:

```python

from zteradb import ZTeraDBQuery
from zteradb.zteradb_filter_functions import ZTIN

# Example: Checks if age fall in 20 or 30
filterCondition = ZTIN("age", [20, 30])

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

```

---

### `ZTCONTAINS(field: string, value: string)`
- **Description**: The `ZTICONTAINS` function is used to find a case-sensitive substring within a schema field's data. It returns a new `FilterCondition` instance that can later be used to build the filter query.
- **Parameters**:
  - `field` (string): The field is schema field name.
  - `value` (string): A substring contained within the value of a schema field.

- **Returns**:
  - A new `FilterCondition` instance with the `like` filter applied to the filter.

- **Throws**:
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - To find records where the value appears anywhere within the schema field's data.

- **Example**:

```python

from zteradb import ZTeraDBQuery, ZTCONTAINS

# Example 1: Case-sensitive search for product names containing the letter "a"
filterCondition = ZTCONTAINS("product_name", "a")

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

```

---

### `ZTICONTAINS(field: string, value: string)`
- **Description**: The `ZTICONTAINS` function is used to find a case-insensitive substring within a schema field's data. It returns a new `FilterCondition` instance that can later be used to build the filter query.
- **Parameters**:
  - `field` (string): The field is schema field name.
  - `value` (string): A substring contained within the value of a schema field.

- **Returns**:
  - A new `FilterCondition` instance with the `ilike` filter applied to the filter.

- **Throws**:
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - To find records where the value appears anywhere within the schema field's data.

- **Example**:

```python

from zteradb import ZTeraDBQuery, ZTICONTAINS

# Example 1: Case-insensitive search for product names containing the letter "a"
filterCondition = ZTICONTAINS("product_name", "a")

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

```

---

### `ZTSTARTSWITH(field: string, value: string)`
- **Description**: The `ZTSTARTSWITH` function is used to find records where a schema field's data starts with a specific, case-sensitive substring. It returns a new `FilterCondition` instance that can later be used to construct the filter query.
- **Parameters**:
  - `field` (string): The field is schema field name.
  - `value` (string): A substring contained within the value of a schema field.

- **Returns**:
  - A new `FilterCondition` instance with the `like` filter applied to the filter.

- **Throws**:
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - To find records where the value case-sensitively starts with a specific substring in the schema field's data.

### Example:

```python

from zteradb import ZTeraDBQuery, ZTSTARTSWITH

# Example 1: Case-sensitive search for product names starts with the letter "a"
filterCondition = ZTSTARTSWITH("product_name", "a")

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

```

---

### `ZTISTARTSWITH(field: string, value: string)`
- **Description**: The `ZTISTARTSWITH` function is used to find records where a schema field's data starts with a specific, case-insensitive substring. It returns a new `FilterCondition` instance that can later be used to construct the filter query.
- **Parameters**:
  - `field` (string): The field is schema field name.
  - `value` (string): A substring contained within the value of a schema field.

- **Returns**:
  - A new `FilterCondition` instance with the `ilike` filter applied to the filter.

- **Throws**:
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - To find records where the value case-insensitively starts with a specific substring in the schema field's data.

### Example:

```python

from zteradb import ZTeraDBQuery, ZTISTARTSWITH

# Example 1: Case-sensitive search for product names starts with the letter "a"
filterCondition = ZTISTARTSWITH("product_name", "a")

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

```

---

### `ZTENDSWITH(field: string, value: string)`
- **Description**: The `ZTENDSWITH` function is used to find records where a schema field's data ends with a specific, case-sensitive substring. It returns a new `FilterCondition` instance that can later be used to construct the filter query.
- **Parameters**:
  - `field` (string): The field is schema field name.
  - `value` (string): A substring contained within the value of a schema field.

- **Returns**:
  - A new `FilterCondition` instance with the `like` filter applied to the filter.

- **Throws**:
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - To find records where the value case-sensitively ends with a specific substring in the schema field's data.

### Example:

```python

from zteradb import ZTeraDBQuery, ZTENDSWITH

# Example 1: Case-sensitive search for product names starts with the letter "a"
filterCondition = ZTENDSWITH("product_name", "a")
# filters all products where product_name starts with "a"

query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

```

---

### `ZTIENDSWITH(field: string, value: string)`
- **Description**: The `ZTIENDSWITH` function is used to find records where a schema field's data ends with a specific, case-insensitive substring. It returns a new `FilterCondition` instance that can later be used to construct the filter query.
- **Parameters**:
  - `field` (string): The field is schema field name.
  - `value` (string): A substring contained within the value of a schema field.

- **Returns**:
  - A new `FilterCondition` instance with the `ilike` filter applied to the filter.

- **Throws**:
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - To find records where the value case-insensitively ends with a specific substring in the schema field's data.

### Example:

```python

from zteradb import ZTeraDBQuery, ZTIENDSWITH

# Example 1: Case-insensitive search for product names ends with the letter "a"
filterCondition = ZTIENDSWITH("product_name", "a")

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

```

---

### `ZTGT(values: list)`
- **Description**: The ZTGT function generates a "greater than" filter for the values provided in the values list. It returns a new FilterCondition instance that can be utilized later in query construction. Additionally, this function supports the BETWEEN AND query, enabling you to filter schema fields within a specific range.
  
- **Parameters**:
  - `values` (list): A list of values, fields, or any ZT* functions to multiply together.
    - **Values**: A list of constants.
    - **Fields**: A list of schema fields.
    - **FilterCondition**: A list of ZT* functions.
    - **Field, Value, FilterCondition**: A combination of list of schema field, constant, and ZT* function.

    - **Example**: `["price", "quantity"]` or `[2, 5]` or `[ZTSUB("price", "discount"), 10]`. The price, quantity and discount are schema fields.
  
- **Returns**:
  - A new `FilterCondition` instance with the greater than filter applied. This can be used as part of a query to filter records based on the result of the greater than.
  
- **Throws**: 
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - Use `ZTGT` when you need to filter records based on the greater than of two or more fields, or a combination of fields and constants.

### Example:

```python

from zteradb import ZTeraDBQuery, ZTGT, ZTMUL

# Example 1: Multiply two fields - "price" and "quantity"
filterCondition = ZTGT(["price", "discount"])
# This checks if price > discount

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

# Example 2: Multiply a constant and a field
filterCondition2 = ZTGT([100, "price", 200])
# This checks if 100 > price > 200.

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)

# Example 2: Multiply a constant and a field
filterCondition3 = ZTGT([
  "price", ZTMUL(["discount", 2])
])
# This checks if price > (discount * 2).

# Generate the query.
query3 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition3)

```

---

### `ZTGTE(values: list)`
- **Description**: The ZTGTE function generates a "greater than or equal to" filter for the values provided in the values list. It returns a new FilterCondition instance that can be utilized later in query construction. Additionally, this function supports the BETWEEN AND query, enabling you to filter schema fields within a specific range.
  
- **Parameters**:
  - `values` (list): A list of values, fields, or any ZT* functions to multiply together.
    - **Values**: A list of constants.
    - **Fields**: A list of schema fields.
    - **FilterCondition**: A list of ZT* functions.
    - **Field, Value, FilterCondition**: A combination of list of schema field, constant, and ZT* function.

    - **Example**: `["price", "discount"]` or `[200, price, 500]` or `[ZTSUB("price", "discount"), 10]`. The price, quantity and discount are schema fields.
  
- **Returns**:
  - A new `FilterCondition` instance with the greater than or equal to filter applied. This can be used as part of a query to filter records based on the result of the greater than.
  
- **Throws**: 
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - Use `ZTGTE` when you need to filter records based on the greater than or equal to of two or more fields, or a combination of fields and constants.

### Example:

```python

from zteradb import ZTeraDBQuery, ZTGTE, ZTMUL

# Example 1: Multiply two fields - "price" and "quantity"
filterCondition = ZTGTE(["price", "discount"])
# This checks if price >= discount

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

# Example 2: Multiply a constant and a field
filterCondition2 = ZTGTE([100, "price", 200])
# This checks if 100 >= price >= 200.

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)

# Example 2: Multiply a constant and a field
filterCondition3 = ZTGTE([
  "price", ZTMUL(["discount", 2])
])
# This checks if price >= (discount * 2).

# Generate the query.
query3 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition3)

```

---


### `ZTLT(values: list)`
- **Description**: The ZTLT function generates a "less than" filter for the values provided in the values list. It returns a new FilterCondition instance that can be utilized later in query construction. Additionally, this function supports the BETWEEN AND query, enabling you to filter schema fields within a specific range.
  
- **Parameters**:
  - `values` (list): A list of values, fields, or any ZT* functions to multiply together.
    - **Values**: A list of constants.
    - **Fields**: A list of schema fields.
    - **FilterCondition**: A list of ZT* functions.
    - **Field, Value, FilterCondition**: A combination of A list of schema field, constant, and ZT* function.

    - **Example**: `["price", "quantity"]` or `[2, 5]` or `[ZTSUB("price", "discount"), 10]`. The price, quantity and discount are schema fields.
  
- **Returns**:
  - A new `FilterCondition` instance with the less than filter applied. This can be used as part of a query to filter records based on the result of the less than.
  
- **Throws**: 
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - Use `ZTLT` when you need to filter records based on the less than of two or more fields, or a combination of fields and constants.

### Example:

```python

from zteradb import ZTeraDBQuery, ZTLT, ZTMUL

# Example 1: Multiply two fields - "price" and "quantity"
filterCondition = ZTLT(["price", "discount"])
# This checks if price < discount

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

# Example 2: Multiply a constant and a field
filterCondition2 = ZTLT([100, "price", 200])
# This checks if 100 < price < 200.

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)

# Example 2: Multiply a constant and a field
filterCondition3 = ZTLT([
  "price", ZTMUL(["discount", 2])
])
# This checks if price < (discount * 2).

# Generate the query.
query3 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition3)

```

---

### `ZTLTE(values: list)`
- **Description**: The `ZTLTE` function generates a "less than or equal to" filter for the values provided in the values list. It returns a new FilterCondition instance that can be utilized later in query construction. Additionally, this function supports the BETWEEN AND query, enabling you to filter schema fields within a specific range.
  
- **Parameters**:
  - `values` (list): A list of values, fields, or any ZT* functions to multiply together.
    - **Values**: A list of constants.
    - **Fields**: A list of schema fields.
    - **FilterCondition**: A list of ZT* functions.
    - **Field, Value, FilterCondition**: A combination of a list of schema field, constant, and ZT* function.

    - **Example**: `["price", "discount"]` or `[200, price, 500]` or `[ZTSUB("price", "discount"), 10]`. The price, quantity and discount are schema fields.
  
- **Returns**:
  - A new `FilterCondition` instance with the less than or equal to filter applied. This can be used as part of a query to filter records based on the result of the less than.
  
- **Throws**: 
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - Use `ZTLTE` when you need to filter records based on the less than or equal to of two or more fields, or a combination of fields and constants.

### Example:

```python
from zteradb import ZTeraDBQuery, ZTLTE, ZTMUL

# Example 1: Multiply two fields - "price" and "quantity"
filterCondition = ZTLTE(["price", "discount"])
# This checks if price <= discount

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

# Example 2: Multiply a constant and a field
filterCondition2 = ZTLTE([100, "price", 200])
# This checks if 100 <= price <= 200.

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)

# Example 2: Multiply a constant and a field
filterCondition3 = ZTLTE([
  "price", ZTMUL(["discount", 2])
])
# This checks if price <= (discount * 2).

# Generate the query.
query3 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition3)

```

---

### `ZTAND(filters: list)`
- **Description**: The `ZTAND` function creates an `AND` filter using the filters provided in the `filters` list. It returns a new `FilterCondition` instance, which can be used later in query construction. This function is especially useful when you need to retrieve records that satisfy both conditions.
  
- **Parameters**:
  - `filters` (list): A list of filter conditions to be combined with an AND operator.
    - **FilterCondition**: A list of ZT* functions.

    - **Example**: `ZTEQUAL("product_name", "xyz")` or `ZTGT([200, price, 500])` or `ZTEQUAL(ZTSUB("price", "discount"), 10)`. `product_name` and `price` are fields in the schema.
  
- **Returns**:
  - A new `FilterCondition` instance with the `AND` operator applied to the filters.
  
- **Throws**: 
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - Use `ZTAND` when you need to filter records based on multiple conditions, where all conditions must be true.

### Example:

```python

from zteradb import  ZTeraDBQuery, ZTAND, ZTLTE, ZTGTE, ZTEQUAL, ZTISTARTSWITH

# Example 1: Multiply two fields - "price" and "quantity"
filterCondition = ZTAND([
  ZTLTE(["price", "discount"]),
  ZTGTE(["price", 100]),
])
# This checks if price <= discount and price >= 100

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

# Example 2: Multiply a constant and a field
filterCondition2 = ZTAND([
  ZTEQUAL("product_code", "ZT0001"),
  ZTISTARTSWITH("product_name", "t"),
])
# This checks if product_code = "ZT0001" and product_name ilike "t%"

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)
```

---

### `ZTOR(filters: list)`
- **Description**: The `ZTOR` function creates an `OR` filter using the filters provided in the `filters` list. It returns a new `FilterCondition` instance, which can be used later in query construction. This function is especially useful when you need to retrieve records that satisfy both conditions.
  
- **Parameters**:
  - `filters` (list): A list of filter conditions to be combined with an OR operator.
    - **FilterCondition**: A list of ZT* functions.

    - **Example**: 
    ```python

      ZTEQUAL("product_name", "xyz")
      
      or
      
      ZTGT([200, price, 500])
      
      or
      
      ZTEQUAL(ZTSUB("price", "discount"), 10)

    ```
    `product_name` and `price` are fields in the schema.
  
- **Returns**:
  - A new `FilterCondition` instance with the `OR` operator applied to the filters.
  
- **Throws**: 
  - **`ZTeraDBError`** if invalid parameters are passed, such as unsupported data types.

- **Use Case**:
  - Use `ZTOR` when you need to filter records based on multiple conditions, where at least one condition must be true.

### Example:

```python

from zteradb import ZTeraDBQuery, ZTOR, ZTLTE, ZTGTE, ZTEQUAL, ZTISTARTSWITH

# Example 1: Multiply two fields - "price" and "quantity"
filterCondition = ZTOR([
  ZTLTE(["price", "discount"]),
  ZTGTE(["price", 100]),
])
# This checks if price <= discount or price >= 100

# Generate the query.
query = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition)

# Example 2: Multiply a constant and a field
filterCondition2 = ZTOR([
  ZTEQUAL("product_code", "ZT0001"),
  ZTISTARTSWITH("product_name", "t"),
])
# This checks if product_code = "ZT0001" or product_name ilike "t%"

# Generate the query.
query2 = ZTeraDBQuery("products") \
  .select() \
  .filterCondition(filterCondition2)

```

---
