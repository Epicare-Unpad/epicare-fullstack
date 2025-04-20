from fastapi import Form
from fastapi.responses import HTMLResponse
import traceback
from fastapi import HTTPException, APIRouter, Form, Request
from fastapi.responses import JSONResponse
from .db import supabase
from .auth import verify_password
from model.LoginInput import LoginInput

router = APIRouter()


@router.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...), request: Request = None):
    try:
        response = supabase.table("users").select(
            "*").eq("email", email).execute()
        user_data = response.data

        if not user_data:
            raise HTTPException(
                status_code=401, detail="Invalid email or password")

        user = user_data[0]

        # Cocokkan password hash
        if not verify_password(password, user["password_hash"]):
            raise HTTPException(
                status_code=401, detail="Invalid email or password")

        # Simpan user ke session
        if request:
            request.session["user"] = {
                "id": user["id"],
                "email": user["email"],
                "name": user.get("name", "")
            }

        # Return HTMLResponse with script to set sessionStorage and redirect
        return HTMLResponse(f"""
        <html>
            <head><title>Redirecting...</title></head>
            <body>
                <script>
                    sessionStorage.setItem('user', JSON.stringify({{
                        'id': '{user["id"]}',
                        'email': '{user["email"]}',
                        'name': '{user.get("name", "")}'
                    }}));
                    window.location.href = '/frontend/chatbot.html';
                </script>
            </body>
        </html>
        """)

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {type(e).__name__} - {e}")
