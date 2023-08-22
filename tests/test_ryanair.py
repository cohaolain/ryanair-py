import unittest
from unittest.mock import patch, Mock, call


import requests

from ryanair import Ryanair

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
        ryanair_instance = Ryanair()
        mock_get_session.assert_called_once()

    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_retryable_query_success(self, mock_get_session):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get_session.return_value.get.return_value = mock_response
        ryanair_instance = Ryanair()
        response = ryanair_instance._retryable_query("mock_url")
        self.assertEqual(response.status_code, 200)

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
        # Add more assertions based on the mocked data

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
        # Add more assertions based on the mocked data

    # Test the retryable_query method's retry mechanism
    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_retryable_query_retries_on_failure(self, mock_get_session):
        mock_response = Mock()
        mock_response.status_code = 200  # Set the status code directly
        mock_get_session.return_value.get.side_effect = [
            requests.ConnectionError(),
            mock_response,  # Use the mock_response here
        ]

        ryanair_instance = Ryanair()
        response = ryanair_instance._retryable_query("mock_url")

        self.assertEqual(response.status_code, 200)
        mock_get_session.return_value.get.assert_has_calls(
            [call("mock_url"), call("mock_url")]
        )

    # Test error handling in get_cheapest_flights method
    @patch("ryanair.SessionManager.SessionManager.get_session")
    def test_get_cheapest_flights_handles_errors(self, mock_get_session):
        mock_get_session.return_value.get.side_effect = requests.HTTPError()

        ryanair_instance = Ryanair()
        with self.assertRaises(requests.HTTPError):
            ryanair_instance.get_cheapest_flights("DUB", "2023-09-01", "2023-09-30")

    # Test logging for errors or warnings
    @patch("ryanair.SessionManager.SessionManager.get_session")
    @patch("ryanair.ryanair.logger")
    def test_logging_for_errors(self, mock_logger, mock_get_session):
        mock_get_session.return_value.get.side_effect = requests.HTTPError()

        ryanair_instance = Ryanair()
        with self.assertRaises(requests.HTTPError):
            ryanair_instance.get_cheapest_flights("DUB", "2023-09-01", "2023-09-30")

        mock_logger.error.assert_called_once_with(
            "Failed to parse response when querying"
        )


if __name__ == "__main__":
    unittest.main()
