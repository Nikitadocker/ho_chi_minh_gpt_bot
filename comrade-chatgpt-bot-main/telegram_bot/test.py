import unittest
from unittest.mock import patch
from flask import Flask, jsonify

# Assuming the Flask app and healthcheck function are defined in a module named `app`
from bot import bot, check_openai_connection

class HealthcheckTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.check_openai_connection')
    def test_healthcheck_ok(self, mock_check_openai_connection):
        # Mock the check_openai_connection to return True
        mock_check_openai_connection.return_value = True

        response = self.app.get('/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "OK"})

    @patch('app.check_openai_connection')
    def test_healthcheck_error(self, mock_check_openai_connection):
        # Mock the check_openai_connection to return False
        mock_check_openai_connection.return_value = False

        response = self.app.get('/healthcheck')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"status": "ERROR"})

if __name__ == '__main__':
    unittest.main()