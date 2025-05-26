from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Enable CORS supaya frontend bisa akses API tanpa masalah
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ganti * dengan domain frontend-mu kalau sudah produksi
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model artikel untuk request dan response
class Article(BaseModel):
    id: Optional[int] = None
    author: str
    title: str
    url: str
    description: str
    content: str

# Data simulasi artikel (biasanya dari database)
articles = [
    {
        "id": 1,
        "author": "Rian Hidayat",
        "title": "Inovasi Teknologi AI di Era Digital",
        "url": "https://example.com/ai-era-digital",
        "description": "Membahas perkembangan terbaru dalam kecerdasan buatan dan dampaknya pada masyarakat modern.",
        "content": "Isi lengkap artikel tentang AI di era digital..."
    }
]

# Fungsi bantu untuk cari artikel berdasarkan ID
def get_article_by_id(article_id: int):
    for article in articles:
        if article["id"] == article_id:
            return article
    return None

# API: List semua artikel
@app.get("/articles", response_model=List[Article])
def read_articles():
    return articles

# API: Tambah artikel baru
@app.post("/articles", response_model=Article)
def create_article(article: Article):
    new_id = max([a["id"] for a in articles]) + 1 if articles else 1
    article.id = new_id
    articles.append(article.dict())
    return article

# API: Update artikel berdasarkan ID
@app.put("/articles/{article_id}", response_model=Article)
def update_article(article_id: int, updated_article: Article):
    article = get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article.update(updated_article.dict(exclude={"id"}))
    return article

# API: Hapus artikel berdasarkan ID
@app.delete("/articles/{article_id}")
def delete_article(article_id: int):
    article = get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    articles.remove(article)
    return {"detail": "Article deleted"}
