# 베이스 이미지
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /pbook

# 필요한 패키지 설치
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 어플리케이션 코드 복사
COPY ./app /pbook/app
COPY ./admin /pbook/admin
COPY ./templates /pbook/templates
COPY ./admin_templates /pbook/admin_templates
COPY ./controller /pbook/controller
# 기본 환경 변수 설정
ENV SERVICE_TYPE=app 
ENV PORT=8000 

# 포트 노출 (기본 8000)
EXPOSE ${PORT}

# 서비스 타입에 따라 다른 애플리케이션 경로 사용
CMD if [ "$SERVICE_TYPE" = "admin" ]; \
    then uvicorn admin.main:app --host 0.0.0.0 --port ${PORT}; \
    else uvicorn app.main:app --host 0.0.0.0 --port ${PORT}; \
    fi
