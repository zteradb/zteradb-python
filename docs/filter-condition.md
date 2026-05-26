---
sidebar_position: 5
---

# 🎛️ Filter Conditions

This guide provides a comprehensive breakdown of the functional Abstract Syntax Tree (AST) operators available in ZTeraDB. Use these functional helpers to construct intricate, multi-layered queries that go beyond basic key-value matching.

Every helper function returns a `FilterCondition` instance that must be passed directly into your query builder pipeline:

```python
query.filter_condition(condition)
```

## 🎯 Categories Overview

ZTeraDB filter functions are organized into four operational layers:
1. **Comparison Operators:** Evaluate mathematical boundaries and set definitions.
2. **Mathematical Evaluators:** Execute calculations inline within database computations.
3. **String Pattern Matching:** Perform case-sensitive and case-insensitive text lookups.
4. **Logical Aggregators:** Nest multiple expressions together using boolean logic.

---

### 1️⃣ Comparison Operators
Comparison operators evaluate fields against scalar values or other operational expressions.

#### ZTEQUAL(left, right)

Evaluates if the left expression strictly equals the right expression (a = b).

```python
# Check column against scalar value
ZTEQUAL('age', 25)

# Check mathematical resolution against scalar value
ZTEQUAL(ZTMUL(['price', 2]), 100)
```

**SQL Equivalent**
```sql
```

#### ZTGT(expressions)
Evaluates if the first parameter is strictly greater than the second parameter (a > b).

```python
ZTGT(['age', 18])
ZTGT(['price', ZTMUL(['discount', 2])])
```
**SQL Equivalent**
```sql
age > 18;

price > (discount * 2);
```

#### ZTGTE(expressions)
Evaluates if the first parameter is greater than or equal to the second parameter (a ≥ b).

```python
ZTGTE(['salary', 40000])
```

**SQL Equivalent**
```sql
salary >= 40000;
```

#### ZTLT(expressions)
Evaluates if the first parameter is strictly less than the second parameter (a < b).


```python
ZTLT(['age', 65])
```

**SQL Equivalent**
```sql
age < 65;
```


#### ZTLTE(expressions)
Evaluates if the first parameter is less than or equal to the second parameter (a ≤ b).

```python
ZTLTE(['rating', 5])
```
**SQL Equivalent**
```sql
rating <= 5;
```

#### ZTIN(field, values)
Determines if a specified field matches any value within a given literal list.

```python
ZTIN('age', [20, 25, 30])
```

**SQL Equivalent**
```sql
age IN (20, 25, 30);
```

---

### 2️⃣ Mathematical Evaluators
These expressions transform numerical data inline during query resolution before evaluating constraints.

These expressions transform numerical data inline during query resolution before evaluating constraints.

| Function | Argument Type | Operational Action | SQL Equivalent |
| :--- | :--- | :--- | :--- |
| `ZTADD()` | `list` | Sums multiple fields or values together ($a + b + c$) | `(field1 + field2)` |
| `ZTSUB()` | `list` | Subtracts the second value from the first ($a - b$) | `(field1 - field2)` |
| `ZTMUL()` | `list` | Multiplies values together sequentially ($a \times b$) | `(field1 * field2)` |
| `ZTDIV()` | `list` | Divides the first value by the second ($a \div b$) | `(field1 / field2)` |
| `ZTMOD()` | `list` | Calculates the remainder of a division operation ($a \bmod b$) | `(field1 % field2)` |

### Math-Infused Query Example:
```python
# Compiles to: WHERE (price - discount) = 150
condition = ZTEQUAL(
    ZTSUB(['price', 'discount']), 
    150
)

```

## 3️⃣ String Pattern Matching
String operators compile into optimized SQL LIKE syntax patterns. Functions containing an internal `I` flag (e.g., `ZTICONTAINS`) apply `LOWER()` wrappers on data fields to enforce case-insensitive evaluations.

### Substring Search (CONTAINS)

```python
# Case-Sensitive
ZTCONTAINS('name', 'Tea') # WHERE name LIKE '%Tea%'

# Case-Insensitive
ZTICONTAINS('name', 'john') # WHERE LOWER(name) LIKE '%john%'
```

### Prefix Scan (STARTSWITH)

```python
# Case-Sensitive
ZTSTARTSWITH('product_code', 'A-') # WHERE product_code LIKE 'A-%'

# Case-Insensitive
ZTISTARTSWITH('product_code', 'a-') # WHERE LOWER(product_code) LIKE 'a-%'
```

### Suffix Scan (ENDSWITH)
```python
# Case-Sensitive
ZTENDSWITH('email', '.com') # WHERE email LIKE '%.com'

# Case-Insensitive
ZTIENDSWITH('email', '.COM') # WHERE LOWER(email) LIKE '%.com'
```

## 4️⃣ Logical Aggregators
Logical operators allow you to build deeply nested boolean logic trees by passing lists of discrete `FilterCondition` objects.

### `ZTAND(conditions)`
Combines multiple condition blocks. Every expression within the list must evaluate to true.

```python
ZTAND([
    ZTGTE(['age', 18]),
    ZTLT(['age', 30])
])
```

**SQL Equivalent**
```sql
(age >= 18) AND (age < 30);
```

### `ZTOR(conditions)`
Evaluates to true if at least one conditional block within the list resolves to true.

```python
ZTOR([
    ZTEQUAL('status', 'A'),
    ZTEQUAL('status', 'D')
])
```

**SQL Equivalent**
```sql
(status = 'A') OR (status = 'D');
```

## 🧪 Comprehensive Blueprint Example
The example below demonstrates how to fetch products using complex mathematical evaluations combined with text scans.

### Target Goal:
> "Find all products where the calculation of `(price * quantity) > 500` **AND** the `name` property contains the word `'wire'` (ignoring capitalization mismatch)."


```python
from zteradb.query import ZTeraDBQuery
from zteradb.query.filter_condition import ZTAND, ZTGT, ZTMUL, ZTICONTAINS

# 1. Build the functional criteria tree
filter_tree = ZTAND([
    ZTGT([ZTMUL(['price', 'quantity']), 500]),
    ZTICONTAINS('name', 'wire')
])

# 2. Load the tree context inside the query execution block
query = (ZTeraDBQuery('product')
    .select()
    .filterCondition(filter_tree))
```

**Compiled Engine Execution Code:**
```sql
SELECT *
FROM product
WHERE (price * quantity) > 500
  AND LOWER(name) LIKE '%wire%';
```

---

## ⚠️ Common Developer Anti-Patterns

* ❌ **Passing Sequential Arguments to Math Blocks:** Writing ZTSUB('price', 'discount') causing argument mismatch errors.
  * Fix: Pass arithmetic operands inside a single parent list: ZTSUB(['price', 'discount']).

* ❌ **Using Math Operators for Structural Filtering Paths:** Utilizing .filter() for complex evaluations instead of simple exact key matching.
  * Fix: Use simple keyword arguments or dictionary structures inside .filter(). Reserve .filter_condition() exclusively for functional expressions and mathematical drivers.

* ❌ **Handling Unoptimized Case Matching Natively:** Manually embedding Python native lowercase operations within execution hooks or loop routines.
  * Fix: Utilize `ZTICONTAINS`, `ZTISTARTSWITH`, and `ZTIENDSWITH` to perform case-insensitive operations inside the storage engine.

---

### 🎉 Next Step
See these filtering rules applied in complex application environments:  
👉 **[Advanced Query Examples](./query-examples.md)**
