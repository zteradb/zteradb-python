# -----------------------------------------------------------------------------
# File: zteradb_auth.py
# Description: This file contains the classes for handling client and server
#              authentication in the ZTeraDB protocol. It includes functionality
#              for generating authentication tokens, managing credentials, and
#              validating authentication requests.
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

import random
import logging
from hashlib import sha256
from . import zteradb_request_types


log = logging.getLogger(__name__)


class ZTeraDBClientAuth:
    """
    A class that handles client-side authentication logic for ZTeraDB. This includes
    generating authentication tokens, managing access keys, secret keys, and client keys.

    Attributes:
        _access_key (str): Client's access key.
        _secret_key (str): Client's secret key.
        _client_key (str): Client's unique client key.
        _nonce (str): A unique string used in the authentication process.
        _request_token (str): Token used for authenticating requests.
        _request_type (RequestType): Type of the request (e.g., CONNECT).
    """

    __slots__ = ("_access_key", "_secret_key", "_client_key", "_nonce", "_request_token", "_request_type")

    def __init__(self, access_key: str, secret_key: str, client_key: str, nonce: str = "", request_token: str = "",
                 request_type: zteradb_request_types.RequestType = zteradb_request_types.RequestType.NONE):
        """
        Initializes the authentication object with access key, secret key, client key, nonce, and request token.

        :param access_key: Client's access key
        :param secret_key: Client's secret key
        :param client_key: Client's unique client key
        :param nonce: Optional nonce (used in authentication)
        :param request_token: Optional request token (used in authentication)
        :param request_type: Type of request (default: NONE)
        """
        self._access_key: str = access_key
        self._secret_key: str = secret_key
        self._client_key: str = client_key
        self._nonce: str = nonce
        self._request_token: str = request_token
        self._request_type: zteradb_request_types.RequestType = request_type

    def __dict__(self):
        """
        Returns a dictionary representation of the object containing the essential authentication
        information such as the access key, client key, nonce, and request token.

        This method is useful for serializing the object or for returning its core properties in
        a dictionary format. It helps to easily access the authentication details in key-value pairs.

        Example:
            >>> auth = ZTeraDBClientAuth(access_key="accessKey", secret_key="secretKey", client_key="clientKey")
            >>> auth_dict = auth.__dict__()
            >>> print(auth_dict)
            {
                'access_key': 'accessKey',
                'client_key': 'clientKey',
                'nonce': 'f8d35d5a83a02cd125ab32546e85d7e9',
                'request_token': 'b8d8d4e3fd5a2adf067d1e0b70d73f5d8ebf4c3cd7fd9be05c2f11698b4577f1'
            }

        :return: dict: A dictionary representation of the authentication object.
        """
        return dict(
            access_key=self.access_key,
            client_key=self._client_key,
            nonce=self.nonce,
            request_token=self.request_token
        )

    @property
    def nonce(self):
        """
        Returns the nonce (a unique string used in authentication).

        :return: str: The generated nonce.
        """
        return self._nonce

    @property
    def access_key(self):
        """
        Returns the access key (client's access key).

        :return: str: The client's access key.
        """
        return self._access_key

    @property
    def client_key(self):
        """
        Returns the client key (unique identifier for the client).

        :return: str: The client's unique client key.
        """
        return self._client_key

    @property
    def secret_key(self):
        """
        Returns the secret key (client's secret key).

        :return: str: The client's secret key.
        """
        return self._secret_key

    @property
    def request_token(self):
        """
        Returns the request token (used for authenticating requests).

        :return: str: The generated request token.
        """
        return self._request_token

    @property
    def request_type(self):
        """
        Returns the request type (e.g., CONNECT).

        :return: RequestType: The type of request.
        """
        return self._request_type

    @property
    def is_valid_request_token(self):
        """
        This property checks whether the current request token is valid by comparing it
        to a newly generated request token based on the secret key and nonce.

        This is used to verify the authenticity of the authentication request by ensuring
        that the request token matches the expected value. If the tokens match, the
        request is valid, meaning it hasn't been tampered with or forged.

        Example:
            >>> auth = ZTeraDBClientAuth(access_key="accessKey", secret_key="secretKey", client_key="clientKey")
            >>> auth.set_nonce(self.generate_nonce())
            >>> auth.set_request_token(auth.generate_request_token())
            >>> print(auth.is_valid_request_token)  # True because the generated token matches the stored token

            >>> auth.set_request_token(self.generate_request_token())
            >>> print(auth.is_valid_request_token)  # False because the token does not match the generated token

        :return: bool: Returns True if the request token is valid, otherwise False.
        """
        return self.request_token == self.generate_request_token()

    def update_secret_key(self, secret_key=secret_key):
        """
        Updates the secret key for the client.

        :param secret_key: The new secret key.
        """
        self._secret_key = secret_key

    @staticmethod
    def generate_nonce():
        """
        Generate and returns a unique nonce string.

        A nonce is a number used once to prevent replay attacks. It is generated
        by creating a random integer, encoding it, and applying a SHA-256 hash function
        to it, returning the resulting hash as a hexadecimal string.

        Example:
            >>> nonce = ZTeraDBClientAuth.generate_nonce()
            >>> print(nonce)
            'f8eb824f0b62596ac4bbadaeacbfe6c758ad31ac5e8e4304099d3cfd0bc992f9'

        :return: str: A unique nonce string generated by hashing a random integer.
        """
        return sha256(f"{random.randint(10000, 1000000)}".encode()).hexdigest()

    def set_request_token(self, request_token):
        """
        Sets the request token.

        :param request_token: The generated request token.
        """
        self._request_token = request_token

    def set_nonce(self, nonce: str):
        """
        Sets the nonce.

        :param nonce: The nonce to set.
        """
        self._nonce = nonce

    def set_request_type(self, request_type: zteradb_request_types.RequestType):
        """
        Sets the request type (e.g., CONNECT).

        :param request_type: The request type (e.g., CONNECT).
        """
        self._request_type = request_type

    def generate_request_token(self):
        """
        Generate and returns a request token string.

        The request token is a unique token generated by concatenating the secret key
        and the nonce (both encoded as bytes), then applying the SHA-256 hash function
        to the concatenated string, and returning the resulting hash as a hexadecimal string.

        This is used as a unique identifier for a request, ensuring each request has a
        different token, preventing replay attacks.

        Example:
            >>> auth = ZTeraDBClientAuth(access_key="accessKey", secret_key="secretKey", client_key="clientKey")
            >>> auth.set_nonce(auth.generate_nonce())  # Set a nonce
            >>> request_token = auth.generate_request_token()
            >>> print(request_token)
            'b8d8d4e3fd5a2adf067d1e0b70d73f5d8ebf4c3cd7fd9be05c2f11698b4577f1'

        :return: str: A unique request token generated by hashing the concatenation of
                      the secret key and the nonce.
        """
        # Concatenate the secret key and nonce, then encode as bytes
        token_data = f"{self._secret_key}{self.nonce}".encode()

        # Compute the SHA-256 hash of the concatenated data
        # and return the resulting hash as a hexadecimal string
        return sha256(token_data).hexdigest()

    def generate_auth_request(self):
        """
        Generate an authentication request dictionary containing all necessary authentication data.

        This method performs the following steps:
        1. Sets the nonce value using the `generate_nonce` method.
        2. Sets the request token using the `generate_request_token` method.
        3. Sets the request type to `RequestType.CONNECT`, indicating an authentication request.
        4. Returns a dictionary containing the `access_key`, `client_key`, `nonce`, `request_token`,
           and `request_type` values.

        This dictionary is typically used to authenticate the client with the server.

        Example:
            >>> auth = ZTeraDBClientAuth(access_key="accessKey", secret_key="secretKey", client_key="clientKey")
            >>> auth_request = auth.generate_auth_request()
            >>> print(auth_request)
            {
                'access_key': 'accessKey',
                'client_key': 'clientKey',
                'nonce': 'f8d35d5a83a02cd125ab32546e85d7e9',
                'request_token': 'b8d8d4e3fd5a2adf067d1e0b70d73f5d8ebf4c3cd7fd9be05c2f11698b4577f1',
                'request_type': 1
            }

        :return: dict: A dictionary containing authentication request data.
        """
        # Generate and set the nonce
        self.set_nonce(self.generate_nonce())

        # Generate and set the request token
        self.set_request_token(self.generate_request_token())

        # Set the request type to 'CONNECT', indicating an authentication request
        self.set_request_type(zteradb_request_types.RequestType.CONNECT)

        # Return the dictionary with authentication details
        return dict(access_key=self.access_key, client_key=self.client_key, nonce=self.nonce,
                    request_token=self.request_token,
                    request_type=self.request_type.value)


class ZTeraDBServerAuth:
    """
    ZTeraDBServerAuth is a class used for managing server-side authentication
    within the ZTeraDB system. It holds the authentication information such as
    client key, access key, access token, and access token expiration time.

    This class is typically used on the server side to validate requests
    from a client and provide the necessary tokens for authentication purposes.
    It helps maintain the access control between the client and server by managing
    the access tokens.

    Attributes:
        _client_key (str): A unique identifier for the client making the request.
        _access_key (str): The access key associated with the client.
        _access_token (str): The token used to authenticate the client on subsequent requests.
        _access_token_expire (str): The expiration time for the access token.

    Properties:
        client_key (str): Returns the client key.
        access_key (str): Returns the access key.
        access_token (str): Returns the access token.
        access_token_expire (str): Returns the expiration time of the access token.
        is_expired (bool): Returns False if the token is not expired. Placeholder for expiration logic.

    Methods:
        server_token (dict): Returns a dictionary containing the client key and access token.

    Example:
        # Create an instance of ZTeraDBServerAuth with required parameters
        auth_data = {
            "client_key": "client_123",
            "access_key": "access_123",
            "access_token": "token_abc",
            "access_token_expire": "2025-12-31T23:59:59"
        }

        server_auth = ZTeraDBServerAuth(**auth_data)

        # Access client key and access token
        print(server_auth.client_key)  # Output: client_123
        print(server_auth.access_token)  # Output: token_abc

        # Check token expiration (currently returns False as placeholder)
        print(server_auth.is_expired)  # Output: False

        # Retrieve server token as a dictionary
        print(server_auth.server_token())
        # Output: {'client_key': 'client_123', 'access_token': 'token_abc'}
    """
    __slots__ = ("_client_key", "_access_key", "_access_token", "_access_token_expire")

    def __init__(self, **kwargs):
        """
        Initializes a new instance of the ZTeraDBServerAuth class with the given
        parameters. The `kwargs` argument allows flexible assignment of attributes.

        :param kwargs: Dictionary containing the server authentication details.
        Expected keys: 'client_key', 'access_key', 'access_token', 'access_token_expire'.
        """
        self._client_key = kwargs.get("client_key", None)
        self._access_key = kwargs.get("access_key", None)
        self._access_token = kwargs.get("access_token", None)
        self._access_token_expire = kwargs.get("access_token_expire", None)

    @property
    def client_key(self):
        """
        Returns the client key. This is a unique identifier for the client that
        is making the request.

        :return: str: The client key.
        """
        return self._client_key

    @property
    def access_key(self):
        """
        Returns the access key. This is the key used by the client for access
        control and authentication.

        :return: str: The access key.
        """
        return self._access_key

    @property
    def access_token(self):
        """
        Returns the access token. This token is used for authenticating subsequent
        requests from the client.

        :return: str: The access token.
        """
        return self._access_token

    @property
    def access_token_expire(self):
        """
        Returns the expiration time for the access token. This indicates when the
        access token will no longer be valid.

        :return: str: The access token expiration time.
        """
        return self._access_token_expire

    @property
    def is_expired(self):
        """
        Returns the expiration time for the access token. This indicates when the
        access token will no longer be valid.

        :return: str: The access token expiration time.
        """
        # todo: Implement actual expiration check logic (based on current time vs expiration time)
        return False

    def server_token(self):
        """
        Returns a dictionary containing the client key and access token. This is
        useful when sending the server-side authentication token in response
        to client requests.

        :return: dict: A dictionary containing 'client_key' and 'access_token'.
        """
        return dict(client_key=self.client_key, access_token=self.access_token)
