# FastAPI 애플리케이션을 위한 Python 이미지 사용
FROM python:3.10.11-slim

# 작업 디렉토리 설정
WORKDIR /Jiatest/fast_iris

# requirements.txt 파일 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사 (FastAPI 관련 파일 포함)
COPY . .

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

