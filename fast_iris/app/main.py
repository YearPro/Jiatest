from fastapi import FastAPI, Form
from starlette.responses import Response
from prometheus_client import Counter, generate_latest
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import os
from typing import List
from fastapi import Request

# FastAPI 인스턴스 생성
app = FastAPI()
REQUEST_COUNT = Counter("request_count", "Total Request Count", ["method", "endpoint"])
# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="../app/templates")


model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'model', 'iris_m_ver_20240908_2306.pkl')
model = joblib.load(model_path)

# Iris 데이터셋 라벨 이름
label_names = ['setosa', 'versicolor', 'virginica']

# 메트릭 수집 미들웨어 추가
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    response = await call_next(request)
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()  # 요청 카운터 증가
    return response

# 메인 페이지 경로
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 예측 경로
@app.post("/predict/", response_class=HTMLResponse)
async def predict(request: Request, sepal_length: float = Form(...), sepal_width: float = Form(...), petal_length: float = Form(...), petal_width: float = Form(...)):
    features = [sepal_length, sepal_width, petal_length, petal_width]
    
    # 예측
    prediction = model.predict([features])
    
    # 예측된 숫자를 라벨 이름으로 변환
    prediction_label = label_names[prediction[0]]
    
    # 결과 반환 (HTML 페이지에 예측 결과 전달)
    return templates.TemplateResponse("index.html", {"request": request, "prediction": prediction_label})

# Prometheus 메트릭 경로 추가
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

# FastAPI 실행 부분 (uvicorn으로 실행해야 함)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)