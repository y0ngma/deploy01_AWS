## 머신러닝 절차
from sklearn.svm import SVC
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
# 5-1. 알고리즘 선정
clf2 = SVC()
# 5-2. 학습/테스트용 데이터 준비
# 단, 스케일러의 생성재료 X_train
X_test_scaled = scaler.transform( X_test )
# 5-3. 학습
clf2.fit( X_train_scaled, y_train )
# 5-4. 예측해라. 한번도 접하지 않은 데이터를
# 5-5. 성능평가를 수행
clf2.score( X_test_scaled, y_test )