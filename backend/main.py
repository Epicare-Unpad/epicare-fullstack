# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gemini_api import router as gemini_router
from analisis_gejala_api import router as gejala_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Daftarkan router
app.include_router(gemini_router)
app.include_router(gejala_router)
