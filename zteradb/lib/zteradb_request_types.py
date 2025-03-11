# -----------------------------------------------------------------------------
# File: zteradb_request_types.py
# Description: This file defines two Enum classes: `RequestType` and `ResponseType`.
#              These Enums represent various request and response types used in
#              communication with the ZTeraDB system. The `RequestType` enum
#              specifies different types of requests that can be made, while the
#              `ResponseType` enum defines the corresponding response types.
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


class RequestType(enum.Enum):
    """
    Enum representing various request types that can be made to the ZTeraDB system.

    Attributes:
        CONNECT: A request to establish a connection.
        DISCONNECT: A request to disconnect from the system.
        QUERY: A request to perform a query operation.
        PING: A request to ping the server for connectivity.
        CREATE_SCHEMA: A request to create a new schema.
        PUBLISH_SCHEMA: A request to publish a schema.
        DATABASE: A request to interact with the database.
        ACTIVE_DATABASE: A request to get the active database.
        SCHEMA: A request related to schemas.
        SCHEMA_FIELDS: A request related to schema fields.
        SCHEMA_RELATED: A request related to schema relationships.
        SCHEMA_ACCESS: A request related to schema access control.
        DATABASE_ACCESS: A request related to database access control.
        ENTERPRISE_USER: A request related to enterprise users.
        ROLE: A request related to roles.
        ACCESS_CONTROL: A request related to access control settings.
        ZTERADB_INSTANCE: A request related to ZTeraDB instances.
        ZTERADB_ENTERPRISE_INSTANCE: A request related to enterprise instances.
        ZTERADB_ENTERPRISE_INSTANCE_GROUP: A request related to enterprise instance groups.
        ENTERPRISE_INSTANCE: A request related to enterprise instances.
        CREDENTIALS: A request related to credentials.
        USER_PROFILE: A request related to user profiles.
        NONE: Represents no specific request type.
    """

    CONNECT = 0x001
    DISCONNECT = 0x003
    QUERY = 0x005
    PING = 0x007
    CREATE_SCHEMA = 0x008
    PUBLISH_SCHEMA = 0x009
    DATABASE = 0x010
    ACTIVE_DATABASE = 0x011
    SCHEMA = 0x012
    SCHEMA_FIELDS = 0x013
    SCHEMA_RELATED = 0x014
    SCHEMA_ACCESS = 0x015
    DATABASE_ACCESS = 0x016
    ENTERPRISE_USER = 0x017
    ROLE = 0x018
    ACCESS_CONTROL = 0x019
    ZTERADB_INSTANCE = 0x020
    ZTERADB_ENTERPRISE_INSTANCE = 0x021
    ZTERADB_ENTERPRISE_INSTANCE_GROUP = 0x022
    ENTERPRISE_INSTANCE = 0x023
    CREDENTIALS = 0x024
    USER_PROFILE = 0X025
    NONE = None

    def get_name(self):
        """
        Returns the name of the request type.
        Example: 'QUERY'

        Returns:
            str: The name of the request type.
        """
        return self.name

    def get_value(self):
        """
        Returns the integer value associated with the request type.
        Example: 0x005 for QUERY

        Returns:
            int: The value of the request type.
        """
        return self.value


class ResponseType(enum.Enum):
    """
    Enum representing various response types that correspond to different requests
    made to the ZTeraDB system.

    Attributes:
        CONNECTED: A response indicating a successful connection.
        CONNECT_ERROR: A response indicating an error in the connection process.
        DISCONNECTED: A response indicating successful disconnection.
        DISCONNECT_ERROR: A response indicating an error in the disconnection process.
        CLIENT_AUTH_ERROR: A response indicating a client authentication error.
        QUERY_DATA: A response containing data from a query.
        QUERY_COMPLETE: A response indicating the completion of a query operation.
        QUERY_ERROR: A response indicating an error during query execution.
        PONG: A response to a ping request, confirming server availability.
        PARSE_QUERY_ERROR: A response indicating a parsing error in the query.
        NO_ACCESS: A response indicating the lack of access to a resource.
        TOKEN_EXPIRED: A response indicating that a token has expired.
        INVALID_SCHEMA: A response indicating an invalid schema was used.
        FIELD_ERROR: A response indicating an error with a field.
        CREATE_SCHEMA_SUCCESS: A response indicating the success of a schema creation.
        CREATE_SCHEMA_ERROR: A response indicating an error during schema creation.
        PUBLISH_SCHEMA_SUCCESS: A response indicating the success of a schema publishing.
        PUBLISH_SCHEMA_ERROR: A response indicating an error during schema publishing.
        NONE: Represents no specific response type.
    """

    CONNECTED = 0x002
    CONNECT_ERROR = 0x500
    DISCONNECTED = 0x004
    DISCONNECT_ERROR = 0x005
    CLIENT_AUTH_ERROR = 0x006
    QUERY_DATA = 0x007
    QUERY_COMPLETE = 0x608
    QUERY_ERROR = 0x09
    PONG = 0x010
    PARSE_QUERY_ERROR = 0x100
    NO_ACCESS = 0x011
    TOKEN_EXPIRED = 0x400
    INVALID_SCHEMA = 0x401
    FIELD_ERROR = 0x402
    CREATE_SCHEMA_SUCCESS = 0x201
    CREATE_SCHEMA_ERROR = 0x501
    PUBLISH_SCHEMA_SUCCESS = 0x202
    PUBLISH_SCHEMA_ERROR = 0x502
    NONE = None

    def get_name(self):
        """
        Returns the name of the response type.
        Example: 'CONNECTED'

        Returns:
            str: The name of the response type.
        """
        return self.name

    def get_value(self):
        """
        Returns the integer value associated with the response type.
        Example: 0x002 for CONNECTED

        Returns:
            int: The value of the response type.
        """
        return self.value
