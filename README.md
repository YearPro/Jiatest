# Jiatest

# iris_ml 도커파일 --------------------------------------
fastapi dev main.py

# 1. Python 3.10.11 베이스 이미지 사용
FROM python:3.10.11-slim

# 2. Jiatest 디렉토리로 작업 디렉토리 설정
WORKDIR /Jiatest

# 3. requirements.txt 파일 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. 프로젝트 전체 복사 (iris_ml 포함)
COPY . .

# 5. Flask 애플리케이션 실행 (iris_ml 디렉토리의 app.py)
CMD ["python", "iris_ml/app.py"]
---------------------------------------------------------