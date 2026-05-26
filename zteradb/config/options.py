from dataclasses import dataclass, field
from typing import Optional, Union, Dict

from .connection_pool import ConnectionPool

@dataclass
class Options:
    """
    A class to define overall options for ZTeraDB, holding the connection pool settings.
    """
    connection_pool: Union[ConnectionPool, Dict[str, int]] = field(
        default_factory=lambda: ConnectionPool()
    )

    def __post_init__(self):
        """
        Normalizes connection_pool input. If a dictionary is provided,
        it automatically unpacks it into a ConnectionPool instance.
        """
        if isinstance(self.connection_pool, dict):
            # Gracefully handle missing keys by falling back to 0 or defaults
            min_val = self.connection_pool.get("min", 0)
            max_val = self.connection_pool.get("max", 0)

            self.connection_pool = ConnectionPool(min=min_val, max=max_val)

    def is_valid(self):
        """Validates components downstream."""
        if self.connection_pool:
            if not isinstance(self.connection_pool, ConnectionPool):
                raise ValueError(
                    "connection_pool must be a valid ConnectionPool instance or matching dictionary structure.")
            self.connection_pool.is_valid()
