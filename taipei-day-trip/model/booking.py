import json
from fastapi import *
from fastapi.responses import HTMLResponse, JSONResponse

import mysql.connector
from mysql.connector import pooling

import os
from dotenv import load_dotenv ,find_dotenv
import jwt


load_dotenv()
# # 讀取環境變數
db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")


app=FastAPI()

dbconfig = {
    "database": db_name,
    "user": db_user,
    "password": db_password,
    "host": "localhost",
    # "port": "8080"
	}

pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="wehelp_stage2_DB_pool",
                                                    pool_size=5,
                                                    pool_reset_session=True,
                                                    **dbconfig)


"""
以前端都不可相信來做設計
從前端來的只有id、選擇的時間、價格
再用id去查詢資訊

"""

class booking:
    def booking_db_import(booking_user_id,booking_data):
        # 存入booking資料庫中(存入景點id、user_id、預定時間、)
        connection = pool.get_connection()
        cursor = connection.cursor()

        # 查資料庫，如果已經有預定就取代
        # sql = "SELECT * FROM booking_table WHERE booking_user_id = %s;"
        sql = "select count(*) from booking_table where booking_user_id= %s;"
        cursor.execute(sql,(booking_user_id,))
        db_results = cursor.fetchall()
        cursor.close()
        connection.close()
        print("count",db_results[0][0])

        print("count",db_results[0])


        # 如果有紀錄的話
        if db_results[0][0] != 0:
            connection = pool.get_connection()
            cursor = connection.cursor()
            sql = "update booking_table set booking_att_id = %s ,booking_date = %s ,booking_time=%s ,booking_price=%s where booking_user_id = %s;"
            update_data = (booking_data["attractionId"], booking_data["date"],booking_data["time"], booking_data["price"],booking_user_id)
            print(update_data)
            cursor.execute(sql, update_data)
            connection.commit()
            cursor.close()
            connection.close()

        else:
            connection = pool.get_connection()
            cursor = connection.cursor()
            db_sql = "insert into booking_table (booking_user_id, booking_att_id, booking_date, booking_time, booking_price) values (%s,%s,%s,%s,%s);"
            add_data = (booking_user_id, booking_data["attractionId"], booking_data["date"],booking_data["time"], booking_data["price"])
            cursor.execute(db_sql, add_data)
            connection.commit()
            cursor.close()
            connection.close()


    def build_booking(Authorization,body):
        data = json.loads(body)

        #登入狀態驗證
        Authorization_splite = Authorization.split()
        token = Authorization_splite[1]
        try:
            decoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])
        
        except:
            return JSONResponse(content={"error": True, "message": "未登入系統，拒絕存取"}, status_code=403)

        try:
            # 建立預定
            att_id = data['att_id_select']
            booking_user_id = decoded_jwt['id']
            date_select = data['date_select']
            time_id = data['time_id']

            # 用id獲取景點的資料
            connection = pool.get_connection()
            cursor = connection.cursor()

            # 找出名稱、地址 、照片
            sql = "SELECT name, address, file FROM taipei_attractions WHERE id = %s;"
            cursor.execute(sql,(att_id,))
            db_results = cursor.fetchall()
            cursor.close()
            connection.close()

            # 時間、價格選擇驗證
            if time_id=="1" and date_select!="":
                time = "morning"
                price = 2000
                booking_data = {
                    "attractionId":att_id,
                    "date":date_select,
                    "time":time,
                    "price":price
                    }
                try:
                    booking.booking_db_import(booking_user_id,booking_data)
                    return{"ok": True}
                
                except Exception as e:
                    print(e)

            elif time_id=="2" and date_select!="":
                time = "aftrenoon"
                price = 2500
                booking_data = {
                    "attractionId":att_id,
                    "date":date_select,
                    "time":time,
                    "price":price
                    }
                
                try:
                    booking.booking_db_import(booking_user_id,booking_data)
                    return{"ok": True}
                
                except Exception as e:
                    print(e)

            else:
                return JSONResponse(content={"error": True, "message": "建立失敗，時間輸入不正確"}, status_code=400)

        except:
            raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})



    def booking_db_search(Authorization):
        # 搜尋現有的預定行程(booking)
        #登入狀態驗證
        Authorization_splite = Authorization.split()
        token = Authorization_splite[1]
        try:
            decoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])
        
        except:
            return JSONResponse(content={"error": True, "message": "未登入系統，拒絕存取"}, status_code=403)

        booking_user_id = decoded_jwt['id']

        # 如果沒有預定的話就回傳null，有的話就回傳該筆訂單
        connection = pool.get_connection()
        cursor = connection.cursor()
        sql = "select count(%s) from booking_table where booking_user_id=%s;"
        cursor.execute(sql,(booking_user_id,booking_user_id,))
        db_results = cursor.fetchall()
        cursor.close()
        connection.close()
        # print(db_results[0][0])
        # print(type(db_results[0][0]))

        if db_results[0][0]== 0:
            # print("沒預定")
            return {"data":None}
        
        else:
            connection = pool.get_connection()
            cursor = connection.cursor()
            sql = "SELECT taipei_attractions.id,taipei_attractions.name ,taipei_attractions.address ,taipei_attractions.file , booking_table.booking_date, booking_table.booking_time, booking_table.booking_price, booking_table.booking_user_id FROM taipei_attractions inner join booking_table on booking_table.booking_att_id = taipei_attractions.id where booking_user_id =%s ;"
            cursor.execute(sql,(booking_user_id,))
            db_results = cursor.fetchall()
            cursor.close()
            connection.close()
            # print(db_results)

            booking_user_id = db_results[0][7]
            booking_att_id = db_results[0][0]
            booking_att_name = db_results[0][1]
            booking_att_address = db_results[0][2]
            booking_att_image = db_results[0][3]
            booking_att_image_s = booking_att_image.split(",")
            booking_date = db_results[0][4]
            booking_time = db_results[0][5]
            booking_price = db_results[0][6]

            search_result = {"data":{
                                "attraction":{
                                    "id": booking_att_id,
                                    "name": booking_att_name,
                                    "address": booking_att_address,
                                    "image": booking_att_image_s[0],
                                    },
                                    "date": booking_date,
                                    "time": booking_time,
                                    "price": booking_price
                                }
                            }
            
            return search_result




    def delete_booking_function(Authorization):
        Authorization_splite = Authorization.split()
        token = Authorization_splite[1]
        try:
            decoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])
        except:
            return JSONResponse(content={"error": True, "message": "未登入系統，拒絕存取"}, status_code=403)

        booking_user_id = decoded_jwt['id']

        # 刪除預定
        connection = pool.get_connection()
        cursor = connection.cursor()
        sql = "delete from booking_table WHERE booking_user_id = %s;"
        cursor.execute(sql,(booking_user_id,))
        connection.commit()
        cursor.close()
        connection.close()

        return {"ok":True}





