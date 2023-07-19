from flask import Flask, jsonify
from . import sport
from . import repeat

from crawling import task
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore

import os

# MySQL 접속 설정
config = {
    'host': os.environ['DB_HOST'],
    'port': int(os.environ['DB_PORT']),
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWD'],
    'database': os.environ['DB_DBNAME'],
    'charset':'utf8'
    }

schedule = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
schedule.start()
jobstore = MemoryJobStore()
default_repeat_time = int(os.environ['DEFAULT_REPEAT_TIME'])

schedule.add_job(task, 'interval', seconds=default_repeat_time, id='my_job')
task()

app = Flask(__name__)

app.register_blueprint(sport.blue_sport)
app.register_blueprint(repeat.blue_repeat)

# Default path
@app.route('/')
def main():
    return jsonify({"messege" : "This is Web Crawling On Container"}), 200
