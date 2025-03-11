# -----------------------------------------------------------------------------
# File: zteradb_connection.py
# Description: This file defines the ZTeraDBConnectionManager and ZTeraDBConnection
#              classes, which manage a pool of connections to the TeraDB server.
#              The connection manager ensures that the minimum and maximum connection
#              limits are respected, while also providing methods to create, retrieve,
#              and release connections. The ZTeraDBConnection class acts as a wrapper
#              to interact with the connection manager, enabling the execution of queries
#              asynchronously while managing connection lifecycle.
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

import logging
import asyncio

from .. import zteradb_config
from .zteradb_query import ZTeraDBQuery
from .zteradb_connection_protocol import ZTeraDBClientProtocol
from ..zteradb_exception import AuthenticationFailed

log = logging.getLogger(__name__)


class ZTeraDBConnectionManager:
    """
    This class manages a pool of connections to the TeraDB server. It ensures that the minimum and maximum connection
    limits are respected and provides methods for getting and releasing connections from the pool.

    Attributes:
        zteradb_conf (zteradb_config.ZTeraDBConfig): Configuration object for the TeraDB instance.
        host (str): Hostname or IP address of the TeraDB server.
        port (int): Port number of the TeraDB server.
        min_connections (int): Minimum number of connections to maintain in the pool.
        max_connections (int): Maximum number of connections to maintain in the pool.
        _connections (asyncio.Queue): Queue to manage available connections.

    Methods:
        __init__(zteradb_conf, host, port):
            Initializes the connection manager with configuration and server details.

        _async_init():
            Initializes the pool of minimum connections asynchronously.

        connections():
            Returns the connection queue (getter).

        set_min_max_connections():
            Sets the minimum and maximum connection limits based on configuration.

        get_new_connection():
            Creates and returns a new `ZTeraDBClientProtocol` connection.

        create_min_connections():
            Creates the minimum number of connections and adds them to the pool.

        get_connection():
            Retrieves a connection from the pool, or creates a new one if none are available.

        release_connection(connection):
            Releases a connection back into the pool.

        close():
            Closes all open connections in the pool.
    """

    __slots__ = ("zteradb_conf", "host", "port", "min_connections", "max_connections", "_connections")

    def __init__(self, host, port, zteradb_conf):
        """
        Initializes the ZTeraDBConnectionManager instance with the given configuration,
        host, and port details. Validates the configuration and connection parameters,
        and sets up the connection pool properties like minimum and maximum connections.

        :param host: str - The hostname or IP address of the TeraDB server. This should
                            be a non-empty string.
        :param port: int - The port number to connect to on the TeraDB server. This must
                            be an integer.
        :param zteradb_conf: zteradb_config.ZTeraDBConfig - The configuration object containing TeraDB
                                    settings such as access keys and connection details.
                                    It must be validated before use.

        :raises Exception: If the host is invalid (empty or not a string) or if the port
                           is invalid (not an integer).

        Initializes the following instance variables:
        - `host`: The host address for the TeraDB server.
        - `port`: The port number for the TeraDB server.
        - `zteradb_conf`: The configuration object containing TeraDB settings.
        - `min_connections`: The minimum number of connections to maintain in the connection pool.
        - `max_connections`: The maximum number of connections to allow in the connection pool.
        - `_connections`: An asyncio queue to hold available connections.
        - Calls `set_min_max_connections` to determine the connection pool limits.
        - Initiates asynchronous initialization via `async_init`.

        Example usage:
            zteradb_conf = zteradb_config.ZTeraDBConfig(...)
            connection_manager = ZTeraDBConnectionManager(host="db.zteradb.com", port=7777, zteradb_conf=zteradb_conf)
        """
        # The zteradb_conf object must be an instance of ZTeraDBConfig
        if not isinstance(zteradb_conf, zteradb_config.ZTeraDBConfig):
            raise Exception(f"'zteradb_conf' is not valid ZTeraDBConfig")

        # Validate the TeraDB configuration object to ensure it has correct data
        zteradb_conf.is_valid()

        # Validate that the host parameter is a non-empty string
        if not isinstance(host, str) or not host.strip():
            # Raise exception if host is invalid
            raise Exception("ZTeraDB host is required")

        # Validate that the port is an integer
        if not isinstance(port, int):
            # Raise exception if port is invalid
            raise Exception("ZTeraDB port is required")

        # Assign the provided host and port values to the instance variables
        self.host = host
        self.port = port

        # Assign the configuration object to an instance variable
        self.zteradb_conf = zteradb_conf

        # Initialize min_connections and max_connections to 0 by default
        self.min_connections = 0
        self.max_connections = 0

        # Call the method to set minimum and maximum connections based on the configuration
        self.set_min_max_connections()

        # Create an asyncio Queue to hold the available connections
        self._connections = asyncio.Queue()

        # Start an asynchronous task to initialize the connection pool
        asyncio.ensure_future(self._async_init())

    async def _async_init(self):
        """
        Asynchronously initializes the connection pool by creating the minimum number of connections.

        This method is automatically called when an instance of the ZTeraDBConnectionManager is created.
        It ensures that the minimum number of connections, as defined by the configuration,
        are established and available for use in the connection pool.

        Example usage:
            # When an instance of ZTeraDBConnectionManager is created, this method is called automatically
            connection_manager = ZTeraDBConnectionManager(host="127.0.0.1", port=7777, zteradb_conf=zteradb_config)
            # This automatically triggers _async_init() to initialize the connections
        """
        # Calls the method to create the minimum required connections in the pool
        await self.create_min_connections()

    @property
    def connections(self):
        """
        Returns the connection pool managed by the connection manager.

        This property provides access to the internal queue `_connections` that holds
        the available connections for the connection pool. The queue is used to manage
        connections that are reused for multiple database interactions.

        Accessing this property directly allows the user to interact with the pool of
        active connections in the system.

        Example usage:
            connection_pool = manager.connections
            connection = await connection_pool.get()

        returns:
            asyncio.Queue: The internal connection pool queue containing active connections.
        """
        return self._connections

    def set_min_max_connections(self):
        """
        Sets the minimum and maximum number of connections for the connection pool
        based on the configuration options.

        The method checks if the configuration (`zteradb_conf`) contains valid
        connection pool options and updates the `min_connections` and `max_connections`
        properties accordingly. If the configuration is invalid or missing values,
        it gracefully exits without making changes.

        Example usage:
            self.set_min_max_connections()

        """
        # Check if the configuration has valid connection pool options.
        if not self.zteradb_conf.has_options:
            log.warning("Configuration does not contain valid connection pool options.")
            return

        # Extract connection pool options
        pool_options = self.zteradb_conf.options.connection_pool

        # Set min_connections if defined in the configuration, otherwise retain the default value
        min_conn = pool_options["min"]
        if min_conn:
            self.min_connections = min_conn

        # Set max_connections if defined in the configuration, otherwise retain the default value
        max_conn = pool_options["max"]
        if max_conn:
            self.max_connections = max_conn

    async def get_new_connection(self):
        """
        Establishes and returns a new connection to the TeraDB server.

        This method retrieves the connection credentials from the configuration,
        creates a new instance of `ZTeraDBClientProtocol`, establishes a connection
        asynchronously, and returns the connected instance.

        The method will reuse the credentials from the configuration, which are expected
        to be already set during initialization for efficiency.

        Example usage:
            connection = await self.get_new_connection()

        raises:
            Exception: If there is an issue connecting to the TeraDB server.
        """
        try:
            # Create a new instance of the ZTeraDBClientProtocol using the connection details.
            connection = ZTeraDBClientProtocol(
                host=self.host,
                port=self.port,
                zteradb_conf=self.zteradb_conf
            )

            if not connection:
                raise Exception("An error occurred while connecting to ZTeraDB server.")

            # Establish the connection to the TeraDB server asynchronously.
            await connection.connect()

            # Log the successful connection creation.
            log.info(f"Successfully established connection to {self.host}:{self.port}")

            # Return the connected connection object.
            return connection

        except AuthenticationFailed as e:
            pass

        except Exception as e:
            log.error(f"Failed to establish connection to {self.host}:{self.port}: {e}")
            # raise AuthenticationFailed(f"Unable to create a new connection: {e}")

    async def create_min_connections(self):
        """
        Creates the minimum number of connections as specified in the configuration.

        This method creates `min_connections` number of connections asynchronously
        and adds them to the connection pool. It uses asyncio.gather() to concurrently
        create and add the connections, improving efficiency.

        Example usage:
            await connection_manager.create_min_connections()

        Raises:
            Exception: If there is an issue while creating or adding connections to the pool.
        """
        # Create a list of tasks to create connections concurrently
        tasks = [
            self.get_new_connection()  # Asynchronously create each connection
            for _ in range(self.min_connections)
        ]

        try:
            # Gather all tasks concurrently and await their completion
            connections = await asyncio.gather(*tasks)

            # Add all created connections to the pool asynchronously
            for connection in connections:
                await self.connections.put(connection)

        except Exception as e:
            # Handle any exception during the creation or adding of connections
            log.error(f"Error occurred while creating or adding connections: {e}")
            raise Exception(f"Failed to create minimum connections: {e}")

    async def get_connection(self):
        """
        Retrieves a connection from the pool, or creates a new one if none are available.

        This method attempts to fetch a connection from the connection pool.
        If no connections are available, it will create a new connection and return it.

        Example usage:
            connection = await connection_manager.get_connection()

        Returns:
            ZTeraDBClientProtocol: A connection object that can be used to interact with the TeraDB server.
        """
        if not self.connections.empty():
            # Attempt to get a connection from the pool.
            connection = await self.connections.get()

        else:
            # If the pool is empty, create a new connection.
            connection = await self.get_new_connection()

        return connection

    async def release_connection(self, connection):
        """
        Releases a connection back to the connection pool.

        This method adds the provided connection object back into the connection pool
        (`self._connections`). After using a connection, you should release it back
        to the pool to make it available for reuse by other parts of the application.

        Example usage:
            await connection_manager.release_connection(connection)

        Args:
            connection (ZTeraDBClientProtocol): The connection to be released back
                                                into the connection pool.
        """
        print("Release connection...")
        if connection is None:
            return

        # Put the provided connection back into the connection pool to be reused.
        await self.connections.put(connection)

    async def close(self):
        """
        Closes all connections in the connection pool.

        This method iterates over all the connections in the pool and closes them asynchronously.
        It ensures that all connections are properly closed when no longer needed.

        Example usage:
            await connection_manager.close()
        """
        while not self.connections.empty():
            # Retrieve the next connection from the pool
            connection = await self.connections.get()

            # If the connection exists, close it
            if connection:
                await connection.close()


class ZTeraDBConnectionAsync:
    """
    Manages the connection lifecycle for interacting with a TeraDB instance.

    This class is responsible for establishing and maintaining a connection to
    the TeraDB service, executing queries asynchronously, and properly managing
    connection pooling by utilizing the `ZTeraDBConnectionManager`.

    Attributes:
        connection_manager (ZTeraDBConnectionManager): Manages connection pooling
    """
    __slots__ = ("connection_manager", )

    def __init__(self, host, port, zteradb_conf=None):
        """
        Initializes a ZTeraDBConnection instance with the provided connection details.

        This constructor initializes a `ZTeraDBConnectionManager` to handle the connection
        to the TeraDB instance. If no specific configuration is provided, the default global
        configuration (`zteradb_config.ZTERADB_CONF`) is used.

        :param: host (str): The host address of the TeraDB instance.
        :param: port (int): The port on which the TeraDB instance is listening.
        :param: zteradb_conf (Optional[zteradb_config.ZTeraDBConfig]): The optional configuration for TeraDB connection.
                If not provided, the global `zteradb_config.ZTERADB_CONF` is used.

        :raises:
            ValueError: If the `host` or `port` are not of the correct type.
        """
        # Use the provided configuration or fallback to the default global configuration
        zteradb_conf = zteradb_conf if zteradb_conf else zteradb_config.ZTERADB_CONF

        # Initialize the connection manager with the specified or default configuration
        self.connection_manager = ZTeraDBConnectionManager(
            host=host, port=port, zteradb_conf=zteradb_conf
        )

    async def __aenter__(self):
        """
        Asynchronously enters the context manager. This method is called when the
        `async with` statement is executed. It initializes and prepares the context
        for use, returning an instance of the context manager (typically `self`).

        Returns:
            self: The current instance of the context manager, which is typically
                  used inside the `async with` block.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Asynchronously exits the context manager. This method is called when the
        `async with` block is exited. It handles cleanup tasks, such as closing
        resources, and can manage any exceptions that were raised within the block.

        Args:
            exc_type (type or None): The exception type raised within the `async with` block,
                                      or None if no exception was raised.
            exc_val (Exception or None): The exception instance raised within the block,
                                         or None if no exception was raised.
            exc_tb (traceback or None): The traceback object associated with the exception,
                                        or None if no exception was raised.

        Actions:
            - Calls `self.close()` to clean up and release any resources.
            - If an exception was raised within the block (i.e., `exc_type` is not None),
              it re-raises the exception by raising `exc_val`.

        Note:
            If the exception is re-raised, it will propagate to the calling code.
            If no exception is raised or the exception is handled, the block completes successfully.

        """
        # Cleanup: Close the resources asynchronously.
        await self.close()

        # If an exception was raised inside the 'async with' block
        if exc_type:
            # Re-raise the exception that was caught
            raise exc_val

    async def run(self, query: ZTeraDBQuery, query_timeout=None):
        """
        Executes the provided query against the TeraDB instance asynchronously.

        This method retrieves an available connection from the connection manager, executes
        the provided `ZTeraDBQuery` asynchronously, and yields the result as it is received.
        Once the query execution is complete, the connection is released back to the connection pool.

        :params: query (ZTeraDBQuery): The query to be executed on the TeraDB instance. It must be
                                   an instance of the `ZTeraDBQuery` class, which contains
                                   the SQL query and any necessary parameters.

        :returns: yields:
            Result of the query: The data returned by the query execution. This is yielded
                                 asynchronously as the query is executed.

        :raises:
            ValueError: If there are issues with the query execution.
            ConnectionError: If the connection to the TeraDB instance cannot be established.
        """
        # Retrieve a connection from the connection manager
        connection = await self.connection_manager.get_connection()

        if not connection:
            raise Exception("Connection does not exists. Please check connection.")

        # Execute the query asynchronously and yield the data as it is retrieved
        response = connection.execute_query(query=query, connection_manager=self.connection_manager,
                                            query_timeout=query_timeout)
        if not query.is_select_query:
            response_data = await response.__anext__()
            return response_data

        else:
            return response

    async def close(self):
        """
        Asynchronously closes all active connections managed by the connection manager.

        This method ensures that all connections to the TeraDB instance are properly closed,
        releasing any resources that were being used.

        It calls the `close` method of the `connection_manager` to handle the actual closing
        of connections.
        """
        await self.connection_manager.close()
        return True
