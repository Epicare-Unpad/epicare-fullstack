from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client
import os
from dotenv import load_dotenv

router = APIRouter()

# Load .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@router.get("/api/articles")
async def get_articles():
    try:
        response = supabase.table("articles").select("*").execute()
        data = response.data
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/api/articles/{article_id}")
async def get_article_detail(article_id: str):  # Ubah dari int ke str
    try:
        print(f"Mencari artikel dengan ID: {article_id}")  # Debugging
        response = supabase.table("articles").select("*").eq("id", article_id).execute()
        print(f"Response dari Supabase: {response.data}")  # Debugging
        data = response.data
        if not data:
            return JSONResponse(status_code=404, content={"error": "Artikel tidak ditemukan"})
        return JSONResponse(content=data[0])
    except Exception as e:
        print(f"Error: {str(e)}")  # Debugging
        return JSONResponse(status_code=500, content={"error": str(e)})
