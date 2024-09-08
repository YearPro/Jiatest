import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from datetime import datetime
import os

# MLflow 실험 설정 (Experiment 만들기)
mlflow.set_experiment("Iris Classification Experiment")

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

# MLflow로 모델 학습 시작 (Run 시작)
with mlflow.start_run():
    # 하이퍼파라미터 설정
    max_depth = 1
    min_samples_split = 3
    model_dt = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split, random_state=42)
    model_dt.fit(X_train, y_train)

    # 모델 예측 및 성능 평가
    predictions_dt = model_dt.predict(X_test)
    accuracy_dt = accuracy_score(y_test, predictions_dt)
    precision_dt = precision_score(y_test, predictions_dt, average='macro')
    recall_dt = recall_score(y_test, predictions_dt, average='macro')
    f1_dt = f1_score(y_test, predictions_dt, average='macro')

    # 하이퍼파라미터 기록
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("min_samples_split", min_samples_split)

    # 성능 기록
    mlflow.log_param("model_type", "DecisionTree")
    mlflow.log_metric("accuracy", accuracy_dt)
    mlflow.log_metric("precision", precision_dt)
    mlflow.log_metric("recall", recall_dt)
    mlflow.log_metric("f1_score", f1_dt)

    # 현재 날짜와 시간을 기반으로 파일명 생성
    current_time = datetime.now().strftime("%Y%m%d_%H%M")
    model_file_name = f'iris_m_ver_{current_time}.pkl'

    # 모델 파일을 저장할 경로 생성 (현재 디렉토리 + 파일명)
    model_file_path = os.path.join(current_dir, model_file_name)

    # 모델 저장
    joblib.dump(model_dt, model_file_path)

    # 모델을 MLflow에 저장
    mlflow.sklearn.log_model(model_dt, "decision_tree_model")
    
    # 성능 출력
    print(f"모델이 MLflow에 저장되었습니다.")
    print(f"정확도(Accuracy): {accuracy_dt}")
    print(f"정밀도(Precision): {precision_dt}")
    print(f"재현율(Recall): {recall_dt}")
    print(f"F1 스코어: {f1_dt}")
