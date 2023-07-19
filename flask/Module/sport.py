from flask import Blueprint, jsonify
import pymysql

blue_sport = Blueprint("sport", __name__, url_prefix="/sport")


## GET method
@blue_sport.route('', methods=["GET"], strict_slashes=False)
def GET_sport(): 
    try :
        from Module import config

        connection = pymysql.connect(**config)

        # 커서 생성
        cursor = connection.cursor()

        # 쿼리 실행
        query = "SELECT * FROM events"
        cursor.execute(query)

        # 결과 가져오기
        results = cursor.fetchall()
    
        # 커넥션 및 커서 닫기
        cursor.close()
        connection.close()

        return jsonify(results), 200
    
    except Exception as e:
        print("Exception is in GET_sport")
        print(e)
        print()
        return jsonify({"messege" : "Internal Server Error"}),  500
    
    

# ## POST method
# @blue_sport.route('', methods=["POST"], strict_slashes=False)
# def POST_sport():
#     return "sport post success\n"