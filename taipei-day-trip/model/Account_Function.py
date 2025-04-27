import json
import os
from dotenv import load_dotenv
import jwt
from passlib.context import CryptContext
from model.DB_function import DB_Function
import datetime

# 載入 .env 檔案
load_dotenv()

## 讀取環境變數
secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")

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


class AccountFunction:
    def __init__(self):
        pass

    # 1.註冊
    def Register(self, data):
        DB_function = DB_Function()

        new_user_name = data["name"]
        new_user_email = data["email"]
        new_user_password = data["password"]

		# 查看是否已經有相同mail
        sql = "SELECT COUNT(*) FROM member WHERE member_email = %s;"
        parameter = (new_user_email,)
        count = DB_function.search(sql = sql, parameter=parameter)

		# 如果沒有找到相同的，就建立
        if count[0][0] == 0:
            # 密碼做哈希編碼
            try:
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                new_user_password_hash = pwd_context.hash(new_user_password)	
            except Exception as e:
                print(e)

            sql = "insert into member (member_name, member_email, member_password, member_hash_password) values (%s,%s,%s,%s);"
            add_data = (new_user_name, new_user_email, new_user_password, new_user_password_hash)
            DB_function.insert(sql = sql, parameter=add_data)

            return {"ok": True} #註冊成功
        

        else:
            return {"ok": False}
        

    # 2.驗證登入狀態
    def authenticator(self, Authorization):
        DB_function = DB_Function()

        Authorization_splite = Authorization.split()
        token = Authorization_splite[1]
        decoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])

        user_img_sql = "select member_img from member where member_email = %s;"
        user_img_parameter = (decoded_jwt['email'],)
        user_img = DB_function.search(sql = user_img_sql, parameter=user_img_parameter)

        user_signin_info={
            "id":decoded_jwt['id'],
            "name":decoded_jwt['name'],
            "email":decoded_jwt['email'],
            "img":user_img[0],
            }
        
        return{"data":user_signin_info}
    
    
    # 3.帳號有無存在
    def account_exist(self, data):
        DB_function = DB_Function()
        user_email = data['email']
        user_password = data['password']

		# 查看是否已經有相同mail
        db_sql = "select id, member_name, member_email, member_password , member_hash_password from member where member_email = %s;"
        parameter = (user_email,)
        result = DB_function.search(sql = db_sql, parameter=parameter)

        return result
    

    # 4.帳號登入驗證
    """
    用錯誤代號來顯示登入驗證的錯誤
    # message
    1:無此email
    2.密碼錯誤
    """

    def SingIn_Auth(self, data):
        user_email = data['email']
        user_password = data['password']
        account_search = self.account_exist(data)

        if len(account_search)==0:
            return{"ok":False, "message":1} #無此email
        
        else:
			# 確認做完哈希的密碼
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            var_hash_password = pwd_context.verify(user_password, account_search[0][4])

            try:
                if user_email == account_search[0][2] and var_hash_password:
                    payload = {
                                'id': account_search[0][0],
                                'name': account_search[0][1],
                                'email': account_search[0][2],
                                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=3600*7)
                                #'exp': 1743580563  # 過期時間 (Unix timestamp)
                                }
                    
                    #編碼
                    encoded_jwt = jwt.encode(payload, secret_key, algorithm=algorithm)
                    return {"ok":True,"token": encoded_jwt} #登入成功傳回token
                

            #3.密碼錯誤
                else:
                    return{"ok":False, "message":2} #密碼錯誤

            except Exception as e:
                print(e)





        # print(self.account_exist(data))


        
        


