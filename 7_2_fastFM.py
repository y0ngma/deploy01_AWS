# fastFM은 리눅스(우분투추천) 윈도설치불가
############################################
"""# 데이터 모델링

- libFM을 python으로 wrapping한 fastFM 제품사용
- fastFM은 리눅스(우분투추천) 윈도설치불가

## fastFM
- 사용이유
  - 특성 사이의 영향을 주고 받는 상호작용 개념을 계산에 적용하여 처리할 수 잇다(조합, 순서등도 성능을 개선하는데 관여된다)
  - 범주형 변수를 더미(파생)변수로 변환하여 범주간 상호작용성도 계산에 사용할 수 있다
  - 회귀, 분류
  - 행렬 인수분해 머신기능을 탑재하고 있다

1. 알고리즘을 만들고 싶다 -> 1~3 년
  - 언어 : C / C++ 등 랭귀지 + 수학적증명
  - 파이썬래핑 : Cython 사용가능
  - 파이썬 라이브러리 제작
1. 연구기관, 대기업 등 진행
1. 논문

- 제공 알고리즘은 다음과 같다

### ALS : 교대 최소 제곱법
- 장점 : 예측시간빠름, 파라미터수 적다
- 단점 : 규제하면서 학습처리

### SGD : 확률적 경사 하강법
- 장점 : 예측시간빠름, 대규모 데이터를 빠르게 학습가능
- 단점 : 규제, 하이퍼파라미터가 많다

### MCMC : 마로코프 연쇄 몬테카롤로
- Markov Chain Monte Carlo
- 장점 : 하이퍼파라미터 작ㄱ다
- 단점 : 학습속도느림
"""

#pip install fastFM

"""## 가상데이터를 이용하여 기능확인"""

from sklearn.feature_extraction import DictVectorizer
import numpy as np

from fastFM import als
from sklearn.model_selection import learning_curve

# Dictvectorizer => 문자열을 백터화
v = DictVectorizer()

train = [
  { 'user':'1', 'item':'5', 'age':198 },
  { 'user':'2', 'item':'2', 'age':298 },
  { 'user':'3', 'item':'9', 'age':398 },
  { 'user':'4', 'item':'52','age':282 }
]
print(train)

# 데이터를 백터화하여 수치로 표현
X = v.fit_transform( train )
# 수치는 그대로 둔다
# 문자열을 범주형 변수로 취급되어, 총 케이스수만큼 컬럼이 생성
# 0으로 채운뒤에 독립된 값에 1으로 부여식으로 데이터가 변환
# 순서는 무관
# X.toarray()

# y제공 => 평점
# 유저1번은 5.0, 유저2는 1.0, ...
y = np.array( [5.0, 1.0, 2.0, 4.0] )

# 훈련
fm = als.FMRegression( n_iter=1000, init_stdev=0.1
                 , rank=2, l2_reg_w=0.1, l2_reg_V=0.5 )
fm.fit(X, y)

# 예측 : 나이가 24살인데 아이템 10번을 보고 평점을 몇점줄까?
data = {'user':'5', 'item':'10', 'age':24}
fm.predict( v.transform(data) )
