from fastapi import FastAPI, Request, Query, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware  # starlette에서 가져오기
from typing import Optional
from controller.es import search_books 
import asyncpg
import os

app = FastAPI()
templates = Jinja2Templates(directory="/pbook/templates")

# 세션 비밀 키 설정
SECRET_KEY = "mysecretkey"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# 데이터베이스 연결 설정
DATABASE_URL = "postgresql://postgres:ft1234@13.209.243.157:5432/fairytale"

# 애플리케이션 시작 시 데이터베이스 연결 설정
@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)

# 애플리케이션 종료 시 데이터베이스 연결 해제
@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

# 로그인 확인 유틸리티 함수
def get_current_user(request: Request):
    return request.session.get("user")

# 검색 페이지 (로그인 여부에 따라 헤더 상태 변경)
@app.get("/", response_class=HTMLResponse)
async def search_page(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse("search.html", {"request": request, "user": user})

# 검색 처리 (로그인 필요)
# Elasticsearch 검색 기능을 처리하는 경로
@app.get("/es_search", response_class=HTMLResponse)
async def elasticsearch_search(request: Request, query: Optional[str] = Query(None)):
    if query:
        results = search_books(query)
    else:
        results = []  
    
    return templates.TemplateResponse("search_results.html", {
        "request": request,
        "query": query,
        "results": results  
    })

# 회원가입 페이지 (GET 요청)
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# 회원가입 데이터 처리 (POST 요청)
@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    conn = app.state.db
    try:
        await conn.execute(
            """
            INSERT INTO public.users (username, email, password)
            VALUES ($1, $2, $3)
            """,
            username, email, password
        )
    except asyncpg.UniqueViolationError:
        # email 중복에 대해서만 처리 (username 중복은 허용)
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="회원가입 처리 중 오류가 발생했습니다.")
    
    return templates.TemplateResponse("register_success.html", {
        "request": request,
        "username": username
    })

# 로그인 페이지 (GET 요청)
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("login.html", {"request": request})

# 로그인 데이터 처리 (POST 요청)
@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    conn = app.state.db
    # 사용자 인증
    user = await conn.fetchrow(
        """
        SELECT * FROM public.users WHERE email = $1 AND password = $2
        """,
        email, password
    )
    
    if user:
        # 로그인 성공: 세션에 사용자 정보 저장
        request.session["user"] = {"username": user['username'], "email": user['email']}
        return RedirectResponse(url="/", status_code=302)
    else:
        # 로그인 실패 시 다시 로그인 페이지로 리디렉션 및 오류 메시지 표시
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "이메일 또는 비밀번호가 잘못되었습니다."
        })

# 로그아웃 처리
@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/login", status_code=302)
