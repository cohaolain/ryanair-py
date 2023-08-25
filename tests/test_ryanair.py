import datetime
import unittest
from unittest import mock
from unittest.mock import patch, Mock, call


import requests

from ryanair import Ryanair
from ryanair.types import Flight, Trip

MOCKED_ONE_WAY_RESPONSE = {
    "arrivalAirportCategories": None,
    "fares": [
        {
            "outbound": {
                "departureAirport": {
                    "countryName": "Ireland",
                    "iataCode": "DUB",
                    "name": "Dublin",
                    "seoName": "dublin",
                    "city": {"name": "Dublin", "code": "DUBLIN", "countryCode": "ie"},
                },
                "arrivalAirport": {
                    "countryName": "United Kingdom",
                    "iataCode": "BRS",
                    "name": "Bristol",
                    "seoName": "bristol",
                    "city": {"name": "Bristol", "code": "BRISTOL", "countryCode": "gb"},
                },
                "departureDate": "2023-08-23T08:20:00",
                "arrivalDate": "2023-08-23T09:30:00",
                "price": {
                    "value": 17.68,
                    "valueMainUnit": "17",
                    "valueFractionalUnit": "68",
                    "currencyCode": "EUR",
                    "currencySymbol": "€",
                },
                "flightKey": "FR~ 504~ ~~DUB~08/23/2023 08:20~BRS~08/23/2023 09:30~~",
                "flightNumber": "FR504",
                "previousPrice": None,
                "priceUpdated": 1692686097000,
            },
            "summary": {
                "price": {
                    "value": 17.68,
                    "valueMainUnit": "17",
                    "valueFractionalUnit": "68",
                    "currencyCode": "EUR",
                    "currencySymbol": "€",
                },
                "previousPrice": None,
                "newRoute": False,
            },
        },
        {
            "outbound": {
                "departureAirport": {
                    "countryName": "Ireland",
                    "iataCode": "DUB",
                    "name": "Dublin",
                    "seoName": "dublin",
                    "city": {"name": "Dublin", "code": "DUBLIN", "countryCode": "ie"},
                },
                "arrivalAirport": {
                    "countryName": "United Kingdom",
                    "iataCode": "EDI",
                    "name": "Edinburgh",
                    "seoName": "edinburgh",
                    "city": {
                        "name": "Edinburgh",
                        "code": "EDINBURGH",
                        "countryCode": "gb",
                    },
                },
                "departureDate": "2023-08-23T06:30:00",
                "arrivalDate": "2023-08-23T07:40:00",
                "price": {
                    "value": 17.68,
                    "valueMainUnit": "17",
                    "valueFractionalUnit": "68",
                    "currencyCode": "EUR",
                    "currencySymbol": "€",
                },
                "flightKey": "FR~ 812~ ~~DUB~08/23/2023 06:30~EDI~08/23/2023 07:40~~",
                "flightNumber": "FR812",
                "previousPrice": None,
                "priceUpdated": 1692693061000,
            },
            "summary": {
                "price": {
                    "value": 17.68,
                    "valueMainUnit": "17",
                    "valueFractionalUnit": "68",
                    "currencyCode": "EUR",
                    "currencySymbol": "€",
                },
                "previousPrice": None,
                "newRoute": False,
            },
        },
    ],
    "nextPage": None,
    "size": 2,
}

MOCKED_RETURN_RESPONSE = {
    "arrivalAirportCategories": None,
    "fares": [
        {
            "outbound": {
                "departureAirport": {
                    "countryName": "Ireland",
                    "iataCode": "DUB",
                    "name": "Dublin",
                    "seoName": "dublin",
                    "city": {"name": "Dublin", "code": "DUBLIN", "countryCode": "ie"},
                },
                "arrivalAirport": {
                    "countryName": "United Kingdom",
                    "iataCode": "LBA",
                    "name": "Leeds Bradford",
                    "seoName": "leeds",
                    "city": {"name": "Leeds", "code": "LEEDS", "countryCode": "gb"},
                },
                "departureDate": "2023-08-23T06:25:00",
                "arrivalDate": "2023-08-23T07:30:00",
                "price": {
                    "value": 17.59,
                    "valueMainUnit": "17",
                    "valueFractionalUnit": "59",
                    "currencyCode": "EUR",
                    "currencySymbol": "€",
                },
                "flightKey": "FR~ 152~ ~~DUB~08/23/2023 06:25~LBA~08/23/2023 07:30~~",
                "flightNumber": "FR152",
                "previousPrice": None,
                "priceUpdated": 1692687660000,
            },
            "inbound": {
                "departureAirport": {
                    "countryName": "United Kingdom",
                    "iataCode": "LBA",
                    "name": "Leeds Bradford",
                    "seoName": "leeds",
                    "city": {"name": "Leeds", "code": "LEEDS", "countryCode": "gb"},
                },
                "arrivalAirport": {
                    "countryName": "Ireland",
                    "iataCode": "DUB",
                    "name": "Dublin",
                    "seoName": "dublin",
                    "city": {"name": "Dublin", "code": "DUBLIN", "countryCode": "ie"},
                },
                "departureDate": "2023-08-24T20:20:00",
                "arrivalDate": "2023-08-24T21:20:00",
                "price": {
                    "value": 18.76,
                    "valueMainUnit": "18",
                    "valueFractionalUnit": "76",
                    "currencyCode": "EUR",
                    "currencySymbol": "€",
                },
                "flightKey": "FR~ 456~ ~~LBA~08/24/2023 20:20~DUB~08/24/2023 21:20~~",
                "flightNumber": "FR456",
                "previousPrice": None,
                "priceUpdated": 1692685719000,
            },
            "summary": {
                "price": {
                    "value": 36.35,
                    "valueMainUnit": "36",
                    "valueFractionalUnit": "35",
                    "currencyCode": "EUR",
                    "currencySymbol": "€",
                },
                "previousPrice": None,
                "newRoute": False,
                "tripDurationDays": 1,
            },
        },
        {
            "outbound": {
                "departureAirport": {
                    "countryName": "Ireland",
                    "iataCode": "DUB",
                    "name": "Dublin",
                    "seoName": "dublin",
                    "city": {"name": "Dublin", "code": "DUBLIN", "countryCode": "ie"},
                },
                "arrivalAirport": {
                    "countryName": "United Kingdom",
                    "iataCode": "LPL",
                    "name": "Liverpool",
                    "seoName": "liverpool",
                    "city": {
                        "name": "Liverpool",
                        "code": "LIVERPOOL",
                        "countryCode": "gb",
                    },
                },
                "departureDate": "2023-08-23T15:20:00",
                "arrivalDate": "2023-08-23T16:15:00",
                "price": {
                    "value": 20.6,
                    "valueMainUnit": "20",
                    "valueFractionalUnit": "60",
                    "currencyCode": "EUR",
                    "currencySymbol": "€",
                },
                "flightKey": "FR~ 448~ ~~DUB~08/23/2023 15:20~LPL~08/23/2023 16:15~~",
                "flightNumber": "FR448",
                "previousPrice": None,
                "priceUpdated": 1692693055000,
            },
            "inbound": {
                "departureAirport": {
                    "countryName": "United Kingdom",
                    "iataCode": "LPL",
                    "name": "Liverpool",
                    "seoName": "liverpool",
                    "city": {
                        "name": "Liverpool",
                        "code": "LIVERPOOL",
                        "countryCode": "gb",
                    },
                },
                "arrivalAirport": {
                    "countryName": "Ireland",
                    "iataCode": "DUB",
                    "name": "Dublin",
                    "seoName": "dublin",
                    "city": {"name": "Dublin", "code": "DUBLIN", "countryCode": "ie"},
                },
                "departureDate": "2023-08-24T21:20:00",
                "arrivalDate": "2023-08-24T22:15:00",
                "price": {
                    "value": 18.51,
                    "valueMainUnit": "18",
                    "valueFractionalUnit": "51",
                    "currencyCode": "EUR",
                    "currencySymbol": "€",
                },
                "flightKey": "FR~ 447~ ~~LPL~08/24/2023 21:20~DUB~08/24/2023 22:15~~",
                "flightNumber": "FR447",
                "previousPrice": None,
                "priceUpdated": 1692686981000,
            },
            "summary": {
                "price": {
                    "value": 39.11,
                    "valueMainUnit": "39",
                    "valueFractionalUnit": "11",
                    "currencyCode": "EUR",
                    "currencySymbol": "€",
                },
                "previousPrice": None,
                "newRoute": False,
                "tripDurationDays": 1,
            },
        },
    ],
    "nextPage": None,
    "size": 2,
}


class TestRyanair(unittest.TestCase):
    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_initialization(self, mock_get_session):
        _ = Ryanair()
        mock_get_session.assert_called_once()

    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_retryable_query_success(self, mock_get_session):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"fares": []}
        mock_get_session.return_value.get.return_value = mock_response
        ryanair_instance = Ryanair()
        response = ryanair_instance._retryable_query("mock_url")
        self.assertEqual(response, {"fares": []})

    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_retryable_query_client_error(self, mock_get_session):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        mock_get_session.return_value.get.return_value = mock_response
        ryanair_instance = Ryanair()
        with self.assertRaises(requests.HTTPError):
            ryanair_instance._retryable_query("mock_url")

    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_retryable_query_server_error(self, mock_get_session):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        mock_get_session.return_value.get.return_value = mock_response
        ryanair_instance = Ryanair()
        with self.assertRaises(requests.HTTPError):
            ryanair_instance._retryable_query("mock_url")

    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_retryable_query_connection_error(self, mock_get_session):
        mock_get_session.return_value.get.side_effect = requests.ConnectionError()
        ryanair_instance = Ryanair()
        with self.assertRaises(requests.ConnectionError):
            ryanair_instance._retryable_query("mock_url")

    # Test the get_cheapest_flights method
    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_get_cheapest_flights(self, mock_get_session):
        mock_response = Mock()
        mock_response.json.return_value = MOCKED_ONE_WAY_RESPONSE
        mock_get_session.return_value.get.return_value = mock_response

        ryanair_instance = Ryanair()
        flights = ryanair_instance.get_cheapest_flights(
            "DUB", "2023-09-01", "2023-09-30"
        )

        self.assertIsNotNone(flights)
        self.assertTrue(len(flights) > 0)
        self.assertEqual(
            flights,
            [
                Flight(
                    departureTime=datetime.datetime(2023, 8, 23, 8, 20),
                    flightNumber="FR 504",
                    price=17.68,
                    currency="EUR",
                    origin="DUB",
                    originFull="Dublin, Ireland",
                    destination="BRS",
                    destinationFull="Bristol, United Kingdom",
                ),
                Flight(
                    departureTime=datetime.datetime(2023, 8, 23, 6, 30),
                    flightNumber="FR 812",
                    price=17.68,
                    currency="EUR",
                    origin="DUB",
                    originFull="Dublin, Ireland",
                    destination="EDI",
                    destinationFull="Edinburgh, United Kingdom",
                ),
            ],
        )

    # Test error handling in get_cheapest_flights method
    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_get_cheapest_flights_handles_errors(self, mock_get_session):
        mock_get_session.return_value.get.side_effect = requests.HTTPError()

        ryanair_instance = Ryanair()
        with self.assertRaises(requests.HTTPError):
            ryanair_instance.get_cheapest_flights("DUB", "2023-09-01", "2023-09-30")

    # Test the get_cheapest_return_flights method
    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_get_cheapest_return_flights(self, mock_get_session):
        mock_response = Mock()
        mock_response.json.return_value = MOCKED_RETURN_RESPONSE
        mock_get_session.return_value.get.return_value = mock_response

        ryanair_instance = Ryanair()
        trips = ryanair_instance.get_cheapest_return_flights(
            "DUB", "2023-09-01", "2023-09-15", "2023-09-16", "2023-09-30"
        )

        self.assertIsNotNone(trips)
        self.assertTrue(len(trips) > 0)
        self.assertEqual(
            trips,
            [
                Trip(
                    totalPrice=36.35,
                    outbound=Flight(
                        departureTime=datetime.datetime(2023, 8, 23, 6, 25),
                        flightNumber="FR 152",
                        price=17.59,
                        currency="EUR",
                        origin="DUB",
                        originFull="Dublin, Ireland",
                        destination="LBA",
                        destinationFull="Leeds Bradford, United Kingdom",
                    ),
                    inbound=Flight(
                        departureTime=datetime.datetime(2023, 8, 24, 20, 20),
                        flightNumber="FR 456",
                        price=18.76,
                        currency="EUR",
                        origin="LBA",
                        originFull="Leeds Bradford, United Kingdom",
                        destination="DUB",
                        destinationFull="Dublin, Ireland",
                    ),
                ),
                Trip(
                    totalPrice=39.11,
                    outbound=Flight(
                        departureTime=datetime.datetime(2023, 8, 23, 15, 20),
                        flightNumber="FR 448",
                        price=20.6,
                        currency="EUR",
                        origin="DUB",
                        originFull="Dublin, Ireland",
                        destination="LPL",
                        destinationFull="Liverpool, United Kingdom",
                    ),
                    inbound=Flight(
                        departureTime=datetime.datetime(2023, 8, 24, 21, 20),
                        flightNumber="FR 447",
                        price=18.51,
                        currency="EUR",
                        origin="LPL",
                        originFull="Liverpool, United Kingdom",
                        destination="DUB",
                        destinationFull="Dublin, Ireland",
                    ),
                ),
            ],
        )

    # Test error handling in get_cheapest_return_flights method
    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_get_cheapest_return_flights_handles_errors(self, mock_get_session):
        mock_get_session.return_value.get.side_effect = requests.HTTPError()

        ryanair_instance = Ryanair()
        with self.assertRaises(requests.HTTPError):
            ryanair_instance.get_cheapest_return_flights(
                "DUB",
                "2023-09-01",
                "2023-09-30",
                "2023-10-01",
                "2023-10-30",
            )
        self.assertEqual(ryanair_instance.num_queries, 5)

    # Test the retryable_query method's retry mechanism
    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_retryable_query_retries_on_failure(self, mock_get_session):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"fares": []}

        mock_get_session.return_value.get.side_effect = [
            requests.ConnectionError(),
            mock_response,
        ]

        ryanair_instance = Ryanair()
        response = ryanair_instance._retryable_query("mock_url")

        self.assertEqual(response, {"fares": []})
        mock_get_session.return_value.get.assert_has_calls(
            [call("mock_url", params=None), call("mock_url", params=None)]
        )
        self.assertEqual(ryanair_instance.num_queries, 2)

    # Ensure we don't try more than 5 times
    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_retryable_query_retries_on_failure_5_times(self, mock_get_session):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"fares": []}

        mock_get_session.return_value.get.side_effect = [
            requests.ConnectionError(),
            requests.ConnectionError(),
            requests.ConnectionError(),
            requests.ConnectionError(),
            requests.ConnectionError(),
            mock_response,  # even though a 6th call would succeed, we shouldn't get this far
        ]

        ryanair_instance = Ryanair()
        with self.assertRaises(requests.ConnectionError):
            _ = ryanair_instance._retryable_query("mock_url")

        mock_get_session.return_value.get.assert_has_calls(
            [
                call("mock_url", params=None),
                call("mock_url", params=None),
                call("mock_url", params=None),
                call("mock_url", params=None),
                call("mock_url", params=None),
            ]
        )
        self.assertEqual(ryanair_instance.num_queries, 5)

    # Test logging of exceptions
    @patch("ryanair.SessionManager.SessionManager.get_session")
    @patch("ryanair.ryanair.logger")
    def test_logging_of_exceptions(self, mock_logger, mock_get_session):
        mock_get_session.return_value.get.side_effect = requests.HTTPError()

        ryanair_instance = Ryanair()
        with self.assertRaises(requests.HTTPError):
            ryanair_instance.get_cheapest_flights("DUB", "2023-09-01", "2023-09-30")

        mock_logger.exception.assert_called_once_with(mock.ANY)

    # Test that we log a warning if currency of API response doesn't match
    @patch("ryanair.SessionManager.SessionManager.get_session")
    @patch("ryanair.ryanair.logger")
    def test_logging_of_incorrect_currency_response(
        self, mock_logger, mock_get_session
    ):
        mock_response = Mock()
        mock_response.json.return_value = MOCKED_ONE_WAY_RESPONSE
        mock_get_session.return_value.get.return_value = mock_response
        request_currency = "FAKECURRENCY"

        ryanair_instance = Ryanair(request_currency)
        _ = ryanair_instance.get_cheapest_flights("DUB", "2023-09-01", "2023-09-30")

        mock_logger.warning.assert_has_calls(
            [
                call(
                    f"Requested cheapest flights in {request_currency} but API responded with fares in EUR"
                ),
                call(
                    f"Requested cheapest flights in {request_currency} but API responded with fares in EUR"
                ),
            ]
        )

    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_currency_added_to_relevant_queries_if_provided(self, mock_get_session):
        mock_get_session.return_value.get.return_value.json.return_value = {"fares": []}

        ryanair_instance = Ryanair("EUR")
        ryanair_instance.get_cheapest_flights("DUB", "2023-08-23", "2023-08-23")
        ryanair_instance.get_cheapest_return_flights(
            "DUB", "2023-08-23", "2023-08-23", "2023-09-25", "2023-09-25"
        )

        mock_get_session.return_value.get.assert_has_calls(
            [
                call(
                    mock.ANY,
                    params={
                        "departureAirportIataCode": "DUB",
                        "outboundDepartureDateFrom": "2023-08-23",
                        "outboundDepartureDateTo": "2023-08-23",
                        "outboundDepartureTimeFrom": "00:00",
                        "outboundDepartureTimeTo": "23:59",
                        "currency": "EUR",
                    },
                ),
                call(
                    mock.ANY,
                    params={
                        "departureAirportIataCode": "DUB",
                        "outboundDepartureDateFrom": "2023-08-23",
                        "outboundDepartureDateTo": "2023-08-23",
                        "inboundDepartureDateFrom": "2023-09-25",
                        "inboundDepartureDateTo": "2023-09-25",
                        "outboundDepartureTimeFrom": "00:00",
                        "outboundDepartureTimeTo": "23:59",
                        "inboundDepartureTimeFrom": "00:00",
                        "inboundDepartureTimeTo": "23:59",
                        "currency": "EUR",
                    },
                ),
            ],
            any_order=True,
        )

    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_currency_not_added_to_relevant_queries_if_not_provided(
        self, mock_get_session
    ):
        mock_get_session.return_value.get.return_value.json.return_value = {"fares": []}

        ryanair_instance = Ryanair()
        ryanair_instance.get_cheapest_flights("DUB", "2023-08-23", "2023-08-23")
        ryanair_instance.get_cheapest_return_flights(
            "DUB", "2023-08-23", "2023-08-23", "2023-09-25", "2023-09-25"
        )

        mock_get_session.return_value.get.assert_has_calls(
            [
                call(
                    mock.ANY,
                    params={
                        "departureAirportIataCode": "DUB",
                        "outboundDepartureDateFrom": "2023-08-23",
                        "outboundDepartureDateTo": "2023-08-23",
                        "outboundDepartureTimeFrom": "00:00",
                        "outboundDepartureTimeTo": "23:59",
                    },
                ),
                call(
                    mock.ANY,
                    params={
                        "departureAirportIataCode": "DUB",
                        "outboundDepartureDateFrom": "2023-08-23",
                        "outboundDepartureDateTo": "2023-08-23",
                        "inboundDepartureDateFrom": "2023-09-25",
                        "inboundDepartureDateTo": "2023-09-25",
                        "outboundDepartureTimeFrom": "00:00",
                        "outboundDepartureTimeTo": "23:59",
                        "inboundDepartureTimeFrom": "00:00",
                        "inboundDepartureTimeTo": "23:59",
                    },
                ),
            ],
            any_order=True,
        )

    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_optional_param_added_to_relevant_queries_if_provided(
        self, mock_get_session
    ):
        mock_get_session.return_value.get.return_value.json.return_value = {"fares": []}

        ryanair_instance = Ryanair()
        ryanair_instance.get_cheapest_flights(
            "DUB",
            "2023-08-23",
            "2023-08-23",
            destination_airport="LGW",
            max_price=100,
            destination_country="UK",
            custom_params={"custom": "cVal"},
        )
        ryanair_instance.get_cheapest_return_flights(
            "DUB",
            "2023-08-23",
            "2023-08-23",
            "2023-09-25",
            "2023-09-25",
            destination_country="DE",
            destination_airport="LGW",
            max_price=100,
            custom_params={"custom2": "cVal2"},
        )

        mock_get_session.return_value.get.assert_has_calls(
            [
                call(
                    mock.ANY,
                    params={
                        "departureAirportIataCode": "DUB",
                        "outboundDepartureDateFrom": "2023-08-23",
                        "outboundDepartureDateTo": "2023-08-23",
                        "outboundDepartureTimeFrom": "00:00",
                        "outboundDepartureTimeTo": "23:59",
                        "arrivalAirportIataCode": "LGW",
                        "arrivalCountryCode": "UK",
                        "priceValueTo": 100,
                        "custom": "cVal",
                    },
                ),
                call(
                    mock.ANY,
                    params={
                        "departureAirportIataCode": "DUB",
                        "outboundDepartureDateFrom": "2023-08-23",
                        "outboundDepartureDateTo": "2023-08-23",
                        "inboundDepartureDateFrom": "2023-09-25",
                        "inboundDepartureDateTo": "2023-09-25",
                        "outboundDepartureTimeFrom": "00:00",
                        "outboundDepartureTimeTo": "23:59",
                        "inboundDepartureTimeFrom": "00:00",
                        "inboundDepartureTimeTo": "23:59",
                        "arrivalCountryCode": "DE",
                        "priceValueTo": 100,
                        "arrivalAirportIataCode": "LGW",
                        "custom2": "cVal2",
                    },
                ),
            ],
            any_order=True,
        )

    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_all_date_time_fields_accept_valid_types(self, mock_get_session):
        mock_get_session.return_value.get.return_value.json.return_value = {"fares": []}

        ryanair_instance = Ryanair()
        ryanair_instance.get_cheapest_flights(
            "DUB",
            "2023-08-23",
            datetime.datetime(2023, 8, 24),
            departure_time_from="00:01",
            departure_time_to=datetime.datetime(2023, 8, 23, 5, 23).time(),
        )
        ryanair_instance.get_cheapest_flights(
            "DUB",
            "2023-08-25",
            datetime.datetime(2023, 8, 26).date(),
            departure_time_from=datetime.datetime(2023, 8, 23, 7, 23).time(),
            departure_time_to=datetime.datetime(2023, 8, 23, 19, 23).time(),
        )
        ryanair_instance.get_cheapest_return_flights(
            "DUB",
            "2023-08-27",
            datetime.datetime(2023, 8, 28).date(),
            "2023-08-29",
            datetime.datetime(2023, 8, 30),
            outbound_departure_time_from="07:23",
            outbound_departure_time_to=datetime.datetime(2023, 8, 23, 19, 23).time(),
            inbound_departure_time_from=datetime.datetime(2023, 8, 23, 1, 22).time(),
            inbound_departure_time_to=datetime.datetime(2023, 8, 23, 18, 21).time(),
        )

        mock_get_session.return_value.get.assert_has_calls(
            [
                call(
                    mock.ANY,
                    params={
                        "departureAirportIataCode": "DUB",
                        "outboundDepartureDateFrom": "2023-08-23",
                        "outboundDepartureDateTo": "2023-08-24",
                        "outboundDepartureTimeFrom": "00:01",
                        "outboundDepartureTimeTo": "05:23",
                    },
                ),
                call(
                    mock.ANY,
                    params={
                        "departureAirportIataCode": "DUB",
                        "outboundDepartureDateFrom": "2023-08-25",
                        "outboundDepartureDateTo": "2023-08-26",
                        "outboundDepartureTimeFrom": "07:23",
                        "outboundDepartureTimeTo": "19:23",
                    },
                ),
                call(
                    mock.ANY,
                    params={
                        "departureAirportIataCode": "DUB",
                        "outboundDepartureDateFrom": "2023-08-27",
                        "outboundDepartureDateTo": "2023-08-28",
                        "inboundDepartureDateFrom": "2023-08-29",
                        "inboundDepartureDateTo": "2023-08-30",
                        "outboundDepartureTimeFrom": "07:23",
                        "outboundDepartureTimeTo": "19:23",
                        "inboundDepartureTimeFrom": "01:22",
                        "inboundDepartureTimeTo": "18:21",
                    },
                ),
            ],
            any_order=True,
        )


if __name__ == "__main__":
    unittest.main()
