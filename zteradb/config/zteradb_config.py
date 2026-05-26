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
from dataclasses import dataclass
from typing import Optional, Dict, Any, Union
from .response_data_types import ResponseDataTypes
from .envs import ENVS
from .options import Options


@dataclass
class ZTeraDBConfig:
    """
    Configuration class for ZTeraDB client that holds and validates key authentication
    details and optional settings for connecting to the ZTeraDB server.

    Attributes:
        client_key (str): The unique client key to authenticate with the TeraDB server.
        access_key (str): The access key used to access the TeraDB service.
        secret_key (str): The secret key for authentication with the TeraDB service.
        database_id (str): The ID of the database to connect to.
        env (Union[str, ENVS]): The environment instance or its string identifier.
        response_data_type (Union[str, ResponseDataTypes]): Format of the data response.
        connect_timeout (Optional[int]): The timeout duration for connection attempts.
        options (Optional[Options]): Optional configuration for connection pooling.
        use_tls (bool): Flag to determine if connection uses TLS.
        verify_tls_host (bool): Flag to verify hostnames on TLS connections.
    """
    client_key: str
    access_key: str
    secret_key: str
    database_id: str
    env: str or ENVS
    response_data_type: str or ResponseDataTypes
    connect_timeout: Optional[int] = None
    options: Optional[Options] = None
    use_tls: Optional[bool] = False
    verify_tls_host: Optional[bool] = False

    def __post_init__(self):
        """
        Automatically runs right after object instantiation to safely normalize
        and validate configuration parameters.
        """
        self.is_valid()

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
        self._validate_string_keys()
        self._validate_types()
        self._validate_env_key()
        self._validate_response_data_type_key()
        self._validate_options()

    @property
    def has_options(self):
        """
        Property method to check if the `options` attribute is set.

        This property returns the value of the `options` attribute, which may contain additional
        configuration options, such as connection pooling settings. If `options` is `None`,
        the method will return `None`.

        :return: The value of the `options` attribute (could be None if not set).
        """
        return self.options is not None

    def _validate_string_keys(self):
        """Validates critical string attributes to ensure they are non-empty strings."""
        for field_name in ("client_key", "access_key", "secret_key"):
            val = getattr(self, field_name)
            if not isinstance(val, str) or not val.strip():
                raise ValueError(f"'{field_name}' must be a non-empty string.")

    def _validate_types(self):
        """Validates straightforward types and flags."""
        if self.database_id and not isinstance(self.database_id, str):
            raise ValueError(f"database_id must be a string.")

        if self.connect_timeout is not None and not isinstance(self.connect_timeout, int):
            raise ValueError(f"connect_timeout must be an integer.")

        if not isinstance(self.use_tls, bool):
            raise ValueError("use_tls must be a boolean value.")

        if not isinstance(self.verify_tls_host, bool):
            raise ValueError("verify_tls_host must be a boolean value.")

    def _validate_env_key(self):
        """Validates and extracts the environment enum value securely."""
        if isinstance(self.env, ENVS):
            self.env = self.env.value
            return

        try:
            # Check string representation validity
            ENVS(self.env)
        except ValueError:
            valid_envs = ", ".join([e.value for e in ENVS])
            raise ValueError(
                f"'{self.env}' is not a valid environment key. Valid options are: {valid_envs}"
            )

    def _validate_response_data_type_key(self):
        """Validates and extracts the response data type configuration."""
        if isinstance(self.response_data_type, ResponseDataTypes):
            self.response_data_type = self.response_data_type.value
            return

        try:
            ResponseDataTypes(self.response_data_type)
        except ValueError:
            valid_types = ", ".join([r.value for r in ResponseDataTypes])
            raise ValueError(
                f"'{self.response_data_type}' is an invalid response data type. "
                f"Valid choices are: {valid_types}"
            )

    def _validate_options(self):
        """Ensures options object conforms to constraints and delegates internal validation."""
        if self.options:
            if not isinstance(self.options, Options):
                raise ValueError("options must be a valid Options instance.")
            self.options.is_valid()

@dataclass
class ResponseType:
    pass


# Global ZTERADB_CONF. it contains global ZTeraDBConfig object
ZTERADB_CONF: Dict[str, Any] = {}
