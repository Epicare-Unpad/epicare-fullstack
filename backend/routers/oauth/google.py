from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse, HTMLResponse
from authlib.integrations.starlette_client import OAuth
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

router = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")


@router.get("/auth/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)

    # Log the token for debugging
    print("Token received:", token)

    # Ambil user info langsung dari token
    user = token.get('userinfo')
    if not user:
        return HTMLResponse("<h2>Error: User info not found in token.</h2>", status_code=400)

    # Save user info to Supabase
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{SUPABASE_URL}/rest/v1/users",
            headers={
                "apikey": SUPABASE_API_KEY,
                "Authorization": f"Bearer {SUPABASE_API_KEY}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            },
            json={
                "email": user['email'],
                "name": user['name'],
                "picture": user['picture']
            }
        )

    return HTMLResponse(f"""
    <h2>Login sukses!</h2>
    <p>Halo, {user['name']} ({user['email']})</p>
    <img src="{user['picture']}" width="100" height="100" alt="Foto Profil"
         style="border-radius:50%; border:1px solid #ccc;"
         onerror="this.onerror=null; this.src='https://via.placeholder.com/100';"/>
    """)
