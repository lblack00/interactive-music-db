# This file was written by Lucas Black
import unittest
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash
from users import users

class TestUsersIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_patch = patch('users.db_utils')
        cls.mock_db_utils = cls.db_patch.start()
        cls.mock_db = MagicMock()
        cls.mock_db_utils.return_value = cls.mock_db
        users.db = cls.mock_db
        
        cls.test_username = "user"
        cls.test_email = "user@example.com"
        cls.test_password = "password"
        cls.test_hash = generate_password_hash(cls.test_password)
        cls.test_user_id = 999
        cls.test_user_data = {
            "id": cls.test_user_id,
            "username": cls.test_username,
            "email": cls.test_email,
            "password": cls.test_hash,
            "is_admin": False
        }
    
    @classmethod
    def tearDownClass(cls):
        cls.db_patch.stop()
    
    def setUp(self):
        self.mock_db.reset_mock()
    
    def test_user_registration_and_login_flow(self):
        self.mock_db.read_data.side_effect = [
            [],
            [{"password": self.test_hash}],
            [self.test_user_data]
        ]
        self.mock_db.mutate_data.return_value = [[self.test_user_id]]
        
        exists = users.check_username_exists(self.test_username)
        self.assertFalse(exists)
        user_id = users.create_new_user(self.test_username, self.test_email, self.test_hash)
        self.assertEqual(user_id, self.test_user_id)
        is_valid = users.validate_user(self.test_username, self.test_password)
        self.assertTrue(is_valid)
        user_data = users.get_user(self.test_username)
        self.assertEqual(user_data, [self.test_user_data])

        expected_calls = [
            unittest.mock.call("SELECT * FROM users WHERE username=%s;", (self.test_username,)),
            unittest.mock.call("SELECT * FROM users WHERE username=%s;", (self.test_username,)),
            unittest.mock.call("SELECT * FROM users WHERE username=%s;", (self.test_username,))
        ]
        self.assertEqual(self.mock_db.read_data.call_args_list, expected_calls)
        
    def test_admin_check_flow(self):
        admin_username = "admin"
        self.mock_db.read_data.side_effect = [[{"is_admin": True}]]

        is_admin = users.is_user_admin(admin_username)
        self.assertTrue(is_admin)
        self.mock_db.read_data.assert_called_once_with(
            "SELECT is_admin FROM users WHERE username=%s;",
            (admin_username,)
        )
        
    def test_error_handling(self):
        self.mock_db.read_data.side_effect = Exception("Database connection error")
        
        with self.assertRaises(Exception) as context:
            users.check_username_exists("testuser")
            
        self.assertTrue("Database connection error" in str(context.exception))

if __name__ == '__main__':
    unittest.main()