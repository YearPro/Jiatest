# 1. Python 3.10.11 베이스 이미지 사용
FROM python:3.10.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. Python 패키지 설치 (requirements.txt 복사)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 애플리케이션 파일 복사
COPY . .

# 5. Flask 애플리케이션 실행
CMD ["python", "app.py"]
