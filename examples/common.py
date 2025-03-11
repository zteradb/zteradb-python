# -----------------------------------------------------------------------------
# File: common.py
# Description: This file contains helper functions for retrieving environment
#              variables and setting up the ZTeraDB configuration. It provides
#              functions to get connection parameters (host and port) and
#              configure the ZTeraDB connection settings such as client keys,
#              environment, and connection pool options.
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
import os
from zteradb import ZTeraDBConfig, ENVS, Options, ResponseDataTypes


# Retrieve and validate environment variables
def get_connection_params():
    """
    Retrieves the connection parameters (host and port) from environment variables.
    Raises a ValueError if any of the required environment variables are not set.

    Returns:
        tuple: A tuple containing the host and port values for the database connection.
    """
    os.environ.setdefault("ZTERADB_HOST", "localhost")
    os.environ.setdefault("ZTERADB_PORT", "7777")

    # Fetch the host from the environment variables. Default to None if not set.
    host = os.environ.get("ZTERADB_HOST", None)

    # Fetch the port from environment variables and convert to integer. Default to 0 if not set.
    port = int(os.environ.get("ZTERADB_PORT", "0"))

    # Check if either host or port is missing, raise an error if so.
    if not host or not port:
        raise ValueError("ZTERADB_HOST / ZTERADB_PORT are not set in the environment variable")

    # Return the host and port as a tuple
    return host, port


# Set up ZTeraDB configuration
def get_zteradb_config():
    """
    Retrieves the ZTeraDB configuration settings from environment variables and
    constructs a ZTeraDBConfig object. This includes validation for required keys
    such as client, access, and secret keys, as well as database-related settings.

    Returns:
        ZTeraDBConfig: A configured ZTeraDBConfig object with connection and
                       authentication details.

    Raises:
        ValueError: If any required environment variable is missing.
    """
    # Retrieve the required keys and settings from environment variables
    client_key = os.environ.get("ZTERADB_CLIENT_KEY", None)
    access_key = os.environ.get("ZTERADB_ACCESS_KEY", None)
    secret_key = os.environ.get("ZTERADB_SECRET_KEY", None)
    database_id = os.environ.get("ZTERADB_DATABASE_ID", None)

    # Retrieve the environment setting (default to "dev" if not set) and convert it to an enum.
    env = ENVS(os.environ.get("ZTERADB_ENV", "dev"))

    # Retrieve the response data type (default to "json" if not set) and convert it to an enum.
    response_data_type = ResponseDataTypes(os.environ.get("ZTERADB_RESPONSE_TYPE", "json"))

    # Retrieve connection pool settings (min and max connections), defaulting to 0 if not set.
    min_connections = int(os.environ.get("ZTERADB_MIN_CONN", "0"))
    max_connections = int(os.environ.get("ZTERADB_MAX_CONN", "0"))

    # Check if any required authentication variables are missing and raise a ValueError
    if not client_key:
        raise ValueError("ZTERADB_CLIENT_KEY is not set in the environment variable.")

    if not access_key:
        raise ValueError("ZTERADB_ACCESS_KEY is not set in the environment variable.")

    if not secret_key:
        raise ValueError("ZTERADB_SECRET_KEY is not set in the environment variable.")

    if not database_id:
        raise ValueError("ZTERADB_DATABASE_ID is not set in the environment variable.")

    if not env:
        raise ValueError("ZTERADB_ENV is not set in the environment variable.")

    # Create and return the ZTeraDBConfig object with the retrieved environment variables
    return ZTeraDBConfig(
        client_key=client_key,
        access_key=access_key,
        secret_key=secret_key,
        database_id=database_id,
        env=env,
        response_data_type=response_data_type,
        options=Options(connection_pool=dict(min=min_connections, max=max_connections))
    )
