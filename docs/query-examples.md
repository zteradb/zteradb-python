---
sidebar_position: 6
---

# 🍳 Query Cookbook

This reference guide provides production-ready code blocks for standard CRUD operations, complex mathematical evaluations, sorting configurations, and pagination pipelines using the ZTeraDB Query Builder.


## 📌 Table of Contents
* [⚙️ Initial Core Setup](#initial-core-setup)
* [1️⃣ Mutation Operators (INSERT)](#1-mutation-operators-insert)
  * [Insert a Single Record](#insert-a-single-record)
* [2️⃣ Retrieval Operators (SELECT)](#2-retrieval-operators-select)
  * [Select All Table Records](#select-all-table-records)
  * [Select with Basic Scalar Filtering](#select-with-basic-scalar-filtering)
  * [Explicit Column Selection](#explicit-column-selection)
  * [Row Window Offsetting (Pagination Boundary)](#row-window-offsetting-pagination-boundary)
* [3️⃣ Advanced Functional Filters](#3-advanced-functional-filters)
  * [Inline Mathematical Validations](#inline-mathematical-validations)
  * [Case-Insensitive Fuzzy Text Matching](#case-insensitive-fuzzy-text-matching)
* [4️⃣ Update & Delete Mutations](#4-update--delete-mutations)
  * [Conditional Record Updates](#conditional-record-updates)
  * [Target Record Hard Erasures](#target-record-hard-erasures)
* [5️⃣ Relational Join Operations](#5-relational-join-operations)
* [6️⃣ Result Set Modifiers](#6-result-set-modifiers)
  * [Ascending Sorting Sequence](#ascending-sorting-sequence)
  * [Multi-Key Compound Sorting](#multi-key-compound-sorting)
  * [Table Matrix Record Counting](#table-matrix-record-counting)
* [🏆 Unified Master Blueprint Example](#-unified-master-blueprint-example)
* [🎉 Next Steps](#next-steps)

---

## ⚙️ Initial Core Setup {#initial-core-setup}
Every example below assumes an active, pre-configured `ZTeraDBConnectionAsync` lifecycle instance initialized via your global configuration layer using explicit option wrappers and connection pools:

```python
import os
import json
from zteradb import ZTeraDBConnectionAsync
from zteradb.config.zteradb_config import ZTeraDBConfig
from zteradb.config.options import Options
from zteradb.config.connection_pool import ConnectionPool
from zteradb.config.response_data_types import ResponseDataTypes

# Setup advanced configurations and pool sizing
options = Options(
    response_type=ResponseDataTypes.JSON,
    timeout_ms=5000
)

pool_config = ConnectionPool(
    min_size=1,
    max_size=5,
    max_idle_time_ms=30000
)

# Initialize configuration via localized runtime environments
config_raw = json.loads(os.getenv('ZTERADB_CONFIG', '{}'))
config = ZTeraDBConfig(
    config=config_raw,
    options=options,
    pool=pool_config
)

db = ZTeraDBConnectionAsync(
    config=config,
    host=os.getenv('ZTERADB_HOST'),
    port=int(os.getenv('ZTERADB_PORT', 0))
)
```

---

## 1️⃣ Mutation Operators (INSERT) {#1-mutation-operators-insert}
### Insert a Single Record
Builds structured data blocks mapping parameters explicitly to target database storage engines.

```python
from zteradb import ZTeraDBQuery

query = (ZTeraDBQuery('user')
    .insert()
    .fields({
        'email': 'john@example.com',
        'password': 'hashed_pw',
        'status': True
    }))

result = await db.run(query)

print(f"Generated Primary Key ID: {result['last_insert_id']}")
```

**Equivalent SQL**
```sql
INSERT INTO "user" (email, password, status)
VALUES ('john@example.com', 'hashed_pw', TRUE);
```

---

## 2️⃣ Retrieval Operators (SELECT) {#2-retrieval-operators-select}
### Select All Table Records

```python
from zteradb import ZTeraDBQuery

query = ZTeraDBQuery('user').select()
users = await db.run(query)
```

**Equivalent SQL**
```sql
SELECT * FROM "user";
```

### Select with Basic Scalar Filtering
For simple exact-match lookups, pass your payload parameters directly to the `.filter()` helper method.
```python
from zteradb import ZTeraDBQuery

query = (ZTeraDBQuery('user')
    .select()
    .filter({'status': True}))

users = await db.run(query)
```

**Equivalent SQL**
```sql
SELECT * FROM "user" WHERE status = TRUE;
```

### Explicit Column Selection
Reduce wire overhead payloads by picking explicitly specified column dictionaries.

```python
from zteradb import ZTeraDBQuery

query = (ZTeraDBQuery('user')
    .select()
    .fields({'email': 1}))  # Set field map bit-flags to 1 for inclusion-selection

users = await db.run(query)
```

**Equivalent SQL**
```sql
SELECT email FROM "user";
```

### Row Window Offsetting (Pagination Boundary)


```python
from zteradb import ZTeraDBQuery

query = (ZTeraDBQuery('user')
    .select()
    .limit(0, 10))  # API Mapping: limit(offset, count)

users = await db.run(query)
```

**Equivalent SQL**
```sql
SELECT * FROM "user" LIMIT 10 OFFSET 0;
```

---

## 3️⃣ Advanced Functional Filters {#3-advanced-functional-filters}
For complex conditions that extend beyond standard associative key-value loops, inject pre-compiled filter trees directly into `.filter_condition()`.

### Inline Mathematical Validations
```python
from zteradb import ZTeraDBQuery
from zteradb.query.filter_condition import ZTGT, ZTMUL

# Compiles structural calculation boundary rules
condition = ZTGT([
    ZTMUL(['price', 'quantity']),
    500
])

query = (ZTeraDBQuery('product')
    .select()
    .filter_condition(condition))

rows = await db.run(query)
```

**Equivalent SQL**
```sql
SELECT * FROM product WHERE (price * quantity) > 500;
```

### Case-Insensitive Fuzzy Text Matching

```python
from zteradb import ZTeraDBQuery
from zteradb.query.filter_condition import ZTICONTAINS

# Utilizing case-insensitive string matcher helpers
condition = ZTICONTAINS('name', 'john')

query = (ZTeraDBQuery('user')
    .select()
    .filter_condition(condition))

rows = await db.run(query)
```

**Equivalent SQL**
```sql
SELECT * FROM "user" WHERE LOWER(name) LIKE '%john%';
```

---

## 4️⃣ Update & Delete Mutations {#4-update--delete-mutations}
### Conditional Record Updates

```python
from zteradb import ZTeraDBQuery

query = (ZTeraDBQuery('user')
    .update()
    .fields({'status': False})
    .filter({'id': 1}))

result = await db.run(query)

print('Update Success' if result.get('is_updated') else 'No Changes Made')
```

**Equivalent SQL**
```sql
UPDATE "user" SET status = FALSE WHERE id = 1;
```

### Target Record Hard Erasures
```python
from zteradb import ZTeraDBQuery

query = (ZTeraDBQuery('product')
    .delete()
    .filter({'id': 'PRODUCT_ID'}))

result = await db.run(query)
```

**Equivalent SQL**
```sql
DELETE FROM product WHERE id = 'PRODUCT_ID';
```

---

### 5️⃣ Relational Join Operations {#5-relational-join-operations}
Execute structured data links across foreign key references using nested subquery representations via `.related_fields()`.
```python
from zteradb import ZTeraDBQuery

user_filter = (ZTeraDBQuery('user')
    .select()
    .filter({'status': True}))

query = (ZTeraDBQuery('order')
    .select()
    .related_fields({
        'user': user_filter  # Maps target collection bindings implicitly 
    }))

rows = await db.run(query)
```

**Equivalent SQL**
```sql
-- Conceptual Engine Join Mapping
SELECT o.*, u.*
FROM "order" o
JOIN "user" u ON o.user_id = u.id
WHERE u.status = TRUE;
```

---

## 6️⃣ Result Set Modifiers {#6-result-set-modifiers}
### Ascending Sorting Sequence
```python
from zteradb import ZTeraDBQuery

query = (ZTeraDBQuery('product')
    .select()
    .sort({'price': 1}))  # 1 signifies Ascending sorting direction
```

**Equivalent SQL**
```sql
SELECT * FROM product ORDER BY price ASC;
```

### Multi-Key Compound Sorting

```python
from zteradb import ZTeraDBQuery

query = (ZTeraDBQuery('product')
    .select()
    .sort({
        'price': 1,     # Ascending
        'quantity': -1  # -1 signifies Descending sorting direction
    }))
```

**Equivalent SQL**
```sql
SELECT * FROM product ORDER BY price ASC, quantity DESC;
```


### Table Matrix Record Counting
```python
from zteradb import ZTeraDBQuery

query = ZTeraDBQuery('product').count()
result = await db.run(query)

print(f"Active Table Row Count: {result['count']}")
```

**Equivalent SQL**
```sql
SELECT COUNT(*) AS count FROM product;
```
---

## 🏆 Unified Master Blueprint Example
The comprehensive blueprint below combines explicit field lookups, complex mathematical operators, exact-match flags, multi-index sorting arrangements, and strict window pagination limitations into a singular processing chain.
```python
from zteradb import ZTeraDBQuery
from zteradb.query.filter_condition import ZTGT

# 1. Build complex condition logic tree
math_condition = ZTGT(['quantity', 10])

# 2. Aggregate the composite processing sequence
query = (ZTeraDBQuery('product')
    .select()
    .fields({
        'name': 1, 
        'price': 1, 
        'quantity': 1
    })
    .filter_condition(math_condition)
    .filter({'status': 'A'})
    .sort({'price': 1})
    .limit(0, 20))

# 3. Execute query statement via storage connection driver
products = await db.run(query)
```

**Compiled Pipeline Target Output**
```sql
SELECT name, price, quantity
FROM product
WHERE quantity > 10
  AND status = 'A'
ORDER BY price ASC
LIMIT 20 OFFSET 0;
```

---

### 🎉 Next Steps {#next-steps}
* Learn more about complex filter operators inside the **[Filter Conditions Reference](./filter-condition.md)** matrix.
* Need a quick end-to-end framework test configuration? See our structured **[Quick Start Guide](./quickstart.md)** setup path.
