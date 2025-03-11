# ZTeraDB Connection

### `ZTeraDBConnectionAsyncAsync(host: string, port: number, zteradb_config: ZTeraDBConfig)`

- **host**: `string`  
  The hostname of the ZTeraDB server instance.  
  **Example**: `"db.zteradb.com"`, `"192.168.1.1"`, `"custom.host.com"`

- **port**: `number`  
  The port number for the ZTeraDB server instance.  
  **Example**: `7777`, `1234`, or any custom port number.

- **zteradb_config**: `ZTeraDBConfig`
  The configuration object for ZTeraDB. [Click here](./config) for more details.

  **Note**:
    - You can set the ZTeraDBConfig object to access globally by using following way. If you set it globally then you will not need to pass the ZTeraDBConfig
      while calling to ZTeraDBConnectionAsync class

    ```python

    from zteradb import zteradb_config

    zteradb_config.ZTERADB_CONFIG = zteradb_config.ZTeraDBConfig(
      ...
    )

    ```

## Overview

This constructor initializes a new `ZTeraDBConnectionAsync` instance by providing the necessary host, port and ZTeraDB configuration.

`ZTeraDBConnectionAsync` is a class that abstracts all the complexities of interacting with a ZTeraDB instance, allowing developers to focus solely on running queries and closing the connection. It includes the following features:

1. **Client Authentication**: Automatically handles secure authentication between the client and the ZTeraDB server using token-based mechanisms.

2. **Connection Management**: Manages individual and pooled connections, including retries, timeouts, and error management, ensuring stable communication without developer intervention.

3. **Request Handling**: Automatically handles sending and receiving data (queries and results) to/from the ZTeraDB server over TCP sockets.

4. **Query Execution**: Developers can execute queries by simply using the `ZTeraDBConnectionAsync.run(ZTeraDBQuery)` method, passing in a `ZTeraDBQuery` object, without needing to manage the connection or buffering.

5. **Error Handling**: Built-in robust error handling with custom exceptions, covering authentication issues and general connection errors, with no need for the developer to manage these errors.

6. **Connection Pooling**: Connection pooling is handled automatically to ensure that the required number of connections are available for requests, without overloading the server.

After initializing the `ZTeraDBConnectionAsync` instance, developers can simply execute queries using the `ZTeraDBConnectionAsync.run(ZTeraDBQuery)` method and close the connection with `ZTeraDBConnectionAsync.close()`.

If the connection is not explicitly closed, it will be automatically terminated when the process initiated by the developer ends.


## Syntax
```python

    # For more details about the configuration,
    # please refer to the `ZTeraDB Configuration` section.
    from zteradb import ZTeraDBConfig, ZTeraDBConnectionAsync

    zteradb_config = ZTeraDBConfig(
      ...
    )

    # Open a connection
    connection = ZTeraDBConnectionAsync(
      host=str,
      port=int,
      zteradb_conf=zteradb_config,
    )

  # Close the connection
  await connection.close()

 ```
or

```python

    # For more details about the configuration,
    # please refer to the `ZTeraDB Configuration` section.
    from zteradb import zteradb_config, ZTeraDBConnectionAsync
  
    zteradb_config.ZTERADB_CONFIG = zteradb_config.ZTeraDBConfig(
        ...
    )

    # Open a connection
    connection = ZTeraDBConnectionAsync( host=str, port=int)

    # Close the connection
    await connection.close()

```

## Methods

---

### `run(query: ZTeraDBQuery)`
 - **Description**: It executes the query on the ZTeraDB database instance and returns an asynchronous generator containing the query results. If an error occurs, it will return the error instead.
 - **Parameters**:
  - **query**: (ZTeraDBQuery) The ZTeraDBQuery instance.
    - **example**: Below query will fetch all records from product schema.
      ```python

        from zteradb import ZTeraDBQuery
      
        query = ZTeraDBQuery("product").select()    # Select all products
      
        # Assuming the connection object exists
        result = connection.run(query)  # The result will be async generator.

      ```
      [Detailed Example](#example)

  - **Returns**: async generator

  - **Throws**:
    - Throws an error if any error occurred while running the query.

### `close()`

- **Description**: It closes all active connections to the ZTeraDB server. If the developer does not explicitly close the connection, it will be automatically terminated when the process initiated by the developer ends.

- **Returns**: (boolean) `true` if the connection is successfully closed; an error if any issue occurs while closing the connection.

- **Throws**:
    - Throws an error if any error occurred while closing the connection.

- **example**: [Click here](#example)


## Example:

Below is end to end example for getting all users from the user schema
```python

import asyncio

# Import required classes and other things
from zteradb import ZTeraDBConfig, ZTeraDBConnectionAsync, ZTeraDBQuery

# Get ZTeraDB Configuration from .env.
ZTERADB_CONFIG = ZTeraDBConfig(
  ...
)

# Establish connection with ZTeraDB server
connection = ZTeraDBConnectionAsync("db1.zteradb.com", 7777, ZTERADB_CONFIG)

async def main():
    # Prepare select query
    query = ZTeraDBQuery("user").select()

    # Run / execute the query
    result = await connection.run(query)

    # Iterate the result
    async for data in result:
      print(data, "data")
    
    # Close the connection
    await connection.close()

asyncio.run(main())
```