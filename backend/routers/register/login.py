import traceback
from fastapi import HTTPException, APIRouter, Form, Request
from fastapi.responses import JSONResponse
from .db import supabase
from .auth import verify_password
from model.LoginInput import LoginInput

router = APIRouter()


@router.post("/login")
async def login_user(data: LoginInput, request: Request):
    try:
        response = supabase.table("users").select(
            "*").eq("email", data.email).execute()
        user_data = response.data

        if not user_data:
            raise HTTPException(
                status_code=401, detail="Invalid email or password")

        user = user_data[0]

        # Cocokkan password hash
        if not verify_password(data.password, user["password_hash"]):
            raise HTTPException(
                status_code=401, detail="Invalid email or password")

        # Simpan user ke session
        request.session["user"] = {
            "id": user["id"],
            "email": user["email"],
            "name": user.get("name", "")
        }

        return JSONResponse(content={"message": "Login successful"})

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {type(e).__name__} - {e}")
