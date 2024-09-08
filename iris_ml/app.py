from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)

# 현재 파일 위치의 디렉토리 구하기 (모델 파일 로드)
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'model', 'iris_m_ver_20240908_2306.pkl')

# 미리 학습된 모델 로드
model = joblib.load(model_path)

# Iris 데이터셋 라벨 이름
label_names = ['setosa', 'versicolor', 'virginica']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # 폼에서 입력받은 데이터를 float으로 변환
    # 마지막 값은 타겟값이므로 제외하고 특징값 4개만 사용
    features = [float(x) for x in request.form.values()][:4]
    
    # 예측
    prediction = model.predict([features])
    
    # 예측된 숫자를 라벨 이름으로 변환
    prediction_label = label_names[prediction[0]]
    
    # 결과 반환
    return f'Prediction: {prediction_label}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
