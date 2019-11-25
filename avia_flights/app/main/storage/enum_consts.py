from enum import Enum


class PassengerType(Enum):
    single_adult = "SingleAdult"
    single_child = "SingleChild"
    single_infant = "SingleInfant"


class ChargeTypes(Enum):
    total_amount = "TotalAmount"
    airline_taxes = "AirlineTaxes"
    base_fare = "BaseFare"
