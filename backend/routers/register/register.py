from fastapi import FastAPI, HTTPException
from .db import supabase
from model.users import UserRegisterRequest
from .auth import hash_password
from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
async def register_user(data: UserRegisterRequest):
    # Cek apakah email sudah dipakai
    existing = supabase.table("users").select(
        "id").eq("email", data.email).execute()
    if existing.data:
        raise HTTPException(
            status_code=400, detail="Email already registered.")

    hashed_pw = hash_password(data.password)

    response = supabase.table("users").insert({
        "name": data.name,
        "gender": data.gender,
        "date": data.date.isoformat(),
        "email": data.email,
        "password_hash": hashed_pw,
    }).execute()

    if response.data is None or len(response.data) == 0:
        raise HTTPException(status_code=500, detail="Gagal mendaftarkan user")

    return {"message": "User registered successfully"}
