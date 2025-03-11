# -----------------------------------------------------------------------------
# File: zteradb_data_manager.py
# Description: This file defines the `DataManager` class which provides utilities
#              for managing byte data. The class supports packing, unpacking,
#              encoding, and decoding operations for data manipulation. It also
#              offers methods to convert data to JSON format, decode it, and
#              represent it as a string.
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
import struct


class DataManager:
    """
    DataManager provides utilities to manage byte data, including packing, unpacking,
    encoding/decoding, and JSON conversion. It uses the struct module for packing
    and unpacking binary data. It also offers methods to convert data to JSON format
    and decode it into a string.

    Attributes:
        data (bytes): The byte data that will be managed by this instance.
        struct_fmt (str): The format string used for packing/unpacking the data.
        BUFFER_SIZE (int): The size of the buffer required for the data.
    """
    struct_fmt = "!H"
    BUFFER_SIZE = struct.calcsize(struct_fmt)

    def __init__(self, data: bytes):
        """
        Initializes the DataManager with the provided byte data.

        :param data: The byte data that this instance will manage.
        :type data: bytes
        """
        assert type(data) == bytes
        self.data = data

    def __repr__(self):
        """
        Provides a string representation of the DataManager instance.

        :return: The string representation of the byte data as decoded text.
        :rtype: str
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the string representation of the DataManager instance.

        :return: The decoded string from the byte data.
        :rtype: str
        """
        return self.decode()

    def __call__(self):
        """
        Allows the instance to be called like a function, returning the byte data.

        :return: The raw byte data managed by the instance.
        :rtype: bytes
        """
        return self.data

    def pack(self):
        """
        Packs the byte data into a struct format, prepending the length of the data.

        :return: The packed data as bytes.
        :rtype: bytes
        """
        length = len(self.data)
        return struct.pack(self.struct_fmt, length) + self.data

    @classmethod
    def unpack(cls, data: bytes):
        """
        Unpacks the byte data based on the predefined struct format.

        :param data: The data to unpack.
        :type data: bytes
        :return: A tuple containing the unpacked length of the data.
        :rtype: tuple
        """
        if data:
            return struct.unpack(cls.struct_fmt, data[:cls.BUFFER_SIZE])

    def decode(self):
        """
        Decodes the byte data into a string using the default UTF-8 encoding.

        :return: The decoded string representation of the byte data.
        :rtype: str
        """
        return self.data.decode()

    def from_json(self):
        """
        Decodes the byte data into a JSON object.

        :return: The decoded JSON object from the byte data.
        :rtype: dict
        """
        return json.loads(self.decode())
