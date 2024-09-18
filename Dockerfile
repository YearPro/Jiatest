FROM python:3.11-slim

WORKDIR /pbook

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app /pbook/app
COPY ./templates /pbook/templates

EXPOSE 8000

ENV PORT 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
