import enum

class ENVS(enum.Enum):
    """
    Enum class that defines the different environments in which the ZTeraDB client
    can be deployed. This helps to categorize the deployment context and select
    the appropriate configurations for each environment.

    Attributes:
        dev (str): Development environment, typically used for local or in-progress development.
        staging (str): Staging environment, used for testing in a production-like setting.
        qa (str): Quality assurance environment, used for validation and bug-fixing before production.
        prod (str): Production environment, where the system is live and accessible by end-users.
    """
    # Development environment used for local or in-progress development.
    DEV = "dev"

    # Staging environment used for pre-production testing in a production-like setting.
    STAGING = "staging"

    # Quality assurance environment for testing, bug-fixing, and validation before going live.
    QA = "qa"

    # Production environment, where the system is deployed for use by end-users.
    PROD = "prod"

    @classmethod
    def list(cls):
        """
        Returns a list of all environment names defined in the enum.

        This method iterates over the enum and returns the names of all available
        environments as a list of strings.

        Returns:
            List[str]: A list of environment names as strings.
        """
        return [env.name for env in cls]