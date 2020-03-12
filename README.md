# deploy01_AWS
deploy 첫배포

## 세팅절차
1. git에 새로운 저장소 생성
1. 로컬 PC에서 aws폴더를 vs code에 오픈
1. terminal 에서 
    - `git clone https://github.com/y0ngma/deploy01_AWS.git`
1. cd deploy01_AWS

## 파일 세팅 (~/aws/deploy01_AWS)
1. fabfile.py, deploy.json 파일을 이동
1. 서버 파일 생성
    - 파일 간단한것 하나 배포확인 후 프로젝트 진행
1. wsgi.py(엔트리포인트), run.py 생성
1. run.py의 앱과 그것을 import 하는 wsgi.py의 코드작성
1. 배보관련 환경변수 파일수정(deploy.json)
