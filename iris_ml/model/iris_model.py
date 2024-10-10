import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from datetime import datetime
import os

# 현재 파일 위치의 디렉토리 구하기
current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로를 가져옴

# 데이터셋 파일 경로
data_file_path = os.path.join(current_dir, '..', 'data', 'iris_dataset.csv')

# 데이터셋 로드 (CSV 파일을 pandas로 읽기)
iris_data = pd.read_csv(data_file_path)

# 입력 특징과 타겟 값 분리 (데이터프레임의 열을 나눔)
X = iris_data.iloc[:, :-1]  # 특징 (feature) 열
y = iris_data.iloc[:, -1]   # 타겟 (label) 열

# 데이터셋을 학습용과 테스트용으로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 학습
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 현재 날짜와 시간을 기반으로 파일명 생성
current_time = datetime.now().strftime("%Y%m%d_%H%M")
model_file_name = f'iris_m_ver_{current_time}.pkl'

# 모델 파일을 저장할 경로 생성 (현재 디렉토리 + 파일명)
model_file_path = os.path.join(current_dir, model_file_name)

# 모델 저장
joblib.dump(model, model_file_path)

print(f"모델이 저장되었습니다: {model_file_path}")
