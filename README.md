# Ryanair Python

This module allows you to retrieve either:
1) The cheapest flights, with or without return flights, within a fixed set of dates.
or
2) All available flights between two locations, on a given date

This is done directly through Ryanair's API, and does not require an API key.  
## Installation
Run the following command in the terminal:
```
pip install ryanair-py
```
## Usage
To create an instance:
```python
from ryanair import Ryanair

# You can set a currency at the API instance level, so could also be GBP etc. also.
# Note that this may not *always* be respected by the API, so always check the currency returned matches
# your expectation. For example, the underlying API for get_all_flights does not support this.
api = Ryanair("EUR")
```
### Get the cheapest one-way flights
Get the cheapest flights from a given origin airport (returns at most 1 flight to each destination).
```python
from datetime import datetime, timedelta
from ryanair import Ryanair
from ryanair.types import Flight

api = Ryanair(currency="EUR")  # Euro currency, so could also be GBP etc. also
tomorrow = datetime.today().date() + timedelta(days=1)

flights = api.get_cheapest_flights("DUB", tomorrow, tomorrow + timedelta(days=1))

# Returns a list of Flight namedtuples
flight: Flight = flights[0]
print(flight)  # Flight(departureTime=datetime.datetime(2023, 3, 12, 17, 0), flightNumber='FR9717', price=31.99, currency='EUR' origin='DUB', originFull='Dublin, Ireland', destination='GOA', destinationFull='Genoa, Italy')
print(flight.price)  # 9.78
```
### Get the cheapest return trips (outbound and inbound)
```python
from datetime import datetime, timedelta
from ryanair import Ryanair

api = Ryanair(currency="EUR")  # Euro currency, so could also be GBP etc. also
tomorrow = datetime.today().date() + timedelta(days=1)
tomorrow_1 = tomorrow + timedelta(days=1)

trips = api.get_cheapest_return_flights("DUB", tomorrow, tomorrow, tomorrow_1, tomorrow_1)
print(trips[0])  # Trip(totalPrice=85.31, outbound=Flight(departureTime=datetime.datetime(2023, 3, 12, 7, 30), flightNumber='FR5437', price=49.84, currency='EUR', origin='DUB', originFull='Dublin, Ireland', destination='EMA', destinationFull='East Midlands, United Kingdom'), inbound=Flight(departureTime=datetime.datetime(2023, 3, 13, 7, 45), flightNumber='FR5438', price=35.47, origin='EMA', originFull='East Midlands, United Kingdom', destination='DUB', destinationFull='Dublin, Ireland'))
```

### Get all available flights between two airports
E.g. get all available flights from Dublin to London Gatwick, or London, tomorrow:
```python
from datetime import datetime, timedelta

from ryanair import Ryanair
from tabulate import tabulate

# We don't need to specify a currency if we're only using `get_all_flights`, as this API doesn't support currency 
# conversion. It will always return dares denominated in the currency of the departure country.  
api = Ryanair()
tomorrow = datetime.today().date() + timedelta(days=1)

flights = api.get_all_flights("DUB", tomorrow, "LGW")
print(tabulate(flights, headers="keys", tablefmt="github"))

# We can even expand it to include all vaguely-London airports:
flights = api.get_all_flights("DUB", tomorrow, "LON", destination_is_mac=True)
print(tabulate(flights, headers="keys", tablefmt="github"))
```

This prints the following:

| departureTime       | flightNumber   |   price | currency | origin   | originFull   | destination   | destinationFull   |
|---------------------|----------------|---------|----------|----------|--------------|---------------|-------------------|
| 2023-03-12 06:25:00 | FR 114         |   61.99 | EUR      | DUB      | Dublin       | LGW           | London (Gatwick)  |
| 2023-03-12 09:20:00 | FR 112         |   88.12 | EUR      | DUB      | Dublin       | LGW           | London (Gatwick)  |
| 2023-03-12 11:30:00 | FR 122         |  120.37 | EUR      | DUB      | Dublin       | LGW           | London (Gatwick)  |
| ...                 |                |         | EUR      |          |              |               |                   |


and

| departureTime       | flightNumber   |   price | currency | origin   | originFull   | destination   | destinationFull   |
|---------------------|----------------|---------|----------|----------|--------------|---------------|-------------------|
| 2023-03-12 06:25:00 | FR 114         |   61.99 | EUR      | DUB      | Dublin       | LGW           | LON               |
| 2023-03-12 06:35:00 | FR 202         |   65.09 | EUR      | DUB      | Dublin       | STN           | LON               |
| 2023-03-12 07:10:00 | FR 342         |   65.09 | EUR      | DUB      | Dublin       | LTN           | LON               |
| 2023-03-12 08:20:00 | FR 206         |  102.09 | EUR      | DUB      | Dublin       | STN           | LON               |
| ...                 |                |         |          |          |              |               |                   |


