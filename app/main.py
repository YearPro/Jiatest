from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory="/pbook/templates")

# 검색 페이지
@app.get("/", response_class=HTMLResponse)
async def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

# 검색 처리
@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Query(None)):
    results = query if query else ""
    return templates.TemplateResponse("search_results.html", {
        "request": request,
        "query": query,
        "results": results
    })


