# Web-Crawling-On-Container

## Solution
- Python의 Flask 사용
  - 프로그램 동적으로 조정
    - server-clinet 구조 사용
    - server가 종료하기 전까지 계속해서 이벤트 수집
  - Crawling은 따로 처리
    - APScheduler
- 수집된 데이터의 변경 사항 파악
  - 원시 데이터의 변경 사항을 반영
  - 어떤 이벤트가 변경되었는지 기준 선정
    - 이름, 날짜 등 조합하여 판단
- Kubernetes 사용
  - Flask
    - ConfigMap
      - default_repeat_time
      - port
      - database
        - ip
        - port
        - database name
  - Database
    - configMap
      - database
    - Secret
      - user, password
    - PV, PVC
      - for persist

## Docker 
### Flask
- Env
  - DB_HOST
  - DB_PORT
  - DB_USER
  - DB_PASSWD
  - DB_DBNAME
  - DEFAULT_REPEAT_TIME
- Build 
  - docker build --no-cache -t zxcasd3004/assignment:flask .
- Start
  - docker run -itd -e DB_HOST={IP} --name flask -p 8080:8080 zxcasd3004/assignment:flask
### MySQL
- Env
  - MYSQL_ROOT_PASSWORD
  - MYSQL_DATABASE
- Build
  - docker build --no-cache -t zxcasd3004/assignment:mysql .
- Start
  - docker run -itd -p 3306:3306 --name mysql  zxcasd3004/assignment:mysql


