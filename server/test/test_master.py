# This file was written by Lucas Black
import unittest
from unittest.mock import patch, MagicMock
from app import app
from master import master

class TestMasterIntegrationAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        master.set_db_for_testing()

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_master_success(self):
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

    def test_get_master_not_found(self):
        master_id = -1

        response = self.app.get(f'/master/?master_id={master_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Master not found")

    def test_get_master_invalid_id(self):
        response = self.app.get('/master/?master_id=abc')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid master_id format")

    def test_get_master_missing_id(self):
        response = self.app.get('/master/')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Missing master_id parameter")

    def test_get_master_image_success(self):
        mock_master = MagicMock()
        mock_master.images = [{'uri': 'http://example.com/image1.jpg'}, {'uri': 'http://example.com/image2.jpg'}]
        
        mock_client = MagicMock()
        mock_client.master.return_value = mock_master
        
        result = master.get_discogs_api_master(123, True, mock_client)
        
        mock_client.master.assert_called_with(123)
        
        self.assertEqual(result, {
            "images": [{'uri': 'http://example.com/image1.jpg'}, {'uri': 'http://example.com/image2.jpg'}]
        })

    def test_get_master_image_no_images(self):
        mock_master = MagicMock()
        mock_master.images = []
        
        mock_client = MagicMock()
        mock_client.master.return_value = mock_master
        
        result = master.get_discogs_api_master(123, True, mock_client)
        
        self.assertEqual(result, {"images": []})

    def test_get_master_image_exception(self):
        mock_client = MagicMock()
        mock_client.master.side_effect = Exception("API Error")
        
        with patch('builtins.print') as mock_print:
            result = master.get_discogs_api_master(123, True, mock_client)
            mock_print.assert_called_with("Error retrieving master: API Error")
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
