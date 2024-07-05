import json
import logging

logger = logging.getLogger(__name__)

class DataRepositoryService:
    def __init__(self, configurations):
        """
        Initialize the DataRepository with the given configurations.

        Parameters:
        configurations (list): List of EventEP configurations.
        """
        self.data = {}
        self.configurations = configurations
        self.load_all_data()

    def load_all_data(self):
        """
        Load data from all files specified in the configurations.
        """
        for config in self.configurations:
            self.load_data_for_file(config.file)

    def load_data_for_file(self, file_path):
        """
        Load data for a specific file and update the data repository.

        Parameters:
        file_path (str): Path to the file to be loaded.
        """
        try:
            with open(file_path, 'r') as f:
                # Find the corresponding endpoint for the file
                endpoint = next((ep.end_point for ep in self.configurations if ep.file == file_path), None)
                if endpoint:
                    self.data[endpoint] = json.load(f)
                    logger.info(f"Loaded data from {file_path} for endpoint {endpoint}")
                else:
                    logger.warning(f"No endpoint found for file {file_path}")
        except Exception as e:
            logger.exception(f"Failed to load data from {file_path}: {e}")

    def get_data(self, endpoint):
        """
        Retrieve data for a specific endpoint.

        Parameters:
        endpoint (str): The endpoint for which to retrieve data.

        Returns:
        dict: The data for the specified endpoint.
        """
        return self.data.get(endpoint)

    def reload_data(self, file_path):
        """
        Reload data for a specific file.

        Parameters:
        file_path (str): Path to the file to be reloaded.
        """
        self.load_data_for_file(file_path)
