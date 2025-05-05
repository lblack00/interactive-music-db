# This file was written by Lucas Black
import unittest
from unittest.mock import patch, MagicMock
from app import app
from release import release

class TestReleaseIntegrationAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        release.set_db_for_testing()

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_release_success(self):
        release_id = 12345

        response = self.app.get(f'/release/?release_id={release_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", data)
        self.assertIn("release", data["payload"])
        self.assertIsInstance(data["payload"]["release"], list)
        self.assertGreater(len(data["payload"]["release"]), 0)
        self.assertEqual(data["payload"]["release"][0]["title"], "Test Release")
        self.assertEqual(data["payload"]["release"][0]["id"], release_id)

    def test_get_release_not_found(self):
        release_id = -1

        response = self.app.get(f'/release/?release_id={release_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Release not found")

    def test_get_release_invalid_id(self):
        response = self.app.get('/release/?release_id=abc')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid release_id format")

    def test_get_release_missing_id(self):
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

    def test_get_release_image_success(self):
        mock_release = MagicMock()
        mock_release.images = [{'uri': 'http://example.com/image1.jpg'}, {'uri': 'http://example.com/image2.jpg'}]
        
        mock_client = MagicMock()
        mock_client.release.return_value = mock_release
        
        result = release.get_discogs_api_release(123, True, mock_client)
        
        mock_client.release.assert_called_with(123)
        
        self.assertEqual(result, {
            "images": [{'uri': 'http://example.com/image1.jpg'}, {'uri': 'http://example.com/image2.jpg'}]
        })

    def test_get_release_image_no_images(self):
        mock_release = MagicMock()
        mock_release.images = []
        
        mock_client = MagicMock()
        mock_client.release.return_value = mock_release
        
        result = release.get_discogs_api_release(123, True, mock_client)
        
        self.assertEqual(result, {"images": []})

    def test_get_release_image_exception(self):
        mock_client = MagicMock()
        mock_client.release.side_effect = Exception("API Error")
        
        with patch('builtins.print') as mock_print:
            result = release.get_discogs_api_release(123, True, mock_client)
            mock_print.assert_called_with("Error retrieving release: API Error")
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
