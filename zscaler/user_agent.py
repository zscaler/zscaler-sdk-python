import platform

from zscaler import __version__ as VERSION


class UserAgent:
    SDK_NAME = "zscaler-sdk-python"
    PYTHON = "python"

    def __init__(self, user_agent_extra=None):
        python_version = platform.python_version()
        os_name = platform.system()
        os_version = platform.release()
        self._user_agent_string = (
            f"{UserAgent.SDK_NAME}/{VERSION} " f"{UserAgent.PYTHON}/{python_version} " f"{os_name}/{os_version}"
        )
        if user_agent_extra:
            self._user_agent_string += f" {user_agent_extra}"

    @property
    def get_user_agent_string(self):
        return self._user_agent_string

    @staticmethod
    def strip_unwanted_parts(user_agent):
        # Extract the part of the User-Agent string within the parentheses
        stripped_string = user_agent.split("(")[1].split(")")[0]

        # Format the stripped string according to the desired format
        final_string = f"({stripped_string})"
        return final_string
