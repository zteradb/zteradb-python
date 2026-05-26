from dataclasses import dataclass

@dataclass
class ConnectionPool:
    """
    Manages and validates the minimum and maximum connection limits.
    """
    min: int = 0
    max: int = 0

    @property
    def has_min_conn(self) -> bool:
        return self.min is not None

    @property
    def has_max_conn(self) -> bool:
        return self.max is not None

    def set_min_max_connections(self, min_conn, max_conn):
        self.min = min_conn
        self.max = max_conn

    def is_valid(self):
        """Validates connection pool constraints."""
        if not isinstance(self.min, int):
            raise ValueError("min connection must be integer")

        if not isinstance(self.max, int):
            raise ValueError("max connection must be integer")

        if self.min > self.max:
            raise ValueError("min connection must be less than or equal to max connections in the connection_pool")