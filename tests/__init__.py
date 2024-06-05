import unittest
from unittest.mock import patch, Mock

import requests

from ryanair import Ryanair


class TestRyanair(unittest.TestCase):

    @patch('ryanair.SessionManager.SessionManager.get_session')
    def test_initialization(self, mock_get_session):
        ryanair_instance = Ryanair()
        mock_get_session.assert_called_once()

    @patch('ryanair.SessionManager.SessionManager.get_session')
    def test_retryable_query_success(self, mock_get_session):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get_session.return_value.get.return_value = mock_response
        ryanair_instance = Ryanair()
        response = ryanair_instance._retryable_query('mock_url')
        self.assertEqual(response.status_code, 200)

    @patch('ryanair.SessionManager.SessionManager.get_session')
    def test_retryable_query_client_error(self, mock_get_session):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        mock_get_session.return_value.get.return_value = mock_response
        ryanair_instance = Ryanair()
        with self.assertRaises(requests.HTTPError):
            ryanair_instance._retryable_query('mock_url')

    @patch('ryanair.SessionManager.SessionManager.get_session')
    def test_retryable_query_server_error(self, mock_get_session):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        mock_get_session.return_value.get.return_value = mock_response
        ryanair_instance = Ryanair()
        with self.assertRaises(requests.HTTPError):
            ryanair_instance._retryable_query('mock_url')

    @patch('ryanair.SessionManager.SessionManager.get_session')
    def test_retryable_query_connection_error(self, mock_get_session):
        mock_get_session.return_value.get.side_effect = requests.ConnectionError()
        ryanair_instance = Ryanair()
        with self.assertRaises(requests.ConnectionError):
            ryanair_instance._retryable_query('mock_url')

    # ... tests for other public methods ...


if __name__ == '__main__':
    unittest.main()
