from routers.register.register import register_user
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.responses import JSONResponse
from fastapi import status
import sys
import os
from datetime import datetime
from fastapi import HTTPException
import unittest
from fastapi.requests import Request
# Tambahkan path backend ke sys agar bisa impor modul
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class FakeRequest:
    def __init__(self, json_data):
        self._json_data = json_data

    async def json(self):
        return self._json_data


class TestRegisterUser(unittest.IsolatedAsyncioTestCase):

    @patch("routers.register.register.get_supabase", new_callable=MagicMock)
    @patch("routers.register.register.send_verification_email")
    @patch("routers.register.register.hash_password", return_value="hashed_password")
    async def test_successful_register(self, mock_hash, mock_send_email, mock_supabase):
        # Supabase seolah email belum ada
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
            {"id": "user-123"}]

        request = MagicMock()
        request.json = AsyncMock(return_value={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "securepassword",
            "gender": "male",
            "date": "2024-05-01"
        })

        response = await register_user(request)
        self.assertIn("message", response)
        self.assertIn("User registered successfully", response["message"])

    @patch("routers.register.register.get_supabase", new_callable=MagicMock)
    @patch("routers.register.register.send_verification_email")
    @patch("routers.register.register.hash_password", return_value="hashed_password")
    async def test_email_already_registered(self, mock_hash, mock_send_email, mock_supabase):
        # Supabase seolah email sudah ada
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {"id": "exists"}]

        request = MagicMock()
        request.json = AsyncMock(return_value={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "securepassword",
            "gender": "male",
            "date": "2024-05-01"
        })

        with self.assertRaises(HTTPException) as context:
            await register_user(request)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Email already registered.")

    async def test_invalid_payload(self):
        request = MagicMock()
        request.json = AsyncMock(return_value={
            "email": "invalid"
        })

        response = await register_user(request)
        self.assertEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main()
