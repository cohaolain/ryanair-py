"""
This module allows you to retrieve the cheapest flights, with/out return flights, within a fixed set of dates.
This is done directly through Ryanair's API, and does not require an API key.
"""

import requests
from datetime import datetime
from time import sleep

from ryanair.types import Flight, Trip

class Ryanair:
    BASE_API_URL = "https://services-api.ryanair.com/"

    REPEAT_WAIT_SECONDS = 10

    def __init__(self, currency):
        def get_flights(airport, date_from, date_to):
            query_url = ''.join((Ryanair.BASE_API_URL,
                                 "farfnd/v4/oneWayFares"))

            params = {
                "departureAirportIataCode": airport,
                "outboundDepartureDateFrom": self._format_date_for_api(date_from),
                "outboundDepartureDateTo": self._format_date_for_api(date_to),
                "currency": self.currency}

            response = _safe_query_fares(query_url, params)

            flights = []
            if response:
                for flight in response:
                    flights.append(_parse_flight(flight['outbound']))

            return flights

        def get_return_flights(source_airport, date_from, date_to,
                               return_date_from, return_date_to):
            query_url = ''.join((Ryanair.BASE_API_URL,
                                 "farfnd/v4/roundTripFares"))

            params = {
                "departureAirportIataCode": source_airport,
                "outboundDepartureDateFrom": self._format_date_for_api(date_from),
                "outboundDepartureDateTo": self._format_date_for_api(date_to),
                "inboundDepartureDateFrom": self._format_date_for_api(return_date_from),
                "inboundDepartureDateTo": self._format_date_for_api(return_date_to),
                "currency": self.currency}

            response = _safe_query_fares(query_url, params)

            trips = []
            for trip in response:
                trips.append(_parse_trip(trip["outbound"], trip["inbound"]))

            return trips

        def _safe_query_fares(url, params, repeating=False):
            self._num_queries += 1

            try:
                response = requests.get(url, params=params)
                response = response.json()['fares']
            except Exception:
                print("ERROR:", url, params, response, "({} queries made so far)".format(self.num_queries))
                if not repeating:
                    print("Repeating after {} seconds".format(Ryanair.REPEAT_WAIT_SECONDS))
                    sleep(Ryanair.REPEAT_WAIT_SECONDS)
                    return _safe_query_fares(url, params, repeating=True)
                return None

            return response

        def _parse_flight(flight):
            return Flight(
                origin=flight['departureAirport']['iataCode'],
                originFull=', '.join((flight['departureAirport']['name'], flight['departureAirport']['countryName'])),
                destination=flight['arrivalAirport']['iataCode'],
                destinationFull=', '.join((flight['arrivalAirport']['name'], flight['arrivalAirport']['countryName'])),
                departureTime=datetime.fromisoformat(flight['departureDate']),
                price=flight['price']['value']
            )

        def _parse_trip(outbound, inbound):
            outbound = _parse_flight(outbound)
            inbound = _parse_flight(inbound)

            return Trip(
                outbound=outbound,
                inbound=inbound,
                totalPrice=inbound.price + outbound.price
            )

        self.currency = currency

        self.get_flights = get_flights
        self.get_return_flights = get_return_flights

        self._num_queries = 0

    @staticmethod
    def _format_date_for_api(date):
        return date if isinstance(date, str) else date.isoformat()

    @property
    def num_queries(self):
        return self._num_queries
