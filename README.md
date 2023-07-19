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

## Stack
- OS
  - Ubuntu 20.04
  - Window 10
- Langauge
  - Python 3.10.6
- Tool
  - Visual Studio Code
  - Docker Desktop
  - Docker 24.0.2
  - Kubernetes 1.27.2

## Specification
### Database
- events
  | Column      | Type         | Description       |
  | ---         | ---          | ---              |
  | id          | int          | 아이디           |
  | start_date  | datetime     | 경기 시작 시간    |
  | end_data    | datetime     | 경기 종료 시간    |
  | title       | varchar(200) | 경기 내용         |
  | description | varchar(200) | 경기 참가 팀      |
  | created_at  | datetime     | 데이터 생성 시간  |
  | updated_at  | datetime     | 데이터 수정 시간  |
  | process     | varchar(45)  | 경기 상태        |

### API
  | Method  | URI     | Descrition           |
  | ---     | ---     | ---                  |
  | GET     | /       | 애플리케이션 소개      |
  | GET     | /sport  | 경기 데이터 조회       |
  | GET     | /repeat | 현재 크롤링 주기 출력  |
  | POST    | /repeat | 크롤링 주기 변경       |
  

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
## Kubernetes
### Manifest
- Deployment, Service
  - flask
  - mysql
- ConfigMap
  - default repeat time
  - database host
  - database port
  - database user
  - database name
- Secret
  - database password
- Persistent volumn
- Persistent volumn claim

## How to Start
### Kubernetes
```
git clone https://github.com/DongGeun974/Web-Crawling-On-Container.git
cd Web-Crawling-On-Container/manifest
kubectl apply -f .
```
### Docker
```
git clone https://github.com/DongGeun974/Web-Crawling-On-Container.git
cd Web-Crawling-On-Container
docker build -t zxcasd3004:flask -f flask/Dockerfile .
docker build -t zxcasd3004:mysql -f db/Dockerfile .
docker run -itd -e DB_HOST={HOST_IP} --name flask -p 8080:8080 zxcasd3004:flask
docker run -itd -p 3306:3306 --name mysql zxcasd3004:mysql
```
### Flask
```
curl {HOST_IP}:8080
curl {HOST_IP}:8080/sport
curl {HOST_IP}:8080/repeat
curl -d '{"repeat":10}' -H "Content-Type: application/json" -X POST {HOST_IP}:8080/repeat
```
