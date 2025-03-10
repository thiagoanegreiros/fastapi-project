import unittest
from unittest.mock import MagicMock
from core.application.user_service import UserService
from core.domain.user import User

class TestUserService(unittest.TestCase):

    def setUp(self):
        """Set up the test with a mock repository"""
        self.mock_repo = MagicMock()
        self.user_service = UserService(self.mock_repo)

    def test_create_user(self):
        """Test that `create_user` calls `save` correctly"""
        user = User(id="id_01", name="Test User", email="test@example.com")
        self.mock_repo.save.return_value = user

        result = self.user_service.create_user(user)

        self.mock_repo.save.assert_called_once_with(user)
        self.assertEqual(result, user)

    def test_list_users(self):
        """Test that `list_users` returns a list of users"""
        users = [
            User(id="id_01", name="Alice", email="alice@email.com"),
            User(id="id_02", name="Bob", email="bob@email.com"),
        ]
        self.mock_repo.find_all.return_value = users

        result = self.user_service.list_users()

        self.mock_repo.find_all.assert_called_once() 
        self.assertEqual(result, users)

if __name__ == "__main__":
    unittest.main()
