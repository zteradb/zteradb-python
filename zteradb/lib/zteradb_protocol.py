# -----------------------------------------------------------------------------
# File: zteradb_protocol.py
# Description: This file defines the ZTeraDBTCPProtocol class, which handles
#              TCP communication for the ZTeraDB protocol. It manages reading
#              and writing data asynchronously over a TCP connection, as well as
#              handling authentication, connection state, and closing of the connection.
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
import traceback
from .zteradb_data_manager import DataManager

log = logging.getLogger(__name__)

class ZTeraDBTCPProtocol(asyncio.Protocol):
    """
    A class that implements the ZTeraDB TCP protocol using asyncio. This class manages
    asynchronous TCP communication, including reading and writing data, handling
    authentication, and closing connections.

    Attributes:
        _reader: The reader stream for the connection.
        _writer: The writer stream for the connection.
        _is_authenticated: A flag indicating whether the connection is authenticated.
        _is_connected: A flag indicating whether the connection is active.
        _auth_data: Data used for authentication.
    """

    __slots__ = ("_reader", "_writer", "_is_authenticated", "_is_connected", "_auth_data")

    def __init__(self, reader=None, writer=None):
        """
        Initializes the ZTeraDBTCPProtocol instance with the provided reader and writer.

        :param reader: The reader stream for the connection.
        :param writer: The writer stream for the connection.
        """
        self._reader = reader
        self._writer = writer
        self._is_connected = False
        self._is_authenticated = False
        self._auth_data = None
        super().__init__()

    @property
    def reader(self):
        """
        Returns the reader stream for the connection.
        """
        return self._reader

    @property
    def writer(self):
        """
        Returns the writer stream for the connection.
        """
        return self._writer

    @property
    def is_connected(self):
        """
        Returns whether the connection is active.
        """
        return self._is_connected

    @property
    def auth_data(self):
        """
        Returns the authentication data for the connection.
        """
        return self._auth_data

    def set_auth_data(self, data):
        """
        Sets the authentication data for the connection.

        :param data: The authentication data to set.
        """
        self._auth_data = data

    @property
    def is_authenticated(self):
        """
        Returns whether the connection is authenticated.
        """
        return self._is_authenticated

    def set_is_authenticated(self, is_authenticated):
        """
        Sets the authentication status for the connection.

        :param is_authenticated: A flag indicating whether the connection is authenticated.
        """
        self._is_authenticated = is_authenticated

    async def read(self):
        """
        Reads data from the server.

        This method fetches the header size first, then reads the data based on the header's
        length and returns the decoded data in the form of a DataManager object.

        :return: A DataManager object containing the decoded data or None if an error occurs.
        """
        if not self._is_connected:
            await self.close()
            return None

        try:
            # Read the header (first part of the data)
            data_header = await self.receive_all_data(data_size=DataManager.BUFFER_SIZE)
            if not data_header:
                return

            # Unpack the header to determine the size of the data
            data_len = DataManager.unpack(data_header)[0]

            # Read the actual data based on the size in the header
            data = await self.receive_all_data(data_size=data_len)
            return DataManager(bytes(data))

        except Exception as e:
            log.error("An error occurred while reading data. Error:", exc_info=True)
            await self.close()
            return None


    async def receive_all_data(self, data_size):
        """
        Reads all data from the connection, ensuring that the full data of the requested size
        is received.

        :param data_size: The size of the data to read.
        :return: A bytearray containing the received data.
        """
        buffer = bytearray()
        while len(buffer) < data_size:
            if self._is_connected:
                received_data = await self.reader.readexactly(data_size)
                if not received_data:
                    break
                buffer.extend(received_data)

        return buffer

    async def send(self, data: any):
        """
        Sends data to the server.

        This method packs the data into a DataManager object and sends it over the writer stream.

        :param data: The data to send, which will be encoded and packed.
        :return: None
        """
        if not self._is_connected or not self.writer.transport:
            await self.close()
            raise Exception("Connection is cosed!!!")

        try:
            self.writer.write(DataManager(data.encode()).pack())
            await self.writer.drain()

        except (ConnectionResetError, Exception) as e:
            log.error("An error occurred while sending data", exc_info=True)
            await self.close()

    async def close(self):
        """
        Closes the client connection.

        This method ensures that the connection is properly closed by stopping the writer
        and cleaning up the connection state.

        :return: None
        """
        try:
            if self._is_connected:
                self._is_connected = False
                if self.writer:
                    self.writer.close()
                    await self.writer.wait_closed()

        except (ConnectionResetError, BrokenPipeError) as e:
            log.error(e, exc_info=True)

        finally:
            self._is_connected = False
