import os
import typing
from datetime import datetime
# Create pool for parse xml(but i don't use, see in CreateStorage.execute())
from multiprocessing import (
    Pool,
    cpu_count,
    Process
)
from itertools import chain

from bs4.element import Tag
from bs4 import (
    BeautifulSoup,
    NavigableString,
)

from app.main.utils.helpers import listdir_full_path
from .enum_consts import (
    PassengerType,
    ChargeTypes,
)
from .structure import (
    Route,
    Transplant,
    Pricing,
    RouteStorage,
)


class CreateStorage:
    """
    Creating a route repository.
    """
    @staticmethod
    def _get_tag_text(tag: typing.Union[Tag, None]) -> typing.Union[int, str]:
        """
        Getting tag text.
        """
        def is_digit(string):
            if string.isdigit():
                return int(string)
            else:
                try:
                    return float(string)
                except ValueError:
                    return string

        text = None
        if tag:
            text = is_digit(tag.get_text())
        return text

    def _create_pricing(
        self, pricing_data: typing.Union[Tag, None]
    ) -> typing.Dict[str, Pricing]:
        """
        Getting route cost.
        """
        pricing = {}
        if pricing_data:
            for passenger_type in [
                PassengerType.single_adult,
                PassengerType.single_child,
                PassengerType.single_infant,
            ]:
                data = {
                    ChargeTypes.total_amount.name: self._get_tag_text(
                        pricing_data.find(
                            "ServiceCharges",
                            {
                                "type": passenger_type.value,
                                "ChargeType": ChargeTypes.total_amount.value,
                            },
                        )
                    ),
                    ChargeTypes.airline_taxes.name: self._get_tag_text(
                        pricing_data.find(
                            "ServiceCharges",
                            {
                                "type": passenger_type.value,
                                "ChargeType": ChargeTypes.airline_taxes.value,
                            },
                        )
                    ),
                    ChargeTypes.base_fare.name: self._get_tag_text(
                        pricing_data.find(
                            "ServiceCharges",
                            {
                                "type": passenger_type.value,
                                "ChargeType": ChargeTypes.base_fare.value,
                            },
                        )
                    ),
                }
                if pricing_data.find(
                    "ServiceCharges", {"type": passenger_type.value, }
                ):
                    pricing[passenger_type.name] = Pricing(**data)
            return pricing

    def __create_flight_data(self, tag: typing.Union[Tag, None]) -> Transplant:
        """
        Create Transplant.
        """
        data = {
            "source": self._get_tag_text(tag.Source),
            "destination": self._get_tag_text(tag.Destination),
            "carrier": self._get_tag_text(tag.Carrier),
            "flight_number": self._get_tag_text(tag.FlightNumber),
            "departure_time_stamp": datetime.strptime(
                self._get_tag_text(tag.DepartureTimeStamp), "%Y-%m-%dT%H%M"
            ),
            "arrival_time_stamp": datetime.strptime(
                self._get_tag_text(tag.ArrivalTimeStamp), "%Y-%m-%dT%H%M"
            ),
            "class_number": self._get_tag_text(tag.Class),
            "number_of_stops": self._get_tag_text(tag.NumberOfStops),
            "ticket_type": self._get_tag_text(tag.TicketType),
            "fare_basis": self._get_tag_text(tag.FareBasis),
            "warning_text": self._get_tag_text(tag.WarningText),
        }
        return Transplant(**data)

    def _create_transplant(
        self, tag: typing.Union[Tag, None]
    ) -> typing.List[Transplant]:
        if tag:
            transplants = []
            for flight in tag.Flights.children:
                if isinstance(flight, NavigableString):
                    continue

                # Add a flight
                transplants.append(self.__create_flight_data(flight))
            return transplants

    def _load_and_create_routes(
        self, xml_data: str,
    ) -> typing.List[Route]:
        """
        Load xml and create routes
        """
        xml = BeautifulSoup(xml_data, "xml")
        all_routes = []

        for route in xml.PricedItineraries.children:
            if isinstance(route, NavigableString):
                continue

            onward_itinerary = self._create_transplant(
                route.find("OnwardPricedItinerary"),
            )

            return_itinerary = self._create_transplant(
                route.find("ReturnPricedItinerary"),
            )
            pricing = self._create_pricing(route.find("Pricing"))
            request_datetime = datetime.strptime(
                xml.AirFareSearchResponse.get('ResponseTime'),
                "%d-%m-%Y %H:%M:%S"
            ),
            all_routes.append(
                Route(
                    onward_itinerary,
                    return_itinerary,
                    pricing,
                    request_datetime
                )
            )
        return all_routes

    def _execute(self, file_path: str) -> typing.List[Route]:
        with open(file_path, "r") as file:
            xml_data = file.read()
        all_routes = self._load_and_create_routes(xml_data)
        return all_routes

    @classmethod
    def execute(cls) -> RouteStorage:
        self = cls()

        xml_files = listdir_full_path(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)) + "/xml_data/"
            )
        )
        # This option does not work with nginx -> upstream -> uwsgi
        # (Decision: use proxy_pass on protocol http in uwsgi or split into
        # separate components.
        # pool = Pool(processes=cpu_count())
        # routes = list(
        #     chain.from_iterable(pool.map(self._execute, xml_files))
        # )
        routes = []
        for xml_path in xml_files:
            routes.extend(self._execute(xml_path))
        return RouteStorage(routes)
