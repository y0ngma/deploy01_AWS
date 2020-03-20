## 주제
- 웹기반 머신러닝을 활용하여 언어감지 기능을 제공하는 서비스

### 프로젝트구조
```py
/
L run.py        # entry point : 시작점
L read.me       # 설명파일
L service       
    L start.py  # 플라스크 라우팅, 서버설정
    L ml
        L __init__.py                # 머신러닝 모듈작동
        L clf_labels.json            # 분류의 답을가진파일
        L clf_model_yyyymmddhhmm.model  # 학습된 SVC
    L static            # 정적파일(*.js,*.css,리소스등)
    L templates         # 랜더링할 html파일위치
        L index.html    # 서비스 메인화면
```
---
### jQuery
    1. 요소(element)를 찾는다
    1. 그 요소에 이벤트를 준다. or 요소를 조작한다.
    1. 기타 통신처리(ajax)
- 크게 두가지로 나뉜다.
    - 통신
    - 돔조작
        - 찾기
            - 순서:id-클래스-부모자식관계-자식서열-특성속성
        - 이벤트 주기
        - 조작

### geoJson
- opinet.co.kr 에서 읍면동 까지 나누는 지도 참고
1. geoJson => 반정형
1. 디비오픈
1. 폴리곤 갯수만큼 반복
    - 행정구역별 (폴리곤단위) 한줄식 읽어서 (파일처리)
    - 읽은 데이터 한개는 json 형식이므로, json.load()
    - json.load() 자료구조를 그대로 유지
    - => gps, 기타 정보를 인덱싱 처리 가능
    - => df 구성 => db에 insert
        - 다만 시군별로 테이블 나눠서 넣기
        - 너무 느림 
1. 디비 닫기
---

## MariaDB setup
1. 다운로드
    ```py
    https://downloads.mariadb.org/mariadb/10.4.12/ # 최신 바로전 버전

    https://downloads.mariadb.org/interstitial/mariadb-10.4.12/winx64-packages/mariadb-10.4.12-winx64.msi/from/http%3A//mirror.terrahost.no/mariadb/ # MSI 64버전
    ```
    1. 비번설정화면에서 8자리 이상해야 나중에 AWS 에 연동시 동일하게 가능
        - [x] enable access from remote machines for 'root' user
        - [x] use UTF-8
    1. 나머지는 체크변동없이 설치완료시킴

1. Mysql client(Maria DB)
    ```bash
    # 비번입력후
    create database python_db;
    show databases;
    # 생성 확인후 exit로 나가기 
    ```

1. DF -> SQL -> DB
    - Maria 장점
        - 테이블을 알아서 만들어준다
        - csv -> DataFrame -> database에 insert(끝)
    1. 업로드 준비하기
        ```py 
        # 설치 이 환경 : conda, 범용:pip
        ! conda install pymysql -y
        # 파이선에서 mysql계렬에 acess 할수 있는 모둘
        import pymysql
        # DataFrame에서 디비와 연동하기 위한 sql드라이버
        from sqlalchemy import create_engine
        # csv -> df
        import pandas as pd
        # df -> sql
        import pandas.io.sql as pSql # io는 input output
        # 연결
        db_url = 'mysql+pymysql://root:11111111@127.0.0.1/python_db'
        # 엔진생성
        engine = create_engine( db_url, encoding = 'utf8' )
        # 디비 연결
        conn = engine.connect()
        # 연결 및 자동해제
        ```
    1. 자료를 불러들여서 올리기
        ```py
        # 1. csv -> df 로 읽어서 변환
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
        ```

1. HeidiSQL
    1. 세션이름 local
    1. 암호입력 11111111
    1. 데이터베이스 : python_db 드롭다운 후 선택
    1. 저장 후 열기
        - DB삭제후 복원해보기
            - python_db 우클릭해서 SQL로 내보내기
            - 파일에 SQL 파일 불러오기
        - DB 에 넣기 
            - 최상단 query텝
            ```sql
                -- 용산구의 행정구역 경계 gps를 가져와라
                SELECT *  FROM tbl_gps WHERE gu_id = '1';
                -- 다음과 같은 명령문임
                SELECT *  FROM tbl_gps 
                WHERE gu_id = (
                    SELECT gu_id FROM tbl_areas WHERE gu ='용산구'
                    );
            ```

---

## AWS setup
### 서버 프리티어 세부설정 : 추가과금 방지하기
- **상단 서비스텝 클릭**
- @ 컴퓨팅
    - EC2
        - 인스턴스 시작
        - 1단계: 
            1. 총 1~7단계인데 좌측 `프리티어` 체크
            1. Ubuntu Server 18.04 LTS 64비트
        - 2단계:
            - 검토 및 시작
        - 7단계:시작(프리티어는 단계3~6생략됨)
            - 새키페어 생성
            - 시작
        - 인스턴스보기
            - Name에 서버이름을 flask_svr 등으로 적기
            - pending -> running 확인
            - IPv4 퍼블릭 IP 가 내 IP 주소
    - https://kr.godaddy.com/에서 필요시 도메인 구입 가능 (~xyz주소이름)

- @ 데이터베이스
    - RDS
        - (기존인터페이스로 전환)
        - 1/3단계
            1. 하단 프리티어 체크 후 MariaDB 선택
        - 2/3단계
            1. DB인스턴스 클래스 드롭다운메뉴에 db.t2(t2는 무료라는뜻)확인
            2. 스토리지 자동 조정 활성화 체크해제(과금방지)
            3. 인스턴스 식별자
                - python_db
            4. 마스터 사용자 이름
                - root(보안유의)
            5. 암호입력
        - 3/3단계
            1. 퍼블릭엑세스 가능성
                - 예
            2. 데이터베이스이름
                - python_db
            3. 백업보전 기간 
                - 0일
            4. 스냅샷 태그복사 
                - 해제
            5. 확장모니터링
                - 사용안함
            6. 마이너 버전 자동 업그레이드 
                - 사용 안 함
            7. 삭제 방지
                - 비활성
    - 데이터베이스 삭제하는법
        - 우클릭 `상태 - 종료(terminate)`
---

## HeidiSQL - AWS 연동
### HeidiSQL에 연동할 세션추가
- 파일 밑의 코드접속 아이콘 (세션관리자)
1. 신규 - aws
1. 호스트명 : 엔드포인트 복사 붙여넣기
    - RDS의 데이터베이스 연결&보안에 있다
1. 사용자   :root
1. 암호     :8자리
1. 데이터베이스 드롭다운 메뉴클릭(안될시 인바운드 막힌것)
    - python_db 선택
    - 안될시
        - aws 서버의 보안에서 퍼블릭엑세스 가능성 확인
        - inbound rules의 Source에 적힌 IP만 접속허용이다.
        - Edit inbound rules 에서 0.0.0.0/32 추가(anywhere)       
1. 저장-열기

### putty setup
- AWS의 EC2생성시 키페어.pem을 다운로드
1. putty 프로그램 다운로드
    - https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
    1. putty.exe (the SSH and Telnet client itself)
    1. puttygen.exe (a RSA and DSA key generation utility)
        - 위 두개를 64 bit 다운로드

1. puttygen 실행
    - 윈도우에서 실행하므로 필요한 ppk 변환기
    1. Load 
        1. 모든확장자 
        1. 자신의 .pem 선택 
    1. Save private key
        1. passphrase 경고창 뜨면 예
        1. 동일한 이름으로 .ppk 로 저장

1. putty 실행
    - Ubuntu 열어보기
    1. 첫화면Session에서
        1. Host Name : ubuntu@자신의 퍼블릭DNS(IPv4) IP
        2. `Saved Session`에 aws적고 Save 클릭
    1. SSH
        1. Auth
            1. browse 본인 ppk 파일 선택
    2. Window
        1. Appearance - font size 설정
    3. 다시 Session 에서
        1. aws Save 눌러서 SSH 설정 저장
        2. Open 후 실행확인
    4. putty 재 시작시 
        1. 저장된 aws 를 Load 
        1. Open

### ubuntu
- 우분투 실행창에서 경로 확인해보기
```py
ubuntu@ip-172-31-46-157:~$ cd ..
ubuntu@ip-172-31-46-157:/home$ cd ..
ubuntu@ip-172-31-46-157:/$ ls
bin   home            lib64       opt   sbin  tmp      vmlinuz.old
boot  initrd.img      lost+found  proc  snap  usr
dev   initrd.img.old  media       root  srv   var
etc   lib             mnt         run   sys   vmlinuz
ubuntu@ip-172-31-46-157:/$ cd /home/ubuntu # 처음 시작위치
ubuntu@ip-172-31-46-157:~$ ls
ubuntu@ip-172-31-46-157:~$
```






