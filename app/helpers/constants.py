from app.models.implementation_type import ImplementationType

# Define all your constants here
DEFAULT_SERVER_HOST = "0.0.0.0"
DEFAULT_SERVER_PORT = 8036
# This will be set from the docker container definition
DEFAULT_CONFIG_PATH = "/usr/src/app/config.json"
CONFIG_PATH_KEY = "CONFIG_PATH"

DEFAULT_CALENDAR_IMPLEMENTATION = ImplementationType.ICALENDAR
