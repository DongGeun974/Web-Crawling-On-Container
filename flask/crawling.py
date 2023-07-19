import pymysql
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import datetime

# Crawling data from web
# Output:
# ['2023-04-02 15:30:00', 
# '2023-04-02 19:30:00', 
# 'Live score Sunrisers Hyderabad vs Rajasthan Royals at Rajiv Gandhi International Stadium, Hyderabad', 
# 'Sunrisers Hyderabad vs Rajasthan Royals', 
# 'done']
#
def crawl():

    data = []
    
    response = requests.get("https://timesofindia.indiatimes.com/sports/cricket/ipl/schedule")
    soup = BeautifulSoup(response.text, 'html.parser')

    for i in soup.find_all(class_="vevent"):
        data.append([parse_date(i.find(class_='dtstart').text), parse_date(i.find(class_='dtend').text), i.find(class_='description').text, i.find(class_='summary').text, calc_date(parse_date(i.find(class_='dtstart').text), parse_date(i.find(class_='dtend').text))])
    
    return data

# Parse date
def parse_date(date):
    return date.split("T")[0] + " " + date.split("T")[1].split("+")[0] + ":00"


# Calculate date
def calc_date(start, end):
    start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    if int((now - end).seconds) > 0:
        return "done"
    elif int((start - now).seconds) > 0 :
        return "waiting"
    else:
        return "running"


# Check table
# If table is not exist, Create table
def check_table():
    try:
        from Module import config
        connection = pymysql.connect(**config)
        cursor = connection.cursor()

        query = "SHOW TABLES LIKE 'events'"
        cursor.execute(query)

        results = cursor.fetchone()

        if not results:
            query = """
                CREATE TABLE `sport`.`events` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `start_date` DATETIME NOT NULL,
                `end_data` DATETIME NOT NULL,
                `title` VARCHAR(200) NOT NULL,
                `description` VARCHAR(200) NOT NULL,
                `created_at` DATETIME NOT NULL,
                `updated_at` DATETIME NOT NULL,
                `process` VARCHAR(45) NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
                ENGINE = InnoDB
                DEFAULT CHARACTER SET = utf8
                COLLATE = utf8_bin;
            """
            cursor.execute(query)

        cursor.close()
        connection.close()
    except Exception as e:
        print("Exception is in check_table")
        print(e)
        print()
    
    

# Select all data from database
# Output :
# [1, 
# datetime.datetime(2023, 3, 31, 19, 30), 
# datetime.datetime(2023, 3, 31, 23, 30), 
# 'Live score Gujarat Titans vs Chennai Super Kings at Narendra Modi Stadium, Ahmedabad', 
# 'Gujarat Titans vs Chennai Super Kings', 
# datetime.datetime(2023, 7, 19, 1, 21, 53),
# datetime.datetime(2023, 7, 19, 1, 21, 53),
# 'done']
# 
def select_all_data():
    try:
        from Module import config
        connection = pymysql.connect(**config)
        # 커서 생성
        cursor = connection.cursor()

        # 쿼리 실행
        query = "SELECT * FROM events WHERE process NOT IN ('canceled')"
        cursor.execute(query)

        # 결과 가져오기
        results = [list(item) for item in cursor.fetchall()]

        # 커넥션 및 커서 닫기
        cursor.close()
        connection.close()

        return results
    
    except Exception as e:
        print("Exception is in select_all_data")
        print(e)
        print()


# Insert all data from crawling to database
def insert_all_data(data):

    try:
        from Module import config
        connection = pymysql.connect(**config)
        # 커서 생성
        cursor = connection.cursor()

        # 쿼리 실행
        query = """
            INSERT INTO `sport`.`events` (`start_date`, `end_data`, `title`, `description`, `created_at`, `updated_at`, `process`)
            VALUES (%s, %s, %s, %s, now(), now(), %s);
        """
        result = cursor.executemany(query, data)
        connection.commit()

        # 커넥션 및 커서 닫기
        cursor.close()
        connection.close()

    except Exception as e:
        print("Exception is in insert_all_data")
        print(e)
        print()


# Update all data in database
def update_all_data(data):
    try :
        from Module import config
        connection = pymysql.connect(**config)
        # 커서 생성
        cursor = connection.cursor()

        # 쿼리 실행
        query = """
            UPDATE `sport`.`events` SET `updated_at` = now(), `process` = 'canceled' WHERE (`id` = %s);
        """
        result = cursor.executemany(query, data)
        connection.commit()

        # 커넥션 및 커서 닫기
        cursor.close()
        connection.close()

    except Exception as e:
        print("Exception is in update_all_data")
        print(e)
        print()


# Compare crawling data with database data
def compare_data(crawl, database):

    # pre-processing
    for i in range(len(crawl)):
        crawl[i][0] = datetime.strptime(crawl[i][0], '%Y-%m-%d %H:%M:%S')
        crawl[i][1] = datetime.strptime(crawl[i][1], '%Y-%m-%d %H:%M:%S')

    # find same data
    crawl_same = []
    db_same = []

    for i in range(len(crawl)):
        for j in range(len(database)):
            if i not in crawl_same and j not in db_same and crawl[i][0] == database[j][1] and crawl[i][1] == database[j][2] and crawl[i][2] == database[j][3] and crawl[i][3] == database[j][4]:
                crawl_same.append(i)
                db_same.append(j)
                break

    
    # delete same data
    crawl_same.sort(reverse=True)
    db_same.sort(reverse=True)
    for i in crawl_same:
        crawl.pop(i)
    for i in db_same:
        database.pop(i)

    # update
    insert_all_data(crawl)
    db_update = []
    for i in database:
        db_update.append([i[0]])
    update_all_data(db_update)



def task():
    print("Start crawling!!")
    crawl_data = crawl()
    check_table()
    db_data = select_all_data()

    if not db_data:
        insert_all_data(crawl_data)
    else:
        compare_data(crawl_data, db_data)

    print("End crawling!!")