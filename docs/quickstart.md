---
sidebar_position: 7
---

# 🚀 Quickstart (10-Minute Beginner Setup)

Welcome to ZTeraDB! This guide is engineered for developers who want to integrate the ZTeraDB Python Client into their applications rapidly using modern asynchronous paradigms. Follow along step-by-step to execute your first database query in under 10 minutes.

## 📌 Table of Contents
* [📋 System Requirements](#system-requirements)
* [📦 1. Installation](#installation)
* [🔐 2. Environment Configuration](#environment-configuration)
* [🔌 3. Establish a Connection Instance](#establish-a-connection-instance)
* [📑 4. Run Your First SELECT Query](#run-your-first-select-query)
* [⚡ 5. Basic CRUD Mutations & Filters](#basic-crud-mutations--filters)
  * [Insert a Record](#insert-a-record)
  * [Update a Record](#update-a-record)
  * [Delete a Record](#delete-a-record)
  * [Simple Scalar Filtering](#simple-scalar-filtering)
  * [Advanced Functional Filtering](#advanced-functional-filtering)
* [🎉 6. Next Steps](#next-steps)

---

## 📋 System Requirements {#system-requirements}

Before installing, ensure your local environment satisfies the runtime prerequisites:

| Requirement | Specification |
| :--- | :--- |
| **Python Version** | Python 3.8 or higher (Download from [python.org](https://www.python.org/downloads/)) |
| **Asynchronous Engine**| Supports native `asyncio` frameworks |
| **Package Registry** | Available via [PyPI](https://pypi.org) |

---


## 📦 1. Installation {#installation}

Integrate the official ZTeraDB package using `pip`. You can install it from the main public registry or target a specific release configuration directly from version control.

### Option 1: Via PyPI (Recommended)

Run the following command in your terminal to install the ZTeraDB client alongside its standard environment variable parsing dependencies:

```sh
pip install zteradb
```

## Option 2: From GitHub Repository
Alternatively, you can pull the package directly from GitHub to target specific active builds or features:

```bash
pip install git+https://github.com/zteradb/zteradb-python.git
```

## 🔐 2. Environment Configuration {#environment-configuration}
Create an isolated environment configuration file named `.env` inside your project's root folder path to safely externalize pipeline security variables.

```bash
# .env
CLIENT_KEY="your_client_identity_string"
ACCESS_KEY="your_active_access_token"
SECRET_KEY="your_cryptographic_signature_key"
DATABASE_ID="your_cluster_instance_id"

ZTERADB_HOST="db1.zteradb.com"
ZTERADB_PORT=7777
ZTERADB_ENV="dev"
REQUEST_DATA_TYPE="json"
```

⚠️ Production Security Watch: Never commit your localized .env variables into public source control networks. Add .env explicitly into your project's .gitignore rules.

---

## 🔌 3. Establish a Connection Instance {#establish-a-connection-instance}
Create a reusable connection gateway file named db.py to initialize and return your storage cluster instance wrapper. This setup configures an internal asynchronous connection pool for managing high-throughput application networking.

```python
import os
from zteradb import ZTeraDBConnectionAsync
from zteradb.config.zteradb_config import ZTeraDBConfig
from zteradb.config.response_data_types import ResponseDataTypes
from zteradb.config.envs import ENVS

def get_db() -> ZTeraDBConnectionAsync:
    """Initializes and returns an asynchronous ZTeraDB Connection pool.
    
    Assumes configuration variables are pre-loaded into the system environment.
    """
    config = ZTeraDBConfig(
        client_key=os.getenv("CLIENT_KEY"),
        access_key=os.getenv("ACCESS_KEY"),
        secret_key=os.getenv("SECRET_KEY"),
        database_id=os.getenv("DATABASE_ID"),
        env=ENVS(os.getenv("ZTERADB_ENV", "dev")),
        response_data_type=os.getenv("REQUEST_DATA_TYPE", "json"),
    )

    host = os.getenv("ZTERADB_HOST", "127.0.0.1")
    port = int(os.getenv("ZTERADB_PORT", "7777"))

    return ZTeraDBConnectionAsync(host, port, config)
```

---

## 📑 4. Run Your First SELECT Query {#run-your-first-select-query}
Create an execution file named test.py to asynchronously fetch table data from your live database node matrix.

```python
# test.py

import asyncio
from db import get_db
from zteradb.query import ZTeraDBQuery

async def main():
    # 1. Establish asynchronous data storage connection engine driver
    db = get_db()

    # 2. Build the query extraction tree
    query = ZTeraDBQuery("user").select()

    # 3. Process execution asynchronously against cluster nodes
    result = await db.run(query)

    # 4. Iterate and clean-print response dictionaries/arrays
    async for user in result:
        print(user)

    # 5. Explicitly terminate pool connection and network handle resources
    await db.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Execute the test runtime sequence inside your CLI environment:

```bash
python test.py
```

🎉 If your routing configurations match your credentials, active user matrices rows will output directly to your terminal screen.

## ⚡ 5. Basic CRUD Mutations & Filters {#basic-crud-mutations--filters}
Below is an onboarding reference containing structured code snippets for typical mutations, conditional writes, and filter configurations utilizing asynchronous processing.

### Insert a Record
```python
query = (
    ZTeraDBQuery("user")
    .insert()
    .fields({
        "email": "test@example.com",
        "password": "secure_hashed_password",
        "status": True
    })
)

result = await db.run(query)
print(f"Generated Auto-Increment ID: {result['last_insert_id']}")
```

### Update a Record
```python
query = (
    ZTeraDBQuery("user")
    .update()
    .fields({"status": False})
    .filter({"id": 1})
)

result = await db.run(query)
```

### Delete a Record
```python
query = (
    ZTeraDBQuery("user")
    .delete()
    .filter({"id": 5})
)

result = await db.run(query)
```

### Simple Scalar Filtering
For straightforward exact-matches on properties, pass static dictionary key-value configurations inside the `.filter()` assignment helper.

```python
query = (
    ZTeraDBQuery("user")
    .select()
    .filter({"status": True})
)
```

### Advanced Functional Filtering
For processing compound mathematical operations or parsing programmatic dynamic validations at the database runtime level, pass your logic tree into `.filter_condition()`.

```python
from zteradb.query.filter_condition import ZTAND, ZTGT, ZTMUL, ZTICONTAINS

# Compiles operational logic evaluating: 
# (price * quantity > 500) AND (product_name case-insensitively contains "premium")
query = (
    ZTeraDBQuery("product")
    .select()
    .filter_condition(
        ZTAND([
            ZTGT([
                ZTMUL(["price", "quantity"]),
                500
            ]),
            ZTICONTAINS(["product_name", "premium"])
        ])
    )
)
```

---

## 🎉 6. Next Steps {#next-steps}

You are officially setup! You have successfully managed your dependency assembly installation layer, connected to database endpoints, managed query statements, and mapped out simple filters.

👉 **Up Next:** If you encounter environment blockades or configuration exceptions, consult the comprehensive **[Troubleshooting Guide](./troubleshooting.md)** blueprint.
