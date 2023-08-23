# Ryanair Python
![Testing status](https://github.com/cohaolain/ryanair-py/actions/workflows/python-app.yml/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/cohaolain/ryanair-py/badge.svg?branch=develop)](https://coveralls.io/github/cohaolain/ryanair-py?branch=develop)

This module allows you to retrieve the cheapest flights, with or without return flights, within a fixed set of dates.

This is done directly through Ryanair's API, and does not require an API key.

## Disclaimer
> __DISCLAIMER:__ This library is not affiliated, endorsed, or sponsored by Ryanair or any of its affiliates.  
> All trademarks related to Ryanair and its affiliates are owned by the relevant companies.  
> The author(s) of this library assume no responsibility for any consequences resulting from the use of this library.  
> The author(s) of this library also assume no liability for any damages, losses, or expenses that may arise from the use of this library.  
> Any use of this library is entirely at the user's own risk.  
> It is solely the user's responsibility to ensure compliance with Ryanair's terms of use and any applicable laws 
> and regulations.  
> The library is an independent project aimed at providing a convenient way to interact with the Ryanair API, allowing
> individuals to find flights for personal use, and then ultimately purchase them via Ryanair's website.
> While the author(s) will make efforts to ensure the library's functionality, they do not guarantee the accuracy,
> completeness, or timeliness of the information provided.  
> The author(s) do not guarantee the availability or continuity of the library, and updates may not be guaranteed.  
> Support for this library may be provided at the author(s)'s discretion, but it is not guaranteed.  
> Users are encouraged to report any issues or feedback to the author(s) via appropriate channels.  
> By using this library, users acknowledge that they have read, understood, and agreed to the terms of this disclaimer.

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
# your expectation.
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
