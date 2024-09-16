# 1. Python 3.10.11 베이스 이미지 사용
FROM python:3.10.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /Jiatest/probook

# 3. requirements.txt 파일 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. 프로젝트 전체 복사
COPY . .

# 5. FastAPI 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
