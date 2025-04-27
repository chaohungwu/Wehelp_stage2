import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling


# 載入 .env 檔案
load_dotenv()

## 讀取環境變數
db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")

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



class DB_Function:

    def __init__(self):
        pass
    
    def search(self, sql, parameter=None):
        """
        sql:str 欲使用的sql語法
        """
        if parameter: #如果有輸入參數
            connection = pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, parameter)#依據頁數查詢資料
            db_search = cursor.fetchall()
            cursor.close()
            connection.close() # return connection to the pool.

            return db_search
        
        else:
            connection = pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql)#依據頁數查詢資料
            db_search = cursor.fetchall()
            cursor.close()
            connection.close() # return connection to the pool.

            return db_search
    

    def insert(self, sql, parameter):
        """
        parameter:(member_name, member_email, member_password, member_hash_password)
        """
        connection = pool.get_connection()
        cursor = connection.cursor()
        db_sql = "insert into member (member_name, member_email, member_password, member_hash_password) values (%s,%s,%s,%s);"
        cursor.execute(db_sql, parameter)
        connection.commit()
        cursor.close()
        connection.close()








