# -----------------------------------------------------------------------------
# File: update-product.py
# Description: This script demonstrates how to update a product in the 'product'
#              table of a ZTeraDB database asynchronously. The script performs the
#              following tasks:
#              - Retrieves connection parameters and configuration for ZTeraDB.
#              - Updates a product's name in the 'product' table where the name matches
#                a given value.
#              - Prints a success or failure message based on whether the product update
#                was successful.
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

# Function to update a product in the 'product' table by name
async def update_product(connection: ZTeraDBConnectionAsync) -> bool:
    """
    Updates the product name in the 'product' table from 'Gaming Keyboard' to
    'Wireless Gaming Keyboard'. Returns True if the update was successful,
    otherwise returns False.

    Args:
        connection (ZTeraDBConnectionAsync): The asynchronous connection to the ZTeraDB server.

    Returns:
        bool: True if the product update was successful, False otherwise.
    """
    # Define the query to update the product name where the current name is 'Gaming Keyboard'
    product_update_query = ZTeraDBQuery("product") \
        .update() \
        .fields(name="Wireless Gaming Keyboard") \
        .filter(name="Gaming Keyboard")

    # Execute the update query asynchronously
    product_update_result = await connection.run(product_update_query)

    # Check if the update was successful by looking at the 'is_updated' key in the result
    return True if product_update_result.get("is_updated") else False

# Main function to run the product update and print the result
async def main():
    # Get connection parameters (host, port) and ZTeraDB configuration
    host, port = get_connection_params()
    zteradb_config = get_zteradb_config()

    # Establish an asynchronous connection to the ZTeraDB server
    async with ZTeraDBConnectionAsync(host=host, port=port, zteradb_conf=zteradb_config) as connection:
        # Attempt to update the product and store whether it was successful
        is_product_updated = await update_product(connection)

        # Print the result based on whether the update was successful
        if is_product_updated:
            print("Product has been updated successfully.")

        else:
            print("Product update failed.")

# Run the main function asynchronously
asyncio.run(main())
