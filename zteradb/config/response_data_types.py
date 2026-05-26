import enum


class ResponseDataTypes(enum.Enum):
    """
    Enum class that defines the supported response data formats for the ZTeraDB client.
    Currently, only the JSON format is supported, but this can be extended in the future.

    Attributes:
        json (str): The string value for the JSON response format, which is the default format used by ZTeraDB.
    """
    # JSON format for response data. This is the default format supported by ZTeraDB.
    JSON: str = "json"

    @classmethod
    def list(cls):
        """
        Returns a list of all the response data types defined in the enum.

        This method iterates over the enum and returns the names of all available response formats
        as a list of strings.

        Returns:
            List[str]: A list of response data format names.
        """
        return [response_data_type.name for response_data_type in cls]