# -----------------------------------------------------------------------------
# File: insert-user-profile.py
# Description: This file demonstrates how to asynchronously connect to a ZTeraDB
#              service, insert data into the 'user' and 'user_profile' tables,
#              and print the 'last_insert_id' for each insert operation.
#              The ZTeraDBConnectionAsync class is used for asynchronous database
#              operations, and environment variables are used to configure the
#              database connection.
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


# Insert a new user into the 'user' table
async def insert_user(connection: ZTeraDBConnectionAsync, email: str) -> int:
    user_query = ZTeraDBQuery("user") \
        .insert() \
        .fields(
            email=email,
            password="9b4d99d461723232aff72be0351f114b",
            status=True
        )

    user_result = await connection.run(query=user_query, query_timeout=3)
    return user_result.get("last_insert_id")

# Insert a new user profile into the 'user_profile' table
async def insert_user_profile(connection: ZTeraDBConnectionAsync, user_id: int) -> int:
    user_profile_query = ZTeraDBQuery("user_profile") \
        .insert() \
        .fields(user=user_id, address="a-123, xyz lane, my city, IN", profile_image="/user/xyz.jpg")

    user_profile_result = await connection.run(query=user_profile_query, query_timeout=3)
    return user_profile_result.get("last_insert_id")


async def main(email):
    host, port = get_connection_params()
    zteradb_config = get_zteradb_config()

    # Establish an asynchronous connection to the ZTeraDB server
    async with ZTeraDBConnectionAsync(host=host, port=port, zteradb_conf=zteradb_config) as connection:
        # Insert the user and retrieve the user ID
        user_id = await insert_user(connection=connection, email=email)

        # Insert the user profile and retrieve the profile ID
        user_profile_id = await insert_user_profile(connection=connection, user_id=user_id)

        # Print the inserted user and profile IDs
        print(f"{user_id=}, {user_profile_id=}")


if __name__ == "__main__":
    # Prompt the user for the user's email ID
    email = input("Enter the user's email: ")

    # Insert a user for the email.
    asyncio.run(main(email=email))
