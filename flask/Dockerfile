FROM python:3.10.6-slim


WORKDIR /app

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/DongGeun974/Web-Crawling-On-Container.git

WORKDIR /app/Web-Crawling-On-Container/flask

RUN pip install -r requirements.txt

ENV DB_HOST mysql
ENV DB_PORT 3306
ENV DB_USER root
ENV DB_PASSWD 1234
ENV DB_DBNAME sport
ENV DEFAULT_REPEAT_TIME 100

EXPOSE 8080

CMD ["python", "-B", "run.py"]
