import json
from fastapi import *
from fastapi.responses import HTMLResponse, JSONResponse
import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv ,find_dotenv
import jwt
import httpx
from datetime import datetime

load_dotenv()
# 讀取環境變數
db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")

# toppay 參數
TAPPAY_TEST_URL = os.getenv("TAPPAY_TEST_URL")
TAPPAY_PARTNER_KEY = os.getenv("TAPPAY_PARTNER_KEY")
MERCHANT_ID = os.getenv("MERCHANT_ID")


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


class order:

    #用非同步的方法，將從前端收到的prime送到tappay的server
    async def tappay_server_connect(prime: str, price:int):
        headers = {
            "Content-Type": "application/json",
            "x-api-key": TAPPAY_PARTNER_KEY
        }
        
        payload = {
            "prime": prime,
            "partner_key": TAPPAY_PARTNER_KEY,
            "merchant_id": MERCHANT_ID,
            "details": "TapPay Test",
            "amount": price,
            "cardholder": {
                "phone_number": "+886923456789",
                "name": "王小明",
                "email": "LittleMing@Wang.com",
                "zip_code": "100",
                "address": "台北市天龍區芝麻街1號1樓",
                "national_id": "A123456789"
            },
            "remember": True
        }

        print(payload)
        # return payload
    
        async with httpx.AsyncClient() as client:
            response = await client.post(TAPPAY_TEST_URL, headers=headers, json=payload)
            print("付款結果:",response.json())
        # 回傳結果給前端
        return response.json()



    async def order_db_import(Authorization, body):
        """
        1. 解析token看使否有登入
        2. 用使用者帳號查詢booking_table裡的資訊
        3. 將booking_table裡該使用者的資訊建立一分到order_table，原有的booking_table該訂單刪除
        5. 將prime傳到tappay server
        6. 取得付款是否成功
        7. 成功的話存到order_table
        8. 將成功資訊回傳前端
        """
        #從前端送過來的訂單資訊
        data = json.loads(body)
        # print(data)
        # print(type(data))


        #1. 登入狀態驗證
        Authorization_splite = Authorization.split()
        token = Authorization_splite[1]
        try:
            decoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])

        except:
            return JSONResponse(content={"error": True, "message": "未登入系統，拒絕存取"}, status_code=403)


        # 2. 用使用者帳號查詢booking_table裡的資訊
        booking_user_id = decoded_jwt['id'] #使用者帳號id
        currentDateAndTime = datetime.now()
        order_number = "{}{}{}{}{}{}{}{}".format(currentDateAndTime.year,
                                                currentDateAndTime.month,
                                                currentDateAndTime.day,
                                                currentDateAndTime.year,
                                                currentDateAndTime.hour,
                                                currentDateAndTime.minute, 
                                                currentDateAndTime.second,
                                                booking_user_id) #訂單編號，編號格式(訂單日期+購買時間+user_id)
            # print(order_number)


        # 3. 將booking_table裡該使用者的資訊建立一分到order_table，原有的booking_table該訂單刪除
        ##建立order訂單db data
        connection = pool.get_connection()
        cursor = connection.cursor()
        connection = pool.get_connection()
        cursor = connection.cursor()
        sql = "select * from booking_table where booking_user_id=%s;"
        cursor.execute(sql,(booking_user_id,))
        db_results = cursor.fetchall()
        cursor.close()
        connection.close()


        try:
            # 要存到 order table 的資料
            order_user_id = db_results[0][1]
            order_att_id = db_results[0][2]
            order_date = db_results[0][3]
            order_time = db_results[0][4]
            order_price = db_results[0][5]
            order_prime = data['prime']
            order_contact_name = data['order']['contact']['name']
            order_contact_email = data['order']['contact']['email']
            order_contact_phone = data['order']['contact']['phone']
            order_status = 0

            if order_contact_name=="" or order_contact_email=="" or order_contact_phone=='':
                return JSONResponse(content={"error": True, "message": "訂單建立失敗，聯絡資訊輸入不正確"}, status_code=400)
            else:
                pass


            add_data = (order_user_id,
                        order_att_id,
                        order_date,
                        order_time,
                        order_price,
                        order_prime,
                        order_contact_name,
                        order_contact_email,
                        order_contact_phone,
                        order_number,
                        order_status)
            
            connection = pool.get_connection()
            cursor = connection.cursor()
            db_sql = "insert into order_table (order_user_id, order_att_id, order_date, order_time, order_price, order_prime, order_contact_name, order_contact_email, order_contact_phone, order_number, order_status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(db_sql, add_data)
            connection.commit()
            cursor.close()
            connection.close()






        except Exception as e:
            print(e)
            return JSONResponse(content={"error": True, "message": "訂單建立失敗，輸入不正確或其他原因"}, status_code=400)



        # 5. 將prime傳到tappay server
        try:
            tappay_response = await order.tappay_server_connect(data['prime'], data['order']['price'])
            print(tappay_response)


            if tappay_response["status"]==0: #付款成功

                payment_status_data = {
                                        "data": {
                                            "number": order_number,
                                            "payment": {
                                            "status": 1,
                                            "message": "付款成功"
                                                }
                                            }
                                        }
                
                # print('payment_status_data:',payment_status_data) #付款成功訊息

                
                connection = pool.get_connection()
                cursor = connection.cursor()
                update_status_sql= 'update order_table set order_status=%s where order_number=%s'; 
                cursor.execute(update_status_sql, (1, order_number,))
                connection.commit()
                cursor.close()
                connection.close()


                #刪除booking_table的資料
                connection = pool.get_connection()
                cursor = connection.cursor()
                delete_booking_sql= 'delete from booking_table where booking_user_id=%s'; 
                cursor.execute(delete_booking_sql, (booking_user_id,))
                connection.commit()
                cursor.close()
                connection.close()



                return payment_status_data #回傳付款成功
            

            else:
                payment_status_data = {
                                        "data": {
                                            "number": order_number,
                                            "payment": {
                                            "status": 0,
                                            "message": "付款失敗"
                                                }
                                            }
                                        }

                return payment_status_data #回傳付款失敗
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})




    async def order_db_search(Authorization, order_num):
        """
        1. 登入狀態驗證
        2. 查詢訂單資訊
        """

        #1. 登入狀態驗證(這邊要確認登入的帳號和訂單的id是一致的)
        Authorization_splite = Authorization.split()
        token = Authorization_splite[1]
        try:
            decoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])
            print(decoded_jwt)


        except:
            return JSONResponse(content={"error": True, "message": "未登入系統，拒絕存取"}, status_code=403)


        # 2. 查詢訂單資訊
        connection = pool.get_connection()
        cursor = connection.cursor()
        sql = "select * from order_table where order_number=%s;"
        cursor.execute(sql,(order_num,))
        db_results = cursor.fetchall()
        cursor.close()
        connection.close()
        print(db_results[0])

        connection = pool.get_connection()
        cursor = connection.cursor()
        sql = "select * from taipei_attractions where id=%s;"
        cursor.execute(sql,(db_results[0][2],))
        att_search_results = cursor.fetchall()
        cursor.close()
        connection.close()
        # print("訂單：",db_results[0])
        # print("景點資訊：",att_search_results[0])

        # print("jwt:",decoded_jwt["id"])
        # print(type(decoded_jwt["id"]))

        # print("db:",db_results[0][1])
        # print(type(db_results[0][1]))

        
        # 這邊要確認登入的帳號和訂單的id是一致的(預防看別人訂單狀況)
        if str(decoded_jwt["id"]) != str(db_results[0][1]):
            raise HTTPException(status_code=403, detail={"error":True, "message":"未登入該訂單帳號，拒絕存取"})


        else:
            print("aaaa")
            att_image = att_search_results[0][14].split(",")

            responses_data = {
                                "data": {
                                    "number": db_results[0][10],
                                    "price": db_results[0][5],
                                    "trip": {
                                    "attraction": {
                                        "id": att_search_results[0][18],
                                        "name": att_search_results[0][2],
                                        "address": att_search_results[0][20],
                                        "image": att_image[0]
                                    },
                                    "date": db_results[0][3],
                                    "time": db_results[0][4]
                                    },
                                    "contact": {
                                    "name": db_results[0][7],
                                    "email": db_results[0][8],
                                    "phone": db_results[0][9]
                                    },
                                    "status": db_results[0][10]
                                    }
                                }


            return responses_data


