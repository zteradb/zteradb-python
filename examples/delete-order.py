# -----------------------------------------------------------------------------
# File: delete-order.py
# Description: This script demonstrates how to delete an order from the 'order'
#              table in a ZTeraDB database asynchronously. It retrieves connection
#              parameters and configuration for ZTeraDB, deletes an order based on
#              the product identifier, and prints a success or failure message.
#
# Note: Ensure the 'product_id' is updated with an actual product ID before running.
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

# Function to delete an order from the 'order' table based on a specific product ID.
async def delete_order(connection: ZTeraDBConnectionAsync, product_id: str) -> bool:
    """
    Deletes an order from the 'order' table where the product matches the specified ID.
    Returns True if the delete operation was successful, otherwise returns False.

    Args:
        connection (ZTeraDBConnectionAsync): The asynchronous connection to the ZTeraDB server.
        product_id (str): The product ID used to identify which order to delete.

    Returns:
        bool: True if the order was deleted successfully, False otherwise.
    """
    # Build the query to delete the order associated with the provided product ID
    delete_order_query = ZTeraDBQuery("order") \
        .delete() \
        .filter(product=product_id) # Specify the product ID to filter by

    # Execute the delete query asynchronously and retrieve the result
    delete_order_result = await connection.run(query=delete_order_query, query_timeout=3)

    # Return whether the 'is_deleted' key in the result confirms deletion
    return True if delete_order_result.get("is_deleted") else False

# Main function to execute the delete operation and print the result.
async def main(product_id: str):
    """
    Executes the delete order operation and prints the result.
    Initializes the database connection and deletes the order using the provided product ID.

    Args:
        product_id (str): The product ID of the order to be deleted.
    """
    # Retrieve host and port for the connection
    host, port = get_connection_params()

    # Retrieve the ZTeraDB configuration from environment variables
    zteradb_config = get_zteradb_config()

    # Establish an asynchronous connection to the ZTeraDB server
    async with ZTeraDBConnectionAsync(host=host, port=port, zteradb_conf=zteradb_config) as connection:
        # Attempt to delete the order and capture the result
        is_order_deleted = await delete_order(connection=connection, product_id=product_id)

        # Print whether the delete operation succeeded or failed
        if is_order_deleted:
            print(f"Order for product ID {product_id} has been deleted successfully.")
        else:
            print(f"Failed to delete the order for product ID {product_id}.")

if __name__ == "__main__":
    # Prompt the user for the order's product ID
    product_id = input("Enter the product ID of the order: ")

    # Delete all orders whose product ID is provided
    asyncio.run(main(product_id=product_id))
