from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers.gemini_api import router as gemini_router
from routers.analisis_gejala_api import router as gejala_router
from routers.register.register import router as register_router
from routers.register.login import router as login_router
from routers.oauth.google import router as google_router
from routers.chat_history import router as chat_history_router

app = FastAPI()

# Path ke frontend HTML
app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")
templates = Jinja2Templates(directory="../frontend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session Middleware
app.add_middleware(SessionMiddleware, secret_key="random_secret_key")

# Router
app.include_router(gemini_router)
app.include_router(gejala_router)
app.include_router(register_router)
app.include_router(login_router)
app.include_router(google_router)

app.include_router(chat_history_router)

# Dependency untuk cek login session


def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/frontend/login.html", status_code=302)
    return user


@app.get("/")
async def root(request: Request):
    user = request.session.get("user")
    if user:
        return RedirectResponse(url="/frontend/chatbot.html")
    return RedirectResponse(url="/frontend/login.html")


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/frontend/login.html")


# Contoh route yang diproteksi (misalnya chatbot)
@app.get("/chatbot-protected")
async def chatbot(request: Request, user: dict = Depends(get_current_user)):
    return RedirectResponse(url="/frontend/chatbot.html")
