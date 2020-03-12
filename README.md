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
        // 자신의 깃주소 (~.git 빼고)
        "REPO_URL":"https://github.com/y0ngma/deploy01_AWS",
        // 원하는 프로젝트명
        "PROJECT_NAME":"deploy01_AWS",
        //자신의 DNS로 대체
        "REMOTE_HOST":"ec2-13-125-237-86.ap-northeast-2.compute.amazonaws.com", 
        // 자신의 ip로 대체
        "REMOTE_HOST_SSH":"13.125.237.86",
        "REMOTE_USER":"ubuntu"
    }
    ```
1. requirements.txt
    - 본 서비스를 구동하기 위해 사용된 모든 파이썬 패키지를 기술한다.
    ```
    flask==1.0.2
    ```

## 구동
- 파이선 3 버전 기반으로 수행
- 운영체계 및 서버 세팅 및 배포, 업데이트 관리 등등을 자동화하는 모듈 => fabric3  
    `$ pip3 install fabric3`
- git에 최종소스 반영
- `$ fab new_server`
    - 중간에 y, git login 등이 나올수있다
- 브라우저 13.125.237.86 접속

## 접속로그 확인 (리눅스에서 확인)
- 오류를 확인 가능
    ```py
    # ubuntu에서
    cd deploy01_AWS # 으로 이동
    tail -f /var/apache2/access.log 
    # 로그확인:port80으로 접속자체가 안되어 아무 기록이 없음
    # inbound rule에서 허용하도록 rule 추가하기
    ```
- 인스턴스 정보판에서 
    - 보안그룹의 launch-wizard-1
        - Edit inbound rules
        1. Inbound rule 1
            - Type : SSH
                - Port range    : 22 (자동)
            - Source type       : anywhere
                - Source        : 0.0.0.0/0, ::/0(자동)
        1. Inbound rule 2 
            - Type : HTTP 
                - Port range    : 80 (자동)
            - Source type       : anywhere                
                - Source        : 0.0.0.0/0(자동)
            - Description : flask server

## 잘 안될때
- 소스코드상에 파일명, 설정값등이 서로 물려 있으므로 오타가 없아야함
- 깃에 그러한 최종 소스가 모두 반영되어야함
- 리눅스에서 기존의 흔적을 모두 제거
    ```py  
    다음경로로 이동     : /home/ubuntu
    # deploy.json의 "PROJECT_NAME"이 프로젝트명이다
    프로젝트삭제        : rm -r -f deploy01_AWS
    숨김파일까지 다확인 : ls -a
    모든가상환경삭제    : rm -r -f .virtualenvs
    로컬 PC에서 fab설치 : fab
    ```