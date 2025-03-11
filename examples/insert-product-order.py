# -----------------------------------------------------------------------------
# File: insert-product-order.py
# Description: This script demonstrates how to insert dummy product and order
#              data asynchronously into a ZTeraDB database using the
#              ZTeraDBConnectionAsync class. It includes functions to insert
#              multiple products and orders, associating them with a user ID.
#              The script performs the following tasks:
#              - Retrieves connection parameters and configuration for ZTeraDB.
#              - Inserts dummy products into the 'product' table.
#              - Inserts dummy orders linked to the products into the 'order' table.
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

import asyncio
from zteradb import ZTeraDBQuery, ZTeraDBConnectionAsync
from examples.common import get_zteradb_config, get_connection_params

# Function to run an insert query asynchronously and return the last inserted ID
async def run_insert_query(connection: ZTeraDBConnectionAsync, query: ZTeraDBQuery):
    """
    Executes an insert query asynchronously and returns the last inserted ID.

    Args:
        connection (ZTeraDBConnectionAsync): The ZTeraDB connection instance.
        query (ZTeraDBQuery): The query object representing the insert statement.

    Returns:
        int: The last inserted ID from the query result.
    """
    # Execute the query and return the last inserted ID from the result
    result = await connection.run(query=query, query_timeout=3)
    return result.get("last_insert_id")

# Function to insert a list of dummy products into the 'product' table
async def insert_dummy_products(connection: ZTeraDBConnectionAsync) -> list:
    """
    Inserts a list of dummy product records into the 'product' table and returns
    the list of inserted product IDs.

    Args:
        connection (ZTeraDBConnectionAsync): The ZTeraDB connection instance.

    Returns:
        list: A list of product IDs inserted into the database.
    """
    # Example product data to insert
    products = [
        dict(name="Wireless Mouse", description="Ergonomic wireless mouse with USB receiver", quantity=120,
             price=1999, create_date="2025-02-01 10:00:00", update_date="2025-02-01 10:00:00", status="A"),
        dict(name="Bluetooth Headphones", description="Noise-canceling over-ear Bluetooth headphones", quantity=50,
             price=5999, create_date="2025-02-02 14:30:00", update_date="2025-02-02 14:30:00", status="A"),
    ]

    # List to store results of product insertions
    product_results = []

    # Loop through each product and insert it into the 'product' table
    for product in products:
        product_query = ZTeraDBQuery("product") \
            .insert() \
            .fields(**product)  # Insert the product fields

        # Add the result of the insert query to the list
        product_results.append(run_insert_query(connection=connection, query=product_query))

    # Use asyncio.gather to execute all insert operations concurrently
    return await asyncio.gather(*product_results)

# Function to insert a list of dummy orders into the 'order' table
async def insert_dummy_orders(connection: ZTeraDBConnectionAsync, user_id: int, product_ids: list[str]) -> list:
    """
    Inserts a list of dummy orders linked to the given user and products into
    the 'order' table. Returns the list of inserted order IDs.

    Args:
        connection (ZTeraDBConnectionAsync): The ZTeraDB connection instance.
        user_id (int): The user ID for whom the orders are being placed.
        product_ids (list[str]): The list of product IDs associated with the orders.

    Returns:
        list: A list of order IDs inserted into the database.
    """
    orders = [
        dict(user_id=user_id, create_date="2025-02-21 10:00:00", update_date="2025-02-21 10:00:00", status="A"),
        dict(user_id=user_id, create_date="2025-02-21 12:00:00", update_date="2025-02-21 12:30:00", status="NA"),
    ]

    # List to store results of order insertions
    order_results = []

    # Loop through each order and insert it into the 'order' table
    for order in orders:
        order_index = orders.index(order)   # Get the index of the current order
        order["product"] = product_ids[order_index] # Assign the corresponding product ID
        order_query = ZTeraDBQuery("order") \
            .insert() \
            .fields(**order)    # Insert the order fields

        # Add the result of the insert query to the list
        order_results.append(run_insert_query(connection=connection, query=order_query))

    # Use asyncio.gather to execute all insert operations concurrently
    return await asyncio.gather(*order_results)

# Main function to execute the entire process of inserting products and orders
async def main(user_id):
    """
    Main function that connects to the ZTeraDB server, inserts dummy products,
    and creates orders linked to the specified user.

    Args:
        user_id (int): The user ID to associate with the orders.
    """
    # Retrieve connection parameters and ZTeraDB configuration
    host, port = get_connection_params()
    zteradb_config = get_zteradb_config()

    # Establish an asynchronous connection to the ZTeraDB server
    async with ZTeraDBConnectionAsync(host=host, port=port, zteradb_conf=zteradb_config) as connection:
        # Insert dummy products and retrieve their IDs
        product_ids = await insert_dummy_products(connection)

        # Insert dummy orders and link them to the product IDs and user ID
        order_ids = await insert_dummy_orders(connection, user_id, product_ids)

        # Print the inserted product and order IDs
        print(f"{product_ids=}, {order_ids=}")


if __name__ == "__main__":
    # Prompt the user for the user ID
    user_id = input("Enter the user ID: ")
    if not user_id.isdigit():
        raise Exception(f"'user_id' must be integer value")

    # Add product and orders for the user
    asyncio.run(main(user_id=int(user_id)))
