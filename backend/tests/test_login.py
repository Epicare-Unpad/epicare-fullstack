import unittest
from unittest.mock import patch, MagicMock
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from routers.register.login import login_user
from model.LoginInput import LoginInput
from dotenv import load_dotenv

load_dotenv()


class TestLoginUser(unittest.IsolatedAsyncioTestCase):

    @patch("routers.register.db.supabase", new_callable=MagicMock)
    @patch("routers.register.login.verify_password")
    async def test_user_not_found(self, mock_verify_password, mock_supabase):
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        login_input = LoginInput(email="test@example.com", password="password")

        response = await login_user(login_input)

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('"success":false', response.text)

    @patch("routers.register.db.supabase", new_callable=MagicMock)
    @patch("routers.register.login.verify_password")
    async def test_password_mismatch(self, mock_verify_password, mock_supabase):
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {"id": 1, "email": "test@example.com",
             "password_hash": "hashed_pw", "verified": True}
        ]
        mock_verify_password.return_value = False
        login_input = LoginInput(
            email="test@example.com", password="wrongpassword")

        response = await login_user(login_input)

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('"success":false', response.text)

    @patch("routers.register.db.supabase", new_callable=MagicMock)
    @patch("routers.register.login.verify_password")
    async def test_user_not_verified(self, mock_verify_password, mock_supabase):
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {"id": 1, "email": "test@example.com",
             "password_hash": "hashed_pw", "verified": False}
        ]
        mock_verify_password.return_value = True
        login_input = LoginInput(email="test@example.com", password="password")

        response = await login_user(login_input)

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('"success":false', response.text)
        self.assertIn("Please verify your email", response.text)

    @patch("routers.register.db.supabase", new_callable=MagicMock)
    @patch("routers.register.login.verify_password")
    async def test_successful_login(self, mock_verify_password, mock_supabase):
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {"id": 1, "email": "test@example.com", "password_hash": "hashed_pw",
             "verified": True, "name": "Test User"}
        ]
        mock_verify_password.return_value = True
        login_input = LoginInput(email="test@example.com", password="password")

        mock_request = MagicMock(spec=Request)
        mock_request.session = {}

        response = await login_user(login_input, request=mock_request)

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('"success":true', response.text)
        self.assertEqual(
            mock_request.session["user"]["email"], "test@example.com")

    @patch("routers.register.db.supabase", new_callable=MagicMock)
    @patch("routers.register.login.verify_password")
    async def test_exception_handling(self, mock_verify_password, mock_supabase):
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception(
            "DB error")
        login_input = LoginInput(email="test@example.com", password="password")

        response = await login_user(login_input)

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("Unexpected error", response.text)


if __name__ == "__main__":
    unittest.main()
