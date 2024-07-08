from dataclasses import dataclass


@dataclass
class CommandLineArgs:
    server: str = "0.0.0.0"
    port: int = 8036
    config: str = ""
