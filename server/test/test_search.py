# This file was written by Lucas Black
import json
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import app
from search import search

class TestSearchIntegrationAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        search.set_db_for_testing()

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True


    def test_user_search_artists(self):
        response = self.client.post(
            '/search',
            data=json.dumps({'query': 'test', 'filterOption': 'artists'}),
            content_type='application/json'
        )

        expected_data = [
            {
                'data_quality': 'Correct',
                'id': 12345,
                'name': 'Test Artist',
                'profile': 'Test artist profile',
                'realname': 'Real Test Artist'
            },
            {
                'data_quality': 'Correct',
                'id': 23456,
                'name': 'Test Artist 2',
                'profile': 'Another test artist profile',
                'realname': 'Real Test Artist 2'
            }
        ]

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['results'], list)
        if data['results']:
            self.assertIn('id', data['results'][0])
            self.assertIn('name', data['results'][0])
        self.assertEqual(data['results'], expected_data)

    def test_user_search_releases(self):
        response = self.client.post(
            '/search',
            data=json.dumps({'query': 'test', 'filterOption': 'releases'}),
            content_type='application/json'
        )

        expected_data = [
            {'artists': 'Unknown Artist', 'id': 45678, 'title': 'Test Album 2', 'year': '2021'},
            {'artists': 'Unknown Artist', 'id': 12345, 'title': 'Test Master', 'year': '2020'},
            {'artists': 'Unknown Artist', 'id': 34567, 'title': 'Test Album 1', 'year': '2020'}
        ]

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIsInstance(data['results'], list)
        if data['results']:
            self.assertIn('id', data['results'][0])
            self.assertIn('title', data['results'][0])
        self.assertEqual(data['results'], expected_data)

    def test_user_search_tracks(self):
        response = self.client.post(
            '/search',
            data=json.dumps({'query': 'test', 'filterOption': 'tracks'}),
            content_type='application/json'
        )

        expected_data = [
            {
                'release_id': 12345,
                'release_title': 'Test Release',
                'released': '2020',
                'title': 'Test Track'
            },
            {
                'release_id': 34567,
                'release_title': 'Test Album 1',
                'released': '2020-01-01',
                'title': 'Test Track 1'
            },
            {
                'release_id': 45678,
                'release_title': 'Test Album 2',
                'released': '2021-06-15',
                'title': 'Test Track 2'
            }
        ]

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['results'], expected_data)

    def test_user_search_invalid_filter(self):
        response = self.client.post(
            '/search',
            data=json.dumps({'query': 'test', 'filterOption': 'invalid'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['results'], [])

    def test_user_search_missing_filter(self):
        response = self.client.post(
            '/search',
            data=json.dumps({'query': 'test'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['results'], [])

if __name__ == '__main__':
    unittest.main()