import uuid
import os
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging
from .db import supabase
from model.users import UserRegisterRequest
from .auth import hash_password
import sys
import os
from utils.email_sender import send_verification_email
router = APIRouter()


@router.post("/register")
async def register_user(request: Request):
    try:
        data_json = await request.json()
        logging.info(f"Received register data: {data_json}")
        data = UserRegisterRequest(**data_json)
    except ValidationError as ve:
        logging.error(f"Validation error: {ve}")
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": ve.errors()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)})

    # Cek apakah email sudah dipakai
    existing = supabase.table("users").select(
        "id").eq("email", data.email).execute()
    if existing.data:
        raise HTTPException(
            status_code=400, detail="Email already registered.")

    hashed_pw = hash_password(data.password)

    # Generate verification token
    verification_token = str(uuid.uuid4())

    # Insert user with verified=False and verification_token
    response = supabase.table("users").insert({
        "name": data.name,
        "gender": data.gender,
        "date": data.date.isoformat(),
        "email": data.email,
        "password_hash": hashed_pw,
        "verified": False,
        "verification_token": verification_token
    }).execute()

    if response.data is None or len(response.data) == 0:
        raise HTTPException(status_code=500, detail="Gagal mendaftarkan user")

    # Send verification email
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8000")
    verification_link = f"{frontend_url}/verify-email?token={verification_token}"
    try:
        send_verification_email(data.email, verification_link)
    except Exception as e:
        logging.error(f"Failed to send verification email: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to send verification email")

    return {"message": "User registered successfully. Please check your email to verify your account before logging in."}


@router.get("/verify-email")
async def verify_email(token: str):
    # Find user by verification token
    user_response = supabase.table("users").select(
        "*").eq("verification_token", token).execute()
    if not user_response.data or len(user_response.data) == 0:
        raise HTTPException(
            status_code=400, detail="Invalid or expired verification token")

    user = user_response.data[0]

    # Update user to verified
    update_response = supabase.table("users").update({
        "verified": True,
        "verification_token": None
    }).eq("id", user["id"]).execute()

    if update_response.data is None or len(update_response.data) == 0:
        raise HTTPException(status_code=500, detail="Failed to verify email")

    return {"message": "Email verified successfully. You can now log in."}
