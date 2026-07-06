from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ZTeraDBResponseData:
    error: bool
    response_code: int
    data: dict
    client_auth: Optional[dict] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.error, bool):
            raise Exception(f"'{self.error}' is not valid error")

        if not isinstance(self.response_code, int):
            raise Exception(f"'{self.response_code}' is not valid response_code")

        if self.client_auth and not isinstance(self.client_auth, dict):
            raise Exception(f"'{self.client_auth}' is not valid client_auth")

        if not isinstance(self.data, dict):
            raise Exception(f"'{self.data}' is not valid data")
