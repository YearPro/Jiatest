from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional

import sys
# Add the parent directory of `app` to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from controll.search_controller import search_page  #기존 기능
from controll.ela import search_books #엘라스틱

app = FastAPI()

# Use the current directory for templates since app and templates are at the same level
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, query: Optional[str] = None):
    return await search_page(request, query)

# Elasticsearch 검색 기능을 처리하는 경로
@app.get("/es_search", response_class=HTMLResponse)
async def elasticsearch_search(request: Request, query: Optional[str] = None):
    # Elasticsearch 검색
    results = search_books(query)
    return templates.TemplateResponse("index.html", {"request": request, "results": results})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
