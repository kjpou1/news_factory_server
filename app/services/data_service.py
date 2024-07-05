import logging
from app.models.currencies import Currencies
from app.models.impact_class import ImpactClass

class DataService:
    @staticmethod
    def filter_data(data, impact_classes=None, currencies=None):
        """
        Filter the data based on impact classes and then currencies.

        Parameters:
        data (list): The list of events to filter
        impact_classes (list): The list of ImpactClass enums to filter by
        currencies (list): The list of Currencies enums to filter by

        Returns:
        list: The filtered list of events
        """
        if not data:
            logging.warning("No data provided to filter.")
            return []

        # Apply impact classes filter first
        if impact_classes:
            data = [event for event in data if event['impactClass'] in [impact_class.value for impact_class in impact_classes]]

        # Apply currencies filter on the already filtered data
        if currencies:
            data = [event for event in data if event['currency'] in [currency.value for currency in currencies]]

        return data
