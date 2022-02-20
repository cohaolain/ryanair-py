from collections import namedtuple

Flight = namedtuple("Flight", ("departureTime", "price", "origin", "originFull",
                               "destination", "destinationFull"))
Trip = namedtuple("Trip", ("totalPrice", "outbound", "inbound"))
