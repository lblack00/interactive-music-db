# This file was written by Lucas Black
import unittest
from unittest.mock import patch
from app import app

class TestRelease(unittest.TestCase):
    def setUp(self):
        """Set up the test client before each test."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.release.get_release')
    def test_get_release_success(self, mock_release):
        release_id = 12345

        # essentially, patch allows use to set return value of get_release() here
        mock_release.return_value = [{"id": release_id, "title": "Test Release"}]

        # make get request to release
        response = self.app.get(f'/release/?release_id={release_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", data)
        self.assertIn("release", data["payload"])
        self.assertIsInstance(data["payload"]["release"], list)
        self.assertGreater(len(data["payload"]["release"]), 0)
        self.assertEqual(data["payload"]["release"][0]["title"], "Test Release")
        self.assertEqual(data["payload"]["release"][0]["id"], release_id)

    @patch('app.release.get_release')
    def test_get_release_not_found(self, mock_release):
        release_id = -1

        mock_release.return_value = []

        response = self.app.get(f'/release/?release_id={release_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Release not found")

    @patch('app.release.get_release')
    def test_get_release_invalid_id(self, mock_release):
        response = self.app.get('/release/?release_id=abc')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid release_id format")

    @patch('app.release.get_release')
    def test_get_release_missing_id(self, mock_release):
        response = self.app.get('/release/')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Missing release_id parameter")

    @patch('app.release.get_release')
    def test_get_release_fail(self, mock_release):
        release_id = 12355

        mock_release.side_effect = Exception()

        response = self.app.get(f'/release/?release_id={release_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)

if __name__ == '__main__':
    unittest.main()
