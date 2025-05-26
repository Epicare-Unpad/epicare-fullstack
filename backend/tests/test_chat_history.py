from routers.chat_history import router
import unittest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from uuid import uuid4
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


# Prepare a mock FastAPI app with the chat_history router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

user_id = str(uuid4())
chat_id = str(uuid4())


class TestChatHistoryAPI(unittest.TestCase):

    @patch("routers.register.db.supabase")
    def test_create_chat(self, mock_supabase):
        mock_supabase.from_.return_value.insert.return_value.execute.return_value.status_code = 201
        mock_supabase.from_.return_value.insert.return_value.execute.return_value.data = [{
            "id": chat_id,
            "user_id": user_id,
            "title": "New Chat",
            "created_at": "2025-05-26T00:00:00"
        }]
        response = client.post("/chat_history/chats",
                               json={"user_id": user_id, "title": "New Chat"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "New Chat")

    @patch("routers.register.db.supabase")
    def test_get_chats(self, mock_supabase):
        mock_supabase.from_.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.status_code = 200
        mock_supabase.from_.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = [{
            "id": chat_id,
            "user_id": user_id,
            "title": "Chat 1",
            "created_at": "2025-05-25T12:00:00"
        }]
        response = client.get(f"/chat_history/chats/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    @patch("routers.register.db.supabase")
    def test_create_message(self, mock_supabase):
        mock_supabase.from_.return_value.insert.return_value.execute.return_value.status_code = 201
        mock_supabase.from_.return_value.insert.return_value.execute.return_value.data = [{
            "id": str(uuid4()),
            "chat_id": chat_id,
            "sender": "user",
            "content": "Hello",
            "created_at": "2025-05-26T01:00:00"
        }]
        response = client.post("/chat_history/messages", json={
            "chat_id": chat_id,
            "sender": "user",
            "content": "Hello"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["content"], "Hello")

    @patch("routers.register.db.supabase")
    def test_get_messages(self, mock_supabase):
        mock_supabase.from_.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.status_code = 200
        mock_supabase.from_.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = [{
            "id": str(uuid4()),
            "chat_id": chat_id,
            "sender": "bot",
            "content": "Hi!",
            "created_at": "2025-05-26T01:05:00"
        }]
        response = client.get(f"/chat_history/messages/{chat_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    @patch("routers.register.db.supabase")
    def test_update_chat_title(self, mock_supabase):
        mock_supabase.from_.return_value.update.return_value.eq.return_value.execute.return_value.status_code = 200
        mock_supabase.from_.return_value.update.return_value.eq.return_value.execute.return_value.data = [{
            "id": chat_id,
            "user_id": user_id,
            "title": "Updated Title",
            "created_at": "2025-05-26T01:00:00"
        }]
        response = client.patch(
            f"/chat_history/chats/{chat_id}", json={"title": "Updated Title"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated Title")

    @patch("routers.register.db.supabase")
    def test_delete_chat(self, mock_supabase):
        mock_supabase.from_.return_value.delete.return_value.eq.return_value.execute.return_value.status_code = 200
        response = client.delete(f"/chat_history/chats/{chat_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Chat deleted successfully", response.json()["message"])
