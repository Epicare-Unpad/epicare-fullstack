# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from backend.routers.gemini_api import router as gemini_router
from routers.gemini_api import router as gemini_router
# from backend.routers.analisis_gejala_api import router as gejala_router
from routers.analisis_gejala_api import router as gejala_router
# from backend.routers.register.register import router as register_router
from routers.register.register import router as register_router
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
app.include_router(register_router)
