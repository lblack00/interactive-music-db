import unittest
from unittest.mock import patch
from app import app

class TestRelease(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.release.get_release')
    def test_get_release(self, mock_release):
        release_id = 12345

        # essentially, patch allows use to set return value of get_release() here
        mock_release.return_value = [{"id": release_id, "title": "Test Release"}]

		# make get request to release
        response = self.app.get(f'/release/?release_id={release_id}')
        data = response.get_json()

       	# assert response values
        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", data)
        self.assertIn("release", data["payload"])
        self.assertEqual(data["payload"]["release"][0]["title"], "Test Release")

if __name__ == '__main__':
    unittest.main()
