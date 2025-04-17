# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware  # Perbaiki di sini
from routers.gemini_api import router as gemini_router
from routers.analisis_gejala_api import router as gejala_router
from routers.register.register import router as register_router
from routers.register.login import router as login_router
from routers.oauth.google import router as google_router
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ganti dengan key yang lebih aman
app.add_middleware(SessionMiddleware, secret_key="random_secret_key")

# Daftarkan router
app.include_router(gemini_router)
app.include_router(gejala_router)
app.include_router(register_router)
app.include_router(login_router)
app.include_router(google_router)
