import argparse

from app.config.config import Config
from app.helpers.constants import (
    CONFIG_PATH_KEY,
    DEFAULT_CONFIG_PATH,
    DEFAULT_SERVER_HOST,
    DEFAULT_SERVER_PORT,
)
from app.models import CommandLineArgs


class CommandLine:
    @staticmethod
    def parse_arguments() -> CommandLineArgs:
        parser = argparse.ArgumentParser(
            description="Run the application with specified arguments."
        )
        parser.add_argument(
            "--server", "-s", type=str, default=DEFAULT_SERVER_HOST, help="Server host"
        )
        parser.add_argument(
            "--port", "-p", type=int, default=DEFAULT_SERVER_PORT, help="Server port"
        )
        parser.add_argument(
            "--config",
            "-c",
            type=str,
            required=True,
            help="Path to the configuration JSON file",
        )
        args = parser.parse_args()
        ## allow for docker configurations
        args.config = args.config or Config.get(CONFIG_PATH_KEY) or DEFAULT_CONFIG_PATH
        return CommandLineArgs(server=args.server, port=args.port, config=args.config)
