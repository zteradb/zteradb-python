# -----------------------------------------------------------------------------
# File: zteradb_client_protocol.py
# Description: This file defines the ZTeraDBClientProtocol class, which manages
#              the communication protocol between the TeraDB client and server.
#              It includes handling authentication, establishing connections,
#              and executing queries asynchronously. The class inherits from
#              the ZTeraDBTCPProtocol and uses asyncio to handle I/O operations.
#              It also manages server authentication and error handling
#              for interactions with the TeraDB database.
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

import json
import logging
import asyncio
from .zteradb_query import ZTeraDBQuery
from .zteradb_auth import ZTeraDBClientAuth, ZTeraDBServerAuth
from .zteradb_protocol import ZTeraDBTCPProtocol
from . import zteradb_request_types
# from .. import ZTeraDBConfig
from ..zteradb_exception import QueryComplete, NoResponseDataError, AuthenticationFailed, ZTeraBaseError
from ..helper.zteradb_common import ZTeraDBResponseData


log = logging.getLogger(__name__)


class ZTeraDBClientProtocol(ZTeraDBTCPProtocol):
    """
    This class handles the communication protocol for interacting with the TeraDB server. It manages the connection,
    authentication, and query execution, providing methods for connecting to the server and performing actions like
    executing queries.

    Attributes:
        _access_key (str): The access key used for authentication.
        _client_key (str): The client key used for authentication.
        _host (str): The IP address or hostname of the TeraDB server.
        _port (int): The port number to connect to on the TeraDB server.
        _connect_timeout (int): The timeout duration for the connection attempt (in seconds).
        _server_auth (ZTeraDBServerAuth): Stores the server's authentication details after a successful authentication.
        _is_connected (bool): Flag indicating whether the client is connected to the server.
        _lock (asyncio.Lock): A lock to ensure thread safety in concurrent connection operations.

    Methods:
        __init__(host: str, port: int, access_key: str, client_key: str, secret_key: str, connect_timeout: int=0):
            Initializes the protocol instance with the provided connection details and authentication keys.

        connect():
            Establishes a connection to the TeraDB server, authenticates, and sets up the connection.

        execute_query(query: ZTeraDBQuery, timeout=None):
            Executes a query on the TeraDB server and yields the results as they are received.

        parse_query_response_data(response_data):
            Parses the query response data and handles different response scenarios such as errors and query completion.

        get_connection(connection):
            Class method that returns a connected instance of ZTeraDBClientProtocol based on the provided connection details.

        set_server_auth(server_auth: ZTeraDBServerAuth):
            Sets the server's authentication details in the client protocol instance.

        is_valid_server_auth_response(client_auth):
            Validates the server authentication response received from the TeraDB server.

        parse_server_auth_response(response_auth):
            Parses the server authentication response into a ZTeraDBServerAuth object.
    """

    __slots__ = ("zteradb_conf", "_host", "_port", "_is_connected", "_server_auth", "_lock")

    def __init__(self, host: str, port: int, zteradb_conf):
        """
        Initializes the ZTeraDBClientProtocol instance, which is used to manage
        the connection and communication with a TeraDB server.

        This constructor sets up the necessary parameters required for establishing
        a connection to the TeraDB server, including authentication credentials,
        connection details (host, port), and an optional connection timeout.

        :param host: str - The hostname or IP address of the TeraDB server.
            Example: `"db.zteradb.com"` or `"192.168.1.100"`

        :param port: int - The port number on which the TeraDB server is running.
            Example: `7777`

        :param: zteradb_conf:
            :param access_key: str - The access key used for authenticating with the TeraDB server.
                Example: `"4SVOHVT0VO81B9KSUJP8Q4PIFS"`

            :param client_key: str - The client key used for authenticating with the TeraDB server.
                Example: `"2AKOHVT0VO81B9KSUJP8Q5PIKW"`

            :param secret_key: str - The secret key used for authentication with the TeraDB server.
                Example: `"7fbb52c011ecafaa9a1d1b8683dd661cb4143f7f27f86c0303e02880f28fe409c0b4266c012f8edf9ed1b729a6c3d6fa88d8f269d4ad146211708a2cca1a7d9a"`

            :param connect_timeout: int (optional) - The timeout for establishing the connection,
                in seconds. If not provided, defaults to `0`, meaning no timeout is set.
                Example: `30` for a 30-second timeout.

        Attributes:
            - `zteradb_conf`: Stores the zteradb conf provided for authentication.
            - `_secret_key`: Stores the secret key provided for authentication.
            - `_host`: Stores the TeraDB server host.
            - `_port`: Stores the TeraDB server port.
            - `_connect_timeout`: Stores the connection timeout duration (in seconds).
            - `_server_auth`: Stores the server authentication information (initialized as `None`).
            - `_is_connected`: Tracks the connection status (initialized as `True`).
            - `_lock`: A `Lock` object used to manage concurrency during connection operations.

        Example usage:
            # Example of initializing a connection to the TeraDB server
            db_client = ZTeraDBClientProtocol(
                host="localhost",
                port=8080,
                access_key="access_key_123",
                client_key="client_key_abc",
                secret_key="secret_key_xyz",
                connect_timeout=30
            )
        """
        self._host = host
        self._port = port
        self.zteradb_conf = zteradb_conf
        self._server_auth: ZTeraDBServerAuth = None
        self._is_connected = True
        self._lock = asyncio.Lock()

    @property
    def lock(self):
        return self._lock

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def access_key(self):
        return self.zteradb_conf.access_key

    @property
    def client_key(self):
        return self.zteradb_conf.client_key

    @property
    def secret_key(self):
        return self.zteradb_conf.secret_key

    @property
    def server_auth(self):
        return self._server_auth

    @property
    def is_connected(self):
        return self._is_connected

    @property
    def connect_timeout(self):
        return self.zteradb_conf.connect_timeout

    def set_server_auth(self, server_auth: ZTeraDBServerAuth):
        """
        Sets the server authentication object.

        :param server_auth: ZTeraDBServerAuth - The authentication details from the server.
        Example:
            server_auth = ZTeraDBServerAuth(auth_token="xyz", secret_key="abc")
            client.set_server_auth(server_auth)
        """
        self._server_auth = server_auth

    def parse_server_auth_response(self, response_auth):
        """
        Parses the server authentication response and returns a ZTeraDBServerAuth object.

        :param response_auth: dict - The response dictionary containing the authentication data.
        :return: ZTeraDBServerAuth - A server authentication object containing parsed data.
        :raises: AssertionError - If the response is not a dictionary.
        Example:
            response_data = {"data": "xyz", "client_auth": {"token": "abc"}}
            auth_response = client.parse_server_auth_response(response_data)
        """
        assert isinstance(response_auth, dict), "Response auth must be a dictionary."
        response_auth["secret_key"] = self.secret_key
        return ZTeraDBServerAuth(**response_auth)

    def is_valid_server_auth_response(self, client_auth):
        """
        Validates the server authentication response.

        :param client_auth: dict - The client authentication response to verify.
        :return: bool - True if the client authentication is valid, False otherwise.
        :raises: AssertionError - If the client_auth is not a dictionary.
        Example:
            response_data = {"token": "xyz"}
            is_valid = client.is_valid_server_auth_response(response_data)
        """
        assert isinstance(client_auth, dict), "Client auth must be a dictionary."
        client_auth["secret_key"] = self.secret_key
        client_auth = ZTeraDBClientAuth(**client_auth)
        return client_auth.is_valid_request_token

    @is_connected.setter
    def is_connected(self, is_connected):
        self._is_connected = is_connected

    @classmethod
    async def get_connection(cls, connection):
        """
        Establishes and returns a connection to the TeraDB server.

        :param connection: ZTeraDBClientProtocol - Connection details to initialize the connection.
        :return: ZTeraDBClientProtocol - Returns a connected instance of ZTeraDBClientProtocol.
        :raises: Exception - If connection or authentication fails.

        Example:
            connection = await ZTeraDBClientProtocol.get_connection(connection)
        """
        obj = cls(
            host=connection.host, port=connection.port,
            zteradb_conf=connection.zteradb_conf
        )
        obj._reader, obj._writer = await asyncio.open_connection(
            host=connection.host, port=connection.port
        )
        obj.set_server_auth(connection.server_auth)
        obj._is_connected = connection.is_connected
        return obj

    async def connect(self):
        """
        Establishes and returns a connection to the TeraDB server, handling both connection
        and authentication processes.

        This method performs the following tasks:
        1. Establishes a TCP connection with the TeraDB server using the provided host and port.
        2. Creates an authentication request using the `ZTeraDBClientAuth` class.
        3. Sends the authentication request to the server.
        4. Waits for and processes the server's authentication response.
        5. If the authentication is successful, the method sets the server's authentication data
           and updates the connection status.

        If the connection or authentication fails, an exception is raised.

        :return: bool - Returns `True` if the connection and authentication were successful.
            - Example: If successful, the method will return `True` after establishing the connection.

        :raises: Exception - If the connection or authentication fails.
            - Example:
                - If no response is received, an exception with the message `"No response received from TeraDB server."` is raised.
                - If authentication fails, an exception with the message `"Authentication failed: <error details>"` is raised.
                - If connection times out, a `Connection timeout` exception is raised.

        Example usage:
            connection_details = {
                "host": "localhost",
                "port": 8080,
                "access_key": "access_key_123",
                "client_key": "client_key_abc",
                "secret_key": "secret_key_xyz"
            }

            connection = await ZTeraDBClientProtocol.get_connection(connection_details)
            success = await connection.connect()
            print(success)  # Output: True (if the connection and authentication are successful)
        """
        try:
            # Establishing the connection to the ZTeraDB server.
            self._reader, self._writer = await asyncio.open_connection(
                host=self._host, port=self._port
            )

            # Creating an authentication request with provided keys
            auth_manager = ZTeraDBClientAuth(
                access_key=self.access_key, secret_key=self.secret_key, client_key=self.client_key
            )

            # Sending the authentication request to the server
            await self.send(json.dumps(auth_manager.generate_auth_request()))

            # Awaiting the response from the server
            response_data = await asyncio.wait_for(self.read(), timeout=self.connect_timeout) if self.connect_timeout else await self.read()
            await self.read()

            # Checking the response data.
            if response_data:
                # Convert response_data from JSON format
                response_data = response_data.from_json()

                if not isinstance(response_data, dict):
                    raise Exception(f"Invalid response received from ZTeraDB server. data: {response_data}")

                response = ZTeraDBResponseData(**response_data)

                # If no error in response, check server authentication
                if not response.error:
                    if self.is_valid_server_auth_response(response.client_auth):
                        # If authentication is valid, parse the response and update the connection
                        server_auth: ZTeraDBServerAuth = self.parse_server_auth_response(response.data)
                        self.set_server_auth(server_auth)
                        super().__init__(reader=self.reader, writer=self.writer)
                        self._is_connected = True
                        return True

                # Raise exception if authentication fails
                raise AuthenticationFailed(f"Authentication failed: {response.data}")
            else:
                # Raise exception if no response data received
                raise NoResponseDataError("No response received from TeraDB server.")

        except asyncio.TimeoutError:
            # Raise exception if request timeout occurred
            raise ZTeraBaseError("Connection timeout. Please check the server's reachability.")

        except AuthenticationFailed as e:
            pass

        except Exception as e:
            # Raise exception if connection error occurs
            raise ZTeraBaseError(f"Connection error: {str(e)}")

    @classmethod
    def parse_query_response_data(cls, response_data):
        """
        Parses the response data from a query execution and handles errors, completion, or the data itself.

        This method processes the `response_data` received after executing a query on the TeraDB server.
        It performs the following actions:
        1. Converts the `response_data` to JSON if it's not already in JSON format.
        2. Checks for errors in the response and raises an exception if any are found.
        3. If the response indicates that the query is complete, raises a `QueryComplete` exception.
        4. Returns the data if the query is successful and the response contains data.

        :param response_data: The response data from the server after executing a ZTeraDB query.
            The response data is expected to be in the following format:

            {
                "error": boolean,           # Indicates if there was an error in the response
                "response_code": int,       # Numeric response code from the server (e.g., 0 for success)
                "client_auth": dict,        # Client authentication details (e.g., credentials or tokens)
                "data": any                 # The actual data returned by the query, or an error message
            }

            Example response data:
            - Success Response:
              {"error": false, "response_code": 0, "client_auth": {"auth_token": "abc123"}, "data": {"id": 1, "name": "John"}}
            - Error Response:
              {"error": true, "response_code": 1, "client_auth": null, "data": "An error occurred during query execution."}

        :raises: Exception - If the response contains an error.
            - Example: If the `"error"` field is `true`, an exception is raised with the error message in `"data"`.

        :raises: QueryComplete - If the response indicates that the query execution is complete.
            - Example: If the `"response_code"` is `QUERY_COMPLETE` (a constant value representing query completion), it raises the `QueryComplete` exception.

        :raises: NoResponseDataError - If the response contains no data.
            - Example: If the `"data"` field is missing or empty, the method raises the `NoResponseDataError` exception.

        :return: dict - If the query is successful and the response contains data, it returns the `"data"` part of the response.
            - Example: If the response contains `"data": {"id": 1, "name": "John"}`, the method will return `{"id": 1, "name": "John"}`.

        Example usage:

            response_data = {
                "error": false,
                "response_code": 0,
                "client_auth": {"auth_token": "abc123"},
                "data": {"id": 1, "name": "John"}
            }

            try:
                result = ZTeraDBClientProtocol.parse_query_response_data(response_data)
                print(result)  # Output: {"id": 1, "name": "John"}
            except Exception as e:
                print(f"Error: {str(e)}")

        """
        # Check if response_data is valid and contains the required fields
        if response_data:
            # Convert response_data to DICT
            response_data = response_data.from_json()

            if not isinstance(response_data, dict):
                raise ZTeraBaseError(f"Invalid response received from ZTeraDB server. data: {response_data}")

            # Check if the response contains an error
            if response_data["error"]:
                raise ZTeraBaseError(response_data['data'])

            # Check if the response code indicates that the query is complete
            if response_data["response_code"] == zteradb_request_types.ResponseType.QUERY_COMPLETE.value:
                raise QueryComplete("query_completed")

            # If the response contains data, return it
            if response_data["data"]:
                return response_data["data"]

        # If no data is found, raise an exception
        raise NoResponseDataError("no_response_data")

    async def execute_query(self, query: ZTeraDBQuery, connection_manager, query_timeout=None):
        """
        Executes a query on the TeraDB server and processes the results asynchronously.

        This method will:
        - Validate the query type.
        - Ensure the client is connected to the server.
        - Authenticate the connection.
        - Send the query to the server.
        - Process the server's response and yield the result.

        :param query: ZTeraDBQuery - The query object to be executed.
            - Example: `query = ZTeraDBQuery("users").select()`
        :param connection_manager: ZTeraDBConnectionManager - Query Manager object for releasing connection
        :param query_timeout: int (optional) - Timeout for the query execution in seconds. If not provided, no timeout is applied.
            - Example: `timeout = 5` (5 seconds)

        :raises: ValueError - If the provided query is not an instance of ZTeraDBQuery.
            - Example: If you pass a non-`ZTeraDBQuery` object, this will raise a `ValueError`.

        :raises: Exception - If there is an issue with the connection or authentication.

        Example usage:

            # Assuming `client` is an instance of `ZTeraDBClientProtocol`
            async def run_query():
                # Create a new ZTeraDBQuery object
                query = ZTeraDBQuery("users").select()

                # Execute the query with a timeout of 5 seconds
                async for result in client.execute_query(query, timeout=5):
                    print(result)  # Print each result as it is received

            import asyncio
            asyncio.run(run_query())  # Run the query asynchronously
        """
        # Ensure the provided query is an instance of ZTeraDBQuery.
        if not isinstance(query, ZTeraDBQuery):
            # Release the connection to connection manager
            await connection_manager.release_connection(self)
            raise ValueError(f"{query} is not an instance of ZTeraDBQuery")

        # Check if the client is connected to the TeraDB server.
        if not self.is_connected:
            # If not connected, attempt to establish the connection.
            await self.connect()

        # Check if the client is both connected and authenticated with the server.
        if not self.is_connected or not self.server_auth:
            # Release the connection to connection manager
            await connection_manager.release_connection(self)
            raise ZTeraBaseError("Not connected to the server or missing server authentication.")

        # Prepare the request data for the query, which includes:
        #   - The query string generated from the ZTeraDBQuery object.
        #   - The request type set as QUERY.
        #   - The server authentication token for security.
        request_data = {
            "query": query.generate(),  # Generate the query string to be sent to the ZTeraDB server.
            "request_type": zteradb_request_types.RequestType.QUERY.value,  # Set the request type as QUERY.
            "database_id": self.zteradb_conf.database_id,   # Set the database ID
            "env": self.zteradb_conf.env,   # Set the query environment
            **self.server_auth.server_token()   # Add the authentication token from the server.
        }

        # Send the query request to the ZTeraDB server.
        await self.send(json.dumps(request_data))

        # Attempt to parse the initial response data.
        try:
            while True:
                # Wait for the server's response.
                response_data = await asyncio.wait_for(self.read(), timeout=query_timeout) if query_timeout else await self.read()

                # Yield parsed response data.
                yield self.parse_query_response_data(response_data=response_data)

        # Ignore NoResponseDataError, QueryComplete exceptions.
        except (NoResponseDataError, QueryComplete):
            pass

        # Release the connection to connection manager
        await connection_manager.release_connection(self)