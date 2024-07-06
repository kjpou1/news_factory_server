from dataclasses import dataclass


@dataclass
class CommandLineArgs:
    server: str = "localhost"
    port: int = 8036
    config: str = ""
