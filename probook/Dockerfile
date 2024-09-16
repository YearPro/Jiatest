FROM python:3.10-slim

# 최상위 디렉토리인 JIATEST를 작업 디렉토리로 설정
WORKDIR /JIATEST

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Nginx 설정 파일 복사
COPY nginx.conf /etc/nginx/nginx.conf

# FastAPI 실행 (Uvicorn 사용)
CMD ["uvicorn", "probook.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
