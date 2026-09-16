import sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Bookmark Service")

DB_FILE = "bookmarks.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL UNIQUE,
                title TEXT
            )
        """)
        conn.commit()

init_db()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    field_name = errors[0]["loc"][-1] if errors else "body"
    msg = errors[0]["msg"] if errors else "invalid input"
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": f"Invalid field '{field_name}': {msg}", "field": str(field_name)}
    )

class BookmarkCreate(BaseModel):
    url: str = Field(..., min_length=1, max_length=2048)
    title: Optional[str] = Field(None, max_length=255)

@app.post("/bookmarks", status_code=status.HTTP_201_CREATED)
def create_bookmark(payload: BookmarkCreate):
    url = payload.url.strip()
    
    if not url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Field 'url' cannot be blank", "field": "url"}
        )

    if not (url.startswith("http://") or url.startswith("https://")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Field 'url' must start with http:// or https://", "field": "url"}
        )

    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT id, url, title FROM bookmarks WHERE url = ?", (url,))
        existing = cursor.fetchone()
        if existing:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"id": existing["id"], "url": existing["url"], "title": existing["title"], "status": "existing"}
            )

        cursor.execute("INSERT INTO bookmarks (url, title) VALUES (?, ?)", (url, payload.title))
        conn.commit()
        new_id = cursor.lastrowid

        return {"id": new_id, "url": url, "title": payload.title, "status": "created"}

@app.get("/bookmarks", status_code=status.HTTP_200_OK)
def list_bookmarks():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, url, title FROM bookmarks ORDER BY id DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.get("/bookmarks/{bookmark_id}", status_code=status.HTTP_200_OK)
def get_bookmark(bookmark_id: int):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, url, title FROM bookmarks WHERE id = ?", (bookmark_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found")
        return dict(row)

@app.delete("/bookmarks/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(bookmark_id: int):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found")
    return None