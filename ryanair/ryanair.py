"""
This module allows you to retrieve either
1) the cheapest flights, with or without return flights, within a fixed set of dates.
or
2) all available flights between two locations, on a given date
This is done directly through Ryanair's API, and does not require an API key.
"""
import logging
from datetime import datetime, date, time
from typing import Union, Optional

import backoff
import requests
from deprecated import deprecated

from ryanair.types import Flight, Trip

logger = logging.getLogger("ryanair")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s:%(message)s', datefmt="%Y-%m-%d %I:%M:%S")

console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# noinspection PyBroadException
class Ryanair:
    BASE_SERVICES_API_URL = "https://services-api.ryanair.com/farfnd/v4/"
    BASE_AVAILABILITY_API_URL = "https://www.ryanair.com/api/booking/v4/"

    def __init__(self, currency: Optional[str] = None):
        self.currency = currency

        self._num_queries = 0

    def get_cheapest_flights(self, airport: str, date_from: Union[datetime, date, str],
                             date_to: Union[datetime, date, str], destination_country: Optional[str] = None,
                             custom_params: Optional[dict] = None,
                             departure_time_from: Union[str, time] = "00:00",
                             departure_time_to: Union[str, time] = "23:59",
                             max_price: Optional[int] = None,
                             destination_airport: Optional[str] = None
                             ):
        query_url = ''.join((Ryanair.BASE_SERVICES_API_URL,
                             "oneWayFares"))

        params = {
            "departureAirportIataCode": airport,
            "outboundDepartureDateFrom": self._format_date_for_api(date_from),
            "outboundDepartureDateTo": self._format_date_for_api(date_to),
            "outboundDepartureTimeFrom": self._format_time_for_api(departure_time_from),
            "outboundDepartureTimeTo": self._format_time_for_api(departure_time_to)
        }
        if self.currency:
            params['currency'] = self.currency
        if destination_country:
            params['arrivalCountryCode'] = destination_country
        if max_price:
            params['priceValueTo'] = max_price
        if destination_airport:
            params['arrivalAirportIataCode'] = destination_airport
        if custom_params:
            params.update(custom_params)

        try:
            response = self._retryable_query(query_url, params)["fares"]
        except Exception:
            logger.exception(f"Failed to parse response when querying {query_url}")
            return []

        if response:
            return [self._parse_cheapest_flight(flight['outbound']) for flight in response]

        return []

    def get_cheapest_return_flights(self, source_airport: str,
                                    date_from: Union[datetime, date, str],
                                    date_to: Union[datetime, date, str],
                                    return_date_from: Union[datetime, date, str],
                                    return_date_to: Union[datetime, date, str],
                                    destination_country: Optional[str] = None,
                                    custom_params: Optional[dict] = None,
                                    outbound_departure_time_from: Union[str, time] = "00:00",
                                    outbound_departure_time_to: Union[str, time] = "23:59",
                                    inbound_departure_time_from: Union[str, time] = "00:00",
                                    inbound_departure_time_to: Union[str, time] = "23:59",
                                    max_price: Optional[int] = None,
                                    destination_airport: Optional[str] = None
                                    ):
        query_url = ''.join((Ryanair.BASE_SERVICES_API_URL,
                             "roundTripFares"))

        params = {
            "departureAirportIataCode": source_airport,
            "outboundDepartureDateFrom": self._format_date_for_api(date_from),
            "outboundDepartureDateTo": self._format_date_for_api(date_to),
            "inboundDepartureDateFrom": self._format_date_for_api(return_date_from),
            "inboundDepartureDateTo": self._format_date_for_api(return_date_to),
            "currency": self.currency,
            "outboundDepartureTimeFrom": self._format_time_for_api(outbound_departure_time_from),
            "outboundDepartureTimeTo": self._format_time_for_api(outbound_departure_time_to),
            "inboundDepartureTimeFrom": self._format_time_for_api(inbound_departure_time_from),
            "inboundDepartureTimeTo": self._format_time_for_api(inbound_departure_time_to)
        }
        if destination_country:
            params['arrivalCountryCode'] = destination_country
        if max_price:
            params['priceValueTo'] = max_price
        if destination_airport:
            params['arrivalAirportIataCode'] = destination_airport
        if custom_params:
            params.update(custom_params)

        try:
            response = self._retryable_query(query_url, params)["fares"]
        except Exception as e:
            logger.exception(f"Failed to parse response when querying {query_url}")
            return []

        if response:
            return [self._parse_cheapest_return_flights_as_trip(trip["outbound"], trip["inbound"])
                    for trip in response]
        else:
            return []

    def get_all_flights(self, origin_airport: str, date_out: Union[datetime, date, str], destination: str,
                        locale: str = "en-ie", origin_is_mac: bool = False, destination_is_mac: bool = False,
                        custom_params: Optional[dict] = None):
        query_url = ''.join((Ryanair.BASE_AVAILABILITY_API_URL, f"{locale}/availability"))

        params = {
            # Assume single adult ticket only
            "ADT": 1,
            "TEEN": 0,
            "CHD": 0,
            "INF": 0,

            "DateOut": self._format_date_for_api(date_out),
            "DateIn": "",

            "Origin": origin_airport,
            "Destination": destination,
            "OriginIsMac": origin_is_mac,
            "DestinationIsMac": destination_is_mac,

            "IncludeConnectingFlights": False,  # What? You do that?
            "ToUs": "AGREED",

            # Presently unused, but these and others can be set by custom_params

            # "Disc": 0,
            # "promoCode": "",
            # "FlexDaysBeforeOut": 2,
            # "FlexDaysOut": 2,
            # "FlexDaysBeforeIn": 2,
            # "FlexDaysIn": 2,
            # "RoundTrip": false,
        }

        if custom_params:
            params.update(custom_params)

        try:
            response = self._retryable_query(query_url, params)
            currency = response["currency"]
            trip = response["trips"][0]
            flights = trip['dates'][0]['flights']
            if flights:
                if self.currency and self.currency != currency:
                    logger.warning(f"Configured to fetch fares in {self.currency} but availability API doesn't support"
                                   f" specifying the currency, so it responded with fares in {currency}")

                return [self._parse_all_flights_availability_result_as_flight(flight,
                                                                              trip['originName'],
                                                                              trip['destinationName'],
                                                                              currency)
                        for flight in flights]
        except Exception:
            logger.exception(f"Failed to parse response when querying {query_url} with parameters {params}")
            return []

    @staticmethod
    def _on_query_error(e):
        logger.exception(f"Gave up retrying query, last exception was {e}")

    @backoff.on_exception(backoff.expo, Exception, max_tries=5, logger=logger, on_giveup=_on_query_error,
                          raise_on_giveup=False)
    def _retryable_query(self, url, params):
        self._num_queries += 1

        return requests.get(url, params=params).json()

    def _parse_cheapest_flight(self, flight):
        currency = flight['price']['currencyCode']
        if self.currency and self.currency != currency:
            logger.warning(f"Requested cheapest flights in {self.currency} but API responded with fares in {currency}")
        return Flight(
            origin=flight['departureAirport']['iataCode'],
            originFull=', '.join((flight['departureAirport']['name'], flight['departureAirport']['countryName'])),
            destination=flight['arrivalAirport']['iataCode'],
            destinationFull=', '.join((flight['arrivalAirport']['name'], flight['arrivalAirport']['countryName'])),
            departureTime=datetime.fromisoformat(flight['departureDate']),
            flightNumber=f"{flight['flightNumber'][:2]} {flight['flightNumber'][2:]}",
            price=flight['price']['value'],
            currency=currency
        )

    def _parse_cheapest_return_flights_as_trip(self, outbound, inbound):
        outbound = self._parse_cheapest_flight(outbound)
        inbound = self._parse_cheapest_flight(inbound)

        return Trip(
            outbound=outbound,
            inbound=inbound,
            totalPrice=inbound.price + outbound.price
        )

    @staticmethod
    def _parse_all_flights_availability_result_as_flight(response, origin_full, destination_full, currency):
        return Flight(departureTime=datetime.fromisoformat(response['time'][0]),
                      flightNumber=response['flightNumber'],
                      price=response['regularFare']['fares'][0]['amount'] if response['faresLeft'] != 0 else float(
                          'inf'),
                      currency=currency,
                      origin=response['segments'][0]['origin'],
                      originFull=origin_full,
                      destination=response['segments'][0]['destination'],
                      destinationFull=destination_full
                      )

    @staticmethod
    def _format_date_for_api(d: Union[datetime, date, str]):
        if isinstance(d, str):
            return d

        if isinstance(d, datetime):
            return d.date().isoformat()

        if isinstance(d, date):
            return d.isoformat()

    @staticmethod
    def _format_time_for_api(t: Union[time, str]):
        if isinstance(t, str):
            return t

        if isinstance(t, time):
            return t.strftime("%H:%M")

    @property
    def num_queries(self):
        return self._num_queries

    @deprecated(version="2.0.0", reason="deprecated in favour of get_cheapest_flights", action="once")
    def get_flights(self, airport, date_from, date_to, destination_country=None):
        return self.get_cheapest_flights(airport, date_from, date_to, destination_country)

    @deprecated(version="2.0.0", reason="deprecated in favour of get_cheapest_return_flights", action="once")
    def get_return_flights(self, source_airport, date_from, date_to,
                           return_date_from, return_date_to,
                           destination_country=None):
        return self.get_cheapest_return_flights(source_airport, date_from, date_to,
                                                return_date_from, return_date_to, destination_country)
