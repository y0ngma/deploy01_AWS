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
    - git주소, 서버의ip, 도메인은 향후 ip와 연결(호스팅쪽),  
    리눅스 접속 계정 ID 등 설정
    ```json
    {
        "REPO_URL":"https://github.com/y0ngma/deploy01_AWS",
        // 자신의 깃주소 (~.git 빼고)
        "PROJECT_NAME":"deploy01_AWS",
        "REMOTE_HOST":"13.125.237.86",
        // "REMOTE_HOST":"ec2-54-180-116-168.ap-northeast-2.compute.amazonaws.com", //자신의 ip로 대체
        "REMOTE_HOST_SSH":"13.125.237.86",
        // 자신의 ip로 대체
        "REMOTE_USER":"ubuntu"
    }
    ```
1. requirements.txt
    - 본 서비스를 구동하기 위해 사용된 모든 파이썬 패키지를 기술한다.
    ```
    flask==1.0.2
    pandas==0.25.1
    ```

## 구동
- 파이선 3 버전 기반으로 수행
- 운영체계 및 서버 세팅 및 배포, 업데이트 관리 등등을 자동화하는 모듈 => fabric3  
`$ pip3 install fabric3`
- git에 최종소스 반영