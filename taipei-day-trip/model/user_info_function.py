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
from passlib.context import CryptContext

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



class user_info:



    def user_img_upload(Authorization,body):
        #1. 登入狀態驗證(這邊要確認登入的帳號和訂單的id是一致的)
        Authorization_splite = Authorization.split()
        token = Authorization_splite[1]
        try:
            decoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])
            print(decoded_jwt)


        except:
            return JSONResponse(content={"error": True, "message": "未登入系統，拒絕存取"}, status_code=403)

        try:
            user_id = decoded_jwt['id']
            upload_data = body
            print(user_id)
            # print(upload_data['img'])
            # print(type(upload_data['img']))


            # 將圖片存到db中
            connection = pool.get_connection()
            cursor = connection.cursor()
            update_img_sql= "UPDATE member SET member_img=%s WHERE id=%s"; 
            cursor.execute(update_img_sql, (upload_data['img'], user_id,))
            connection.commit()
            cursor.close()
            connection.close()

            return {"ok":True, "img":upload_data}

        except Exception as e:
            print(e)            
            raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})


    def user_password_update(Authorization,body):
        #1. 登入狀態驗證(這邊要確認登入的帳號和訂單的id是一致的)
        Authorization_splite = Authorization.split()
        token = Authorization_splite[1]
        try:
            decoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])
            print(decoded_jwt)


        except:
            return JSONResponse(content={"error": True, "message": "未登入系統，拒絕存取"}, status_code=403)

        try:
            user_id = decoded_jwt['id']
            update_data = body
            print(user_id)
            print(update_data['old_password'])
            # print(type(upload_data['img']))

            """
            1.確定舊密碼要一致
            2.確定新密碼跟舊密碼不一樣
            3.將新密碼做hash
            4.更新新密碼、hash後的值到DB
            """

            connection = pool.get_connection()
            cursor = connection.cursor()
            sql = "select id,member_email,member_password from member where id=%s;"
            cursor.execute(sql,(user_id,))
            db_results = cursor.fetchall()
            cursor.close()
            connection.close()

            print("asdas:",db_results)
            user_old_password =  db_results[0][2]

            if user_old_password == update_data['old_password']:
                if update_data['new_password']!=user_old_password:
                    
                    try:
                        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                        new_user_password_hash = pwd_context.hash(update_data['new_password'])	
                    
                        connection = pool.get_connection()
                        cursor = connection.cursor()
                        update_password_sql= "UPDATE member SET member_password=%s,member_hash_password=%s  WHERE id=%s"; 
                        cursor.execute(update_password_sql, (update_data['new_password'],new_user_password_hash, user_id,))
                        connection.commit()
                        cursor.close()
                        connection.close()
                        return {"ok":True}

                    except Exception as e:
                        print(e)

                
                else:
                    return {"ok":False,"message":"新密碼跟舊密碼一樣"}
            else:
                return {"ok":False,"message":"舊密碼錯誤"}



            return {"ok":True, "img":update_data}

        except Exception as e:
            print(e)            
            raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})


