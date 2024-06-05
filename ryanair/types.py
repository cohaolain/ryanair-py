from collections import namedtuple

Flight = namedtuple("Flight", ("departureTime", "flightNumber", "price", "currency", "origin", "originFull",
                               "destination", "destinationFull"))
Trip = namedtuple("Trip", ("totalPrice", "outbound", "inbound"))
