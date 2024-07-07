import logging

from flask import Blueprint, Response, request

from app.config.config import Config
from app.helpers.constants import DEFAULT_CALENDAR_IMPLEMENTATION
from app.models.currencies import Currencies
from app.models.impact_class import ImpactClass
from app.models.implementation_type import ImplementationType
from app.services.ical_service import ICalService

calendar_bp = Blueprint("calendar", __name__)

logger = logging.getLogger(__name__)


def create_route(app, endpoint):
    @app.route(f"/{endpoint}")
    def serve_ical():
        print(f"serve_{endpoint} has been called")  # Debugging line

        # Get filter parameters from query string
        currencies_param = request.args.get("currencies")
        impact_classes_param = request.args.get("impact-classes")
        # Get implementation to use
        implementation_param = request.args.get(
            "implementation", ImplementationType.ICALENDAR.value
        )  # Default to 'icalendar'

        currencies = None
        impact_classes = None

        if currencies_param:
            currencies = [
                Currencies.from_text(currency)
                for currency in currencies_param.split(",")
            ]
        if impact_classes_param:
            impact_classes = [
                ImpactClass.from_text(impact_class)
                for impact_class in impact_classes_param.split(",")
            ]

        # Set filters in config
        config = Config()
        config.set_filters(impact_classes=impact_classes, currencies=currencies)

        # Retrieve data for this endpoint
        data = config.data_repository_service.get_data(endpoint)
        if not data:
            return Response("No events found", status=404)

        # Determine the implementation to use
        try:
            implementation = ImplementationType(implementation_param.lower())
        except ValueError:
            logger.warning(
                "Invalid implementation '%s' provided. Defaulting to '%s'.",
                implementation_param,
                DEFAULT_CALENDAR_IMPLEMENTATION.name,
            )
            implementation = DEFAULT_CALENDAR_IMPLEMENTATION

        # Generate filtered iCal
        calendar = ICalService.generate_ical(data, implementation.value)

        if not calendar:
            return Response("No events found", status=404)

        # Convert calendar to string
        ical_string = calendar.to_string()

        # Serve the iCal file
        return Response(ical_string, mimetype="text/calendar")


def create_routes_from_config(app, config):
    for ep in config.configurations:
        create_route(app, ep.end_point)
