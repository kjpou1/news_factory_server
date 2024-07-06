import logging
import os

from dotenv import load_dotenv

from app.helpers.constants import DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT
from app.helpers.resource_loader import ResourceLoader
from app.models import SingletonMeta
from app.models.event_ep import EventEP

# from app.services.data_repository_service import DataRepositoryService


class Config(metaclass=SingletonMeta):
    _is_initialized = False

    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        if not self._is_initialized:
            self.logger = logging.getLogger(__name__)
            self._server = None
            self._port = None
            self.configurations = []
            self._today_data = None
            self._impact_classes = None
            self._currencies = None
            self.data_repository_service = None  # Initialize DataRepository later
            self._is_initialized = True

    @classmethod
    def initialize(cls):
        cls()

    @staticmethod
    def get(key, default=None):
        return os.getenv(key, default)

    @property
    def server_host(self):
        return (
            self._server
            if self._server
            else self.get("SERVER_HOST", DEFAULT_SERVER_HOST)
        )

    @property
    def server_port(self):
        return (
            self._port
            if self._port
            else int(self.get("SERVER_PORT", DEFAULT_SERVER_PORT))
        )

    @property
    def today_data(self):
        return self._today_data

    @property
    def impact_classes(self):
        return self._impact_classes

    @property
    def currencies(self):
        return self._currencies

    def set_server_host(self, host):
        self._server = host

    def set_server_port(self, port):
        self._port = port

    def load_today_data(self, filename):
        self._today_data = ResourceLoader.load_json_file(filename)
        if self._today_data:
            self.logger.info("Loaded today's data from: %s", filename)
        else:
            self.logger.error("Failed to load today's data from: %s", filename)

    def set_filters(self, impact_classes=None, currencies=None):
        self._impact_classes = impact_classes
        self._currencies = currencies

    def load_config(self, config_path):
        """
        Load configurations from a JSON file.

        Parameters:
        config_path (str): Path to the JSON configuration file
        """
        try:
            data = ResourceLoader.load_json_file(config_path)
            self.configurations = [
                EventEP(**ep) for ep in data.get("configurations", [])
            ]
            self.logger.info("Loaded configuration from %s", config_path)
            # Initialize DataRepositoryService with the loaded configurations
            # self.data_repository_service = {} #DataRepositoryService(self.configurations)
        except Exception as e:
            self.logger.exception(
                "Failed to load configuration file %s: %s", config_path, e
            )
