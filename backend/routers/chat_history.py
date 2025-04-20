from fastapi import APIRouter, HTTPException
from routers.register.db import supabase
from typing import List
from pydantic import BaseModel
from uuid import UUID

router = APIRouter(
    prefix="/chat_history",
    tags=["chat_history"]
)


@router.get("/test")
async def test_endpoint():
    return {"message": "Chat history router is working"}


class Chat(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    created_at: str


class Message(BaseModel):
    id: UUID
    chat_id: UUID
    sender: str
    content: str
    created_at: str


@router.get("/chats/{user_id}", response_model=List[Chat])
async def get_chats(user_id: UUID):
    response = supabase\
        .from_("chats")\
        .select("*")\
        .eq("user_id", str(user_id))\
        .order("created_at", desc=True)\
        .execute()
    status_code = getattr(response, 'status_code', None)
    if status_code is not None and status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch chats")
    if response.data is None:
        raise HTTPException(status_code=500, detail="Failed to fetch chats")
    return response.data


class ChatCreateRequest(BaseModel):
    user_id: UUID
    title: str


@router.post("/chats", response_model=Chat)
async def create_chat(chat: ChatCreateRequest):
    from datetime import datetime
    now_iso = datetime.utcnow().isoformat()
    response = supabase.from_("chats").insert({
        "user_id": str(chat.user_id),
        "title": chat.title,
        "created_at": now_iso
    }).execute()
    status_code = getattr(response, 'status_code', None)
    if status_code is not None and status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to create chat")
    if response.data is None or len(response.data) == 0:
        raise HTTPException(status_code=500, detail="Failed to create chat")
    return response.data[0]


@router.get("/messages/{chat_id}", response_model=List[Message])
async def get_messages(chat_id: UUID):
    response = supabase\
        .from_("messages")\
        .select("*")\
        .eq("chat_id", str(chat_id))\
        .order("created_at", desc=False)\
        .execute()
    status_code = getattr(response, 'status_code', None)
    if status_code is not None and status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch messages")
    if response.data is None:
        raise HTTPException(status_code=500, detail="Failed to fetch messages")
    return response.data


class MessageCreateRequest(BaseModel):
    chat_id: UUID
    sender: str
    content: str


@router.post("/messages", response_model=Message)
async def create_message(message: MessageCreateRequest):
    from datetime import datetime
    now_iso = datetime.utcnow().isoformat()
    response = supabase.from_("messages").insert({
        "chat_id": str(message.chat_id),
        "sender": message.sender,
        "content": message.content,
        "created_at": now_iso
    }).execute()
    status_code = getattr(response, 'status_code', None)
    if status_code is not None and status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to create message")
    if response.data is None or len(response.data) == 0:
        raise HTTPException(status_code=500, detail="Failed to create message")
    return response.data[0]


@router.delete("/chats/{chat_id}")
async def delete_chat(chat_id: UUID):
    # Delete messages associated with the chat
    response_messages = supabase.from_("messages").delete().eq(
        "chat_id", str(chat_id)).execute()
    status_code_messages = getattr(response_messages, 'status_code', None)
    if status_code_messages is not None and status_code_messages != 200:
        raise HTTPException(
            status_code=500, detail="Failed to delete messages")

    # Delete the chat
    response_chat = supabase.from_("chats").delete().eq(
        "id", str(chat_id)).execute()
    status_code_chat = getattr(response_chat, 'status_code', None)
    if status_code_chat is not None and status_code_chat != 200:
        raise HTTPException(status_code=500, detail="Failed to delete chat")

    return {"message": "Chat deleted successfully"}
