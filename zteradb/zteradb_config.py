# -----------------------------------------------------------------------------
# File: zteradb_config.py
# Description: This file defines configuration and utility classes for ZTeraDB,
#              including environment handling, response data types, connection
#              pool settings, and the main configuration class for ZTeraDB client.
#              It uses enums, dataclasses, and validates configuration options
#              to ensure that the provided settings are correct and usable.
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

import enum
from dataclasses import dataclass, field
from typing import Dict, Optional


class ENVS(enum.Enum):
    """
    Enum class that defines the different environments in which the ZTeraDB client
    can be deployed. This helps to categorize the deployment context and select
    the appropriate configurations for each environment.

    Attributes:
        dev (str): Development environment, typically used for local or in-progress development.
        staging (str): Staging environment, used for testing in a production-like setting.
        qa (str): Quality assurance environment, used for validation and bug-fixing before production.
        prod (str): Production environment, where the system is live and accessible by end-users.
    """
    # Development environment used for local or in-progress development.
    dev = "dev"

    # Staging environment used for pre-production testing in a production-like setting.
    staging = "staging"

    # Quality assurance environment for testing, bug-fixing, and validation before going live.
    qa = "qa"

    # Production environment, where the system is deployed for use by end-users.
    prod = "prod"

    @classmethod
    def list(cls):
        """
        Returns a list of all environment names defined in the enum.

        This method iterates over the enum and returns the names of all available
        environments as a list of strings.

        Returns:
            List[str]: A list of environment names as strings.
        """
        return [env.name for env in cls]


class ResponseDataTypes(enum.Enum):
    """
    Enum class that defines the supported response data formats for the ZTeraDB client.
    Currently, only the JSON format is supported, but this can be extended in the future.

    Attributes:
        json (str): The string value for the JSON response format, which is the default format used by ZTeraDB.
    """
    # JSON format for response data. This is the default format supported by ZTeraDB.
    json: str = "json"

    @classmethod
    def list(cls):
        """
        Returns a list of all the response data types defined in the enum.

        This method iterates over the enum and returns the names of all available response formats
        as a list of strings.

        Returns:
            List[str]: A list of response data format names.
        """
        return [response_data_type.name for response_data_type in cls]


@dataclass
class Options:
    """
    A class to define and validate the connection pool settings for ZTeraDB.
    It manages and validates the minimum and maximum connection limits for the
    connection pool.

    Attributes:
        connection_pool (dict): A dictionary containing 'min' and 'max' keys
                                 for defining the minimum and maximum connection
                                 pool limits.
    """
    connection_pool: Dict[str, int] = field(default_factory=lambda: {"min": 0, "max": 0})

    @property
    def has_min_conn(self):
        """
        Property that checks if the minimum connection limit is defined in the
        connection pool configuration.

        This property evaluates whether the `connection_pool` attribute contains a
        valid "min" key. If the "min" key exists, it returns `True`, otherwise
        returns `False`.

        Returns:
            bool: `True` if the minimum connection limit is not None, `False` otherwise.
        """
        return self.connection_pool and self.connection_pool.get("min", None) is not None

    @property
    def has_max_conn(self):
        """
        Checks whether the 'connection_pool' has a valid 'max' connection value.

        This property returns True if the 'connection_pool' dictionary has the key 'max'
        and its value is not None, indicating that a maximum number of connections is defined.

        :return: bool - Returns True if 'max' is not None in 'connection_pool', else False.
        """
        return self.connection_pool and self.connection_pool.get("max", None) is not None

    def is_valid(self):
        """
        Validates the current configuration.

        This method performs the validation of the connection pool configuration by calling
        the `is_valid_connection_pool` method to ensure that the connection pool settings
        (e.g., min and max connections) are correctly defined.

        :raises ValueError: If the connection pool configuration is invalid (e.g., if
                             min and max connections are not integers or if min exceeds max).
        """
        self.is_valid_connection_pool()

    def is_valid_connection_pool(self):
        """
        Validates the connection pool configuration.

        This method checks if the `connection_pool` attribute is a valid dictionary and ensures that:
        - The `min` and `max` connections are integers.
        - The `min` connections value is less than or equal to the `max` connections value.

        If any of these conditions are not met, a `ValueError` will be raised with an appropriate message.

        :raises ValueError: If the connection pool is not a valid dictionary, or if the
                             `min` or `max` values are not integers, or if `min` exceeds `max`.
        """
        # Check if the connection_pool is a valid dictionary.
        if self.connection_pool and not isinstance(self.connection_pool, dict):
            raise ValueError(f"{self.connection_pool} is not a valid connection_pool")

        # Check if the 'min' connection is an integer.
        min_connection = self.connection_pool.get("min", None)
        if min_connection and not isinstance(min_connection, int):
            raise ValueError("min connection must be integer")

        # Check if the 'max' connection is an integer.
        max_connection = self.connection_pool.get("max", None)
        if max_connection and not isinstance(max_connection, int):
            raise ValueError("max connection must be integer")

        # Check if 'min' connection is less than or equal to 'max' connection.
        if min_connection and max_connection and min_connection > max_connection:
            raise ValueError("min connection must be less than or equal to max connections in the connection_pool")


@dataclass
class ZTeraDBConfig:
    """
    Configuration class for ZTeraDB client that holds and validates key authentication
    details and optional settings for connecting to the TeraDB server.

    Attributes:
        client_key (str): The unique client key to authenticate with the TeraDB server.
        access_key (str): The access key used to access the TeraDB service.
        secret_key (str): The secret key for authentication with the TeraDB service.
        database_id (str): The ID of the database to connect to.
        connect_timeout (int): The timeout duration for the connection attempt
        env (str): The environment in which the TeraDB instance is running (e.g., dev, staging, prod).
        response_data_type (str): The format of the data response from TeraDB (e.g., JSON).
        options (Optional[Options]): Optional configuration for connection pooling and other settings.
    """
    client_key: str
    access_key: str
    secret_key: str
    database_id: str
    env: str or ENVS
    response_data_type: str or ResponseDataTypes
    connect_timeout: Optional[int] = None
    options: Optional[Options] = None

    def is_valid(self):
        """
        Validates the configuration parameters for the ZTeraDBConfig object.

        This method checks the validity of each key used for authentication and
        configuration settings, including:
        - client_key
        - access_key
        - secret_key
        - database_id
        - env
        - response_data_type
        - options

        :raises ValueError: If any of the attributes are invalid, a descriptive error message is raised.
        """
        self.is_valid_client_key()
        self.is_valid_access_key()
        self.is_valid_secret_key()
        self.is_valid_database_id_key()
        self.is_connect_timeout_key()
        self.is_valid_env_key()
        self.is_valid_response_data_type_key()
        self.is_valid_options_type_key()

    @property
    def has_options(self):
        """
        Property method to check if the `options` attribute is set.

        This property returns the value of the `options` attribute, which may contain additional
        configuration options, such as connection pooling settings. If `options` is `None`,
        the method will return `None`.

        :return: The value of the `options` attribute (could be None if not set).
        """
        return self.options

    def is_valid_client_key(self):
        """
        Validates the `client_key` attribute.

        This method checks if the `client_key` is a non-empty string. If the `client_key` is either
        not a string or is an empty string, a `ValueError` is raised, indicating that the client key
        is not valid.

        :raises ValueError: If the `client_key` is not a non-empty string.
        """
        if not isinstance(self.client_key, str) or not self.client_key:
            raise ValueError(f"{self.client_key} is not a valid client_key")

    def is_valid_access_key(self):
        """
        Validates the `access_key` attribute.

        This method checks if the `access_key` is a non-empty string. If the `access_key` is either
        not a string or is an empty string, a `ValueError` is raised, indicating that the access key
        is not valid.

        :raises ValueError: If the `access_key` is not a non-empty string.
        """
        if not isinstance(self.access_key, str) or not self.access_key:
            raise ValueError(f"{self.access_key} is not a valid access_key")

    def is_valid_secret_key(self):
        """
        Validates the `secret_key` attribute.

        This method checks if the `secret_key` is a non-empty string. If the `secret_key` is either
        not a string or is an empty string, a `ValueError` is raised, indicating that the secret key
        is not valid.

        :raises ValueError: If the `secret_key` is not a non-empty string.
        """
        if not isinstance(self.secret_key, str) or not self.secret_key:
            raise ValueError(f"{self.secret_key} is not a valid secret_key")

    def is_valid_database_id_key(self):
        """
        Validates the `database_id` attribute.

        This method checks if the `database_id` is a string. If the `database_id` is provided and
        is not a string, a `ValueError` is raised, indicating that the `database_id` is not valid.

        :raises ValueError: If the `database_id` is provided but not a string.
        """
        if self.database_id and not isinstance(self.database_id, str):
            raise ValueError(f"{self.database_id} is not a valid database_id")

    def is_connect_timeout_key(self):
        """
        Validates the `connect_timeout` attribute.

        This method checks if the `connect_timeout` is a integer. If the `connect_timeout` is provided and
        is not an integer, a `ValueError` is raised, indicating that the `connect_timeout` is not valid.

        :raises ValueError: If the `database_id` is provided but not a string.
        """
        if self.connect_timeout and not isinstance(self.connect_timeout, int):
            raise ValueError(f"{self.connect_timeout} is not a valid connect_timeout")

    def is_valid_env_key(self):
        """
        Validates if the provided environment key (env) is valid by checking if it
        exists in the predefined list of supported environments (ENVS enum).

        Raises:
            ValueError: If the provided environment key is not valid.
        """
        try:
            # If the env is instance of ENVS then extract the env.
            if isinstance(self.env, ENVS):
                self.env = self.env.value

            else:
                # Attempt to match the provided env to a valid ENVS enum value
                ENVS(self.env)

        except ValueError:
            # If the env value is not found in the ENVS enum, raise a ValueError
            raise ValueError(
                f"'{self.env}' is not a valid environment key. Valid options are: {', '.join([e.name for e in ENVS])}")

    def is_valid_response_data_type_key(self):
        """
        Validates the response data type specified in the configuration.

        This method checks if the response data type is present and if it is a valid
        `ResponseDataTypes` enum. If the response data type is not valid, it raises a
        `ValueError`.

        :raises ValueError: If the response data type is invalid.
        """
        if self.response_data_type:
            try:
                # If the response_data_type is instance of ResponseDataTypes then extract the response_data_type.
                if isinstance(self.response_data_type, ResponseDataTypes):
                    self.response_data_type = self.response_data_type.value

                else:
                    # Attempt to match the provided response data type to a valid ResponseDataTypes enum value
                    ResponseDataTypes(self.response_data_type)

            except ValueError:
                raise ValueError(f"Invalid response data type: {self.response_data_type}")

    def is_valid_options_type_key(self):
        """
        Validates the options configuration specified in the ZTeraDBConfig.

        This method checks if the `options` attribute is set and if it is an instance of
        the `Options` class. If the validation fails, a `ValueError` is raised. Additionally,
        it calls the `is_valid()` method of the `Options` instance to ensure the configuration
        is valid.

        :raises ValueError: If `options` is not a valid `Options` instance.
        :raises ValueError: If the `options` instance is invalid based on its own validation.
        """
        if self.options:
            if not isinstance(self.options, Options):
                raise ValueError(f"{self.options} is not a valid Options instance.")

            # Validate the options object itself
            self.options.is_valid()

@dataclass
class ResponseType:
    pass


# Global ZTERADB_CONF. it contains global ZTeraDBConfig object
ZTERADB_CONF = dict()
