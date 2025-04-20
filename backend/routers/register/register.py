import logging
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import status
from fastapi import Request
from fastapi import FastAPI, HTTPException
from .db import supabase
from model.users import UserRegisterRequest
from .auth import hash_password
from fastapi import APIRouter

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
