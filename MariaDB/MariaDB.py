## DF -> SQL -> DB
# - Maria 장점
#     - 테이블을 알아서 만들어준다
#     - csv -> DataFrame -> database에 insert(끝)

## 1.업로드 준비하기
# 설치 이 환경 : conda, 범용:pip
# ! conda install pymysql -y
# 파이선에서 mysql계렬에 acess 할수 있는 모둘
import pymysql
# DataFrame에서 디비와 연동하기 위한 sql드라이버
from sqlalchemy import create_engine
# csv -> df
import pandas as pd
# df -> sql
import pandas.io.sql as pSql # io는 input output
# 연결
db_url = 'mysql+pymysql://root:12121212@127.0.0.1/python_db'
# 엔진생성
engine = create_engine( db_url, encoding = 'utf8' )
# 디비 연결
conn = engine.connect()
# 연결 및 자동해제

## 2. 자료를 불러들여서 올리기
# csv -> df 로 읽어서 변환
df1 = pd.read_csv('./raws/gu.csv')
with engine.connect() as conn:
    # 삽입
    # name 테이블명
    # if_exists: 기존데이터 있으면 덮어쓸것인지 추가할건지
    # index: 인덱스
    df1.to_sql( name ='tbl_areas', con=conn, if_exists='replace', index=False)
df2 = pd.read_csv('./raws/gps.csv')
with engine.connect() as conn:
    df2.to_sql( name ='tbl_gpses', con=conn, if_exists='replace', index=False)
    