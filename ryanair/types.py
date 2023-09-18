from dataclasses import dataclass
from datetime import datetime


@dataclass
class Flight:
    departureTime: datetime
    flightNumber: str
    price: float
    currency: str
    origin: str
    originFull: str
    destination: str
    destinationFull: str


@dataclass
class Trip:
    totalPrice: float
    outbound: Flight
    inbound: Flight
