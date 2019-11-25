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
    def get_sort_func(
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
        if self.get_sort_func(sort_attr):
            routes.sort(key=self.get_sort_func(sort_attr))
            # Choose the fastest/cheapest/ ...,
            # leave a list for data uniformity
            routes: list = routes[:limit]
        return routes
