import typing
from datetime import (
    datetime,
    timedelta,
)
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .enum_consts import PassengerType


@dataclass_json
@dataclass
class Route:
    """
    Route class.
    Include onward_itinerary, return_itinerary and pricing.
    """
    onward_itinerary: list
    return_itinerary: list
    pricing: dict
    request_datetime: datetime

    def find_source(self, src: str) -> bool:
        """
        Search for departure place.
        """
        return self.onward_itinerary[0].source == src

    def find_destination(self, destination: str) -> bool:
        """
        Search for destination.
        """
        return self.onward_itinerary[-1].destination == destination

    def get_pricing(
        self, passenger_type: PassengerType = PassengerType.single_adult.name
    ) -> typing.Union[int, None]:
        """
        Route cost.
        """
        for key, pricing in self.pricing.items():
            if key == passenger_type:
                return pricing.total_amount
        return None

    def get_flight_time(self) -> timedelta:
        """
        Flight time.
        """
        return (
            self.onward_itinerary[-1].arrival_time_stamp
            - self.onward_itinerary[0].departure_time_stamp
        )

    def __hash__(self):
        self.request_id = None
        return hash(self.to_json())

    def __eq__(self, other):
        self.request_id = None
        other.request_id = None
        return self.to_json() == other.to_json()

    def __ne__(self, other):
        return not self.__eq__(other)


@dataclass_json
@dataclass
class Transplant:
    """
    Route Transplant.
    """
    source: str
    destination: str
    carrier: str
    flight_number: int
    departure_time_stamp: datetime
    arrival_time_stamp: datetime
    class_number: str
    number_of_stops: int
    ticket_type: str
    fare_basis: str
    warning_text: str


@dataclass_json
@dataclass
class Pricing:
    """
    Route cost.
    """
    total_amount: int
    airline_taxes: int
    base_fare: int


@dataclass_json
@dataclass
class RouteStorage:
    """
    Route repository and interface for work with routers.
    """
    routes: typing.List[Route]

    @staticmethod
    def _get_sort_func(
        sort_attr: typing.Optional[str] = None,
    ) -> typing.Callable:
        sort_func = {
            "fastest": lambda i: i.get_flight_time(),
            "slowest": lambda i: -i.get_flight_time(),
            "cheapest": lambda i: i.get_pricing(),
            "expensive": lambda i: -i.get_pricing(),
            'optimal': lambda i: i.get_pricing() * i.get_flight_time()
        }
        return sort_func.get(sort_attr)

    def get_route(
        self,
        source: str,
        destination: str,
        sort_attr: typing.Optional[str] = None,
        limit: int = 1
    ) -> typing.List[Route]:
        """
        Returning the list of routes and the desired sort
        """
        routes = [
            route for route in self.routes
            if route.find_source(source)
            and route.find_destination(destination)
        ]
        if self._get_sort_func(sort_attr):
            routes.sort(key=self._get_sort_func(sort_attr))
            # Choose the fastest/cheapest/ ...,
            # leave a list for data uniformity
            routes: list = routes[:limit]
        return routes

    def get_diff(self) -> set:
        request_routes = dict()

        for route in self.routes:
            request_routes.setdefault(
                route.request_datetime, set()
            ).add(route)

        request_datetimes: typing.List[datetime] = sorted(
            request_routes.keys()
        )
        # Compare the last request with the penultimate one,
        # if there were not 2, but 3 requests, in order to display the changed
        # flights from the last request.
        last_request = request_routes.pop(request_datetimes.pop())
        pre_last_request = request_routes.pop(request_datetimes.pop())
        return last_request.difference(pre_last_request)
