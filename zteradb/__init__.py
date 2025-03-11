# -----------------------------------------------------------------------------
# File: __init__.py
# Description: This file contains the asynchronous client logic for interacting
#              with the ZTeraDB service. It handles creating and managing
#              connections to the TeraDB database, executing queries, and
#              processing the results asynchronously.
#
# The file imports several modules that provide various utilities and
# components for filtering query conditions, managing database connections,
# creating and executing queries, and handling configuration settings.
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

# Import the ZTeraDBConnection class from zteradb_connection.py, which is responsible
# for managing the connection to the TeraDB service, including establishing
# and closing connections.
from .lib.zteradb_connection import ZTeraDBConnectionAsync

# Import the ZTeraDBQuery class from lib/zteradb_query.py, which is used
# to construct the ZTeraDB query for running in the TeraDB.
from .lib.zteradb_query import ZTeraDBQuery, Sort

# Import all filter condition functions from the filter_condition_functions module.
# These functions may include various utilities for filtering and processing data
# for querying the TeraDB service.
from .lib.zteradb_filter_condition_functions import *

# Import all the configuration settings and classes from zteradb_config.py.
# This provides access to the configuration needed for interacting with the TeraDB
# service, such as API keys, connection pool options, and environment settings.
from .zteradb_config import *

# Import all classes from the zteradb_exception module, which is used to
# catch appropriate errors coming from zteradb query, connection and server.
from .zteradb_exception import *

__version__ = '1.0.0'
