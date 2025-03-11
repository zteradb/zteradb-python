# ZTeraDB Python Client library
This is a Python client library for interacting with **ZTeraDB**, a platform that allows you to connect to your 
existing databases and query them using **ZTeraDB Query Language (ZQL)**. The client provides an easy-to-use interface 
to send queries to ZTeraDB and retrieve results in a standardized format.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installing](#install)
4. [Usage](#usage)
5. [Configuration](https://github.com/zteradb/zteradb-python/blob/main/docs/config.md)
6. [ZTeraDB Connection](https://github.com/zteradb/zteradb-python/blob/main/docs/zteradb-connection.md)
7. [Query](https://github.com/zteradb/zteradb-python/blob/main/docs/query.md)
8. [Filter Conditions](https://github.com/zteradb/zteradb-python/blob/main/docs/filter-condition.md)
9. [License](#license)


## **Features**

- **Connect to Multiple Databases**: Seamlessly interact with your existing databases through ZTeraDB.
- **ZTeraDB Query Language (ZQL)**: Use a unified query language to query data across different database systems.
- **Easy Integration**: Easily integrate ZTeraDB into your Node.js application.
- **Asynchronous Queries**: Support for async/await syntax to handle queries and results asynchronously.
- **Error Handling**: Comprehensive error handling to help debug and manage database queries.

## Requirements
- This is a python module available through the PyPI (Python Package Index) registry.
- Before installing, download and [install python](https://www.python.org/downloads/). Python 3.6.0 or higher is required.


## **Install**
Run following command to install ZTeraDB client for python.

```sh

# Using pip
pip install zteradb


# Using conda
conda install zteradb

```

## **Usage**

```python
import os
import asyncio

# Import ZTeraDBConnect, ZTeraDBQuery classes 
from zteradb import ZTeraDBConnectionAsync, ZTeraDBQuery
from zteradb.zteradb_config import ZTeraDBConfig

ZTERADB_CONFIG = ZTeraDBConfig(
    ...
)

# Establish connection with ZTeraDB server
connection = ZTeraDBConnectionAsync("db1.zteradb.com", 7777, ZTERADB_CONFIG)

async def main():
    # Prepare select query
    query = ZTeraDBQuery("user").select()

    # Run the query
    result = await connection.run(query)

    # Iterate the result
    async for row in result:
        print("Query result: ", row)

    # Close the connection
    await connection.close()


asyncio.run(main())

```

## **License**

This project is licensed under the **ZTeraDB** License - see [LICENCE](https://github.com/zteradb/zteradb-python/blob/main/LICENCE) file for details.
