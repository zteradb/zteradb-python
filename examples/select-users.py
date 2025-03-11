# -----------------------------------------------------------------------------
# File: select-user-by-email.py
# Description: This script demonstrates how to retrieve user data by email
#              asynchronously from a ZTeraDB database using the ZTeraDBConnectionAsync
#              class. It includes a function to query the database for users
#              matching the provided email and print the result.
#              The script performs the following tasks:
#              - Retrieves the database connection configuration.
#              - Queries the 'user' table to retrieve users by their email address.
#              - Prints out the details of the users matching the provided email.
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
from typing import AsyncIterator

from zteradb import ZTeraDBQuery, ZTeraDBConnectionAsync
from examples.common import get_zteradb_config, get_connection_params

# Function to retrieve users from the 'user' table based on the provided email
async def get_users(connection: ZTeraDBConnectionAsync) -> AsyncIterator[dict]:
    """
    Retrieves users from the 'user' table where the email matches the provided value.

    Args:
        connection (ZTeraDBConnectionAsync): The asynchronous connection to the ZTeraDB server.

    Returns:
        async iterator: An asynchronous iterator of user records that match the email.
    """
    # Define the query to select users from the 'user' table, filtering by email
    user_query = ZTeraDBQuery("user") \
        .select()   # Filter all users

    # Execute the query asynchronously and return the results
    return await connection.run(query=user_query, query_timeout=3)

# Main function to initiate the process and print user details for the provided email
async def main():
    """
    The main function to retrieve and print all users.
    """
    # Get the host and port information from the environment
    host, port = get_connection_params()

    # Get the ZTeraDB configuration
    zteradb_config = get_zteradb_config()

    # Establish an asynchronous connection to the ZTeraDB server
    async with ZTeraDBConnectionAsync(host=host, port=port, zteradb_conf=zteradb_config) as connection:
        # Retrieve users matching the provided email
        users = await get_users(connection)

        # Print each user retrieved from the database
        async for user in users:
            print(user)

# Run the main function asynchronously with the given email
asyncio.run(main())
