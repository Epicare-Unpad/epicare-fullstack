from fastapi import status
from fastapi.responses import HTMLResponse
import traceback
from fastapi import HTTPException, APIRouter, Request
from fastapi.responses import JSONResponse
from .db import supabase
from .auth import verify_password
from model.LoginInput import LoginInput

router = APIRouter()


@router.post("/login")
async def login_user(login_input: LoginInput, request: Request = None):
    try:
        email = login_input.email
        password = login_input.password

        response = supabase.table("users").select(
            "*").eq("email", email).execute()
        user_data = response.data

        if not user_data:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"success": False, "message": "Invalid email or password"})

        user = user_data[0]

        # Cocokkan password hash
        if not verify_password(password, user["password_hash"]):
            return JSONResponse(status_code=status.HTTP_200_OK, content={"success": False, "message": "Invalid email or password"})

        # Simpan user ke session
        if request:
            request.session["user"] = {
                "id": user["id"],
                "email": user["email"],
                "name": user.get("name", "")
            }

        # Return JSON response with user info
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "success": True,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user.get("name", "")
            }
        })

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": f"Unexpected error: {type(e).__name__} - {e}"})
