from fastapi import *
from typing import Annotated
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse, JSONResponse

import json

import mysql.connector
from mysql.connector import pooling

import jwt
import datetime
from passlib.context import CryptContext
import os
from dotenv import load_dotenv ,find_dotenv

from model.booking import booking as BookingFunction
from model.order import order as OrderFunction





# 載入 .env 檔案
load_dotenv()
# print(os.environ)
# env_path = find_dotenv()
# print(f"找到 .env 檔案: {env_path}")  # 應該會印出 .env 的路徑
# load_dotenv(dotenv_path="/.env")

# # 讀取環境變數
db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")

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


@app.get("/api/attractions")
def attractions(page:str, keyword:str=None):
	"""
	page 要取得的分頁，每頁 12 筆資料(最小值0，必填欄位)
	keyword 用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選
	"""
	
	try:
		#如果有輸入keyword
		if keyword!= None:
			#連到資料庫連接池，查資料
			connection = pool.get_connection()
			cursor = connection.cursor()
			keyword2 = "%"+keyword+"%"
			#查符合的資料有幾筆
			db_count_sql = "SELECT COUNT(*) FROM taipei_attractions WHERE MRT = %s OR name LIKE %s;"
			cursor.execute(db_count_sql,(keyword, keyword2,))#依據頁數查詢資料
			db_count = cursor.fetchall()
			cursor.close()
			connection.close() # return connection to the pool.

			connection = pool.get_connection()
			cursor = connection.cursor()
			sql = "SELECT id ,name, CAT, description, address, direction, MRT, latitude, longitude, file FROM taipei_attractions WHERE MRT = %s OR name LIKE %s Limit %s,%s ;" #從第幾筆到第幾筆
			cursor.execute(sql,(keyword, keyword2,(int(page))*12, 12,))#依據頁數查詢資料
			db_results = cursor.fetchall()
			cursor.close()
			connection.close() # return connection to the pool.


			if db_results==[]:
				results = {}
				results['nextPage'] = None
				results['data'] = db_results
				return results
			else:
				# 將查出的資訊轉成json格式
				rows = []
				results = {}
				for rs in db_results:
					row = {}
					row["id"] = rs[0]
					row["name"] = rs[1]
					row["category"] = rs[2]
					row["description"] = rs[3]
					row["address"] = rs[4]
					row["transport"] = rs[5]
					row["mrt"] = rs[6]
					row["lat"] = rs[7]
					row["lng"] = rs[8]
					img_url_list =[] #圖片list

					if rs[9].find(",") == -1:#只有一張圖片的時候
						img_url_list.append(rs[9])

					else:#有多張圖片的時候

						i2 = 1
						tp_att_url = rs[9] #景點圖片url
						last_index = 0

						while tp_att_url.find(",",i2) != -1: #loop直到找不到http
							if i2 ==1 :
								img_url_list.append(tp_att_url[:tp_att_url.find(",",i2)])
								last_index = tp_att_url.find(",",i2)
								i2 = tp_att_url.find(",",last_index+1)
							else:
								img_url_list.append(tp_att_url[last_index:tp_att_url.find(",",i2)])
								last_index = tp_att_url.find(",",i2)
								i2 = tp_att_url.find(",",last_index+1)

								if tp_att_url.find(",",i2) == -1:
									img_url_list.append(tp_att_url[last_index:])
								else:
									pass
					row["images"] = img_url_list #回傳所有網址


					rows.append(row)

				#看有沒有下一頁
				if int(db_count[0][0]) - ((int(page)+1)*12)>0:
					results['nextPage'] = int(page)+1
				else:
					results['nextPage'] = None
				#景點資料
				results['data'] = rows

				return results


		#沒輸入keyword
		else:
			#連到資料庫連接池，查資料
			connection = pool.get_connection()
			cursor = connection.cursor()
			db_count_sql = "SELECT COUNT(*) FROM taipei_attractions;"
			cursor.execute(db_count_sql)#依據頁數查詢資料
			db_count = cursor.fetchall()
			cursor.close()
			connection.close() # return connection to the pool.

			connection = pool.get_connection()
			cursor = connection.cursor()
			sql = "SELECT id ,name, CAT, description, address, direction, MRT, latitude, longitude, file FROM taipei_attractions Limit %s,%s ;" #從第幾筆到第幾筆
			cursor.execute(sql,((int(page))*12, 12,))#依據頁數查詢資料
			db_results = cursor.fetchall()
			cursor.close()
			connection.close() # return connection to the pool.

			# 將查出的資訊轉成json格式
			rows = []
			results = {}
			for rs in db_results:
				row = {}
				row["id"] = rs[0]
				row["name"] = rs[1]
				row["category"] = rs[2]
				row["description"] = rs[3]
				row["address"] = rs[4]
				row["transport"] = rs[5]
				row["mrt"] = rs[6]
				row["lat"] = rs[7]
				row["lng"] = rs[8]
				img_url_list =[] #圖片list

				if rs[9].find(",") == -1:#只有一張圖片的時候
					img_url_list.append(rs[9])

				else:#有多張圖片的時候

					i2 = 1
					tp_att_url = rs[9] #景點圖片url
					last_index = 0

					while tp_att_url.find(",",i2) != -1: #loop直到找不到http
						if i2 ==1 :
							img_url_list.append(tp_att_url[:tp_att_url.find(",",i2)])
							last_index = tp_att_url.find(",",i2)
							i2 = tp_att_url.find(",",last_index+1)
						else:
							img_url_list.append(tp_att_url[last_index:tp_att_url.find(",",i2)])
							last_index = tp_att_url.find(",",i2)
							i2 = tp_att_url.find(",",last_index+1)

							if tp_att_url.find(",",i2) == -1:
								img_url_list.append(tp_att_url[last_index:])
							else:
								pass
				row["images"] = img_url_list #回傳所有網址
				rows.append(row)

			#看有沒有下一頁
			# print(db_count)
			if db_count[0][0] - ((int(page)+1)*12)>0:
				results['nextPage'] = int(page)+1
			else:
				results['nextPage'] = None
			#景點資料
			results['data'] = rows

			return results
	except:
		raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})



@app.get("/api/attraction/{attractionId}")
def attractions_id(attractionId:Annotated[int ,None]):
	try:
		#連到資料庫連接池，查資料
		connection = pool.get_connection()
		cursor = connection.cursor()

		sql = "SELECT id ,name, CAT, description, address, direction, MRT, latitude, longitude, file FROM taipei_attractions WHERE id = %s;" #從第幾筆到第幾筆
		cursor.execute(sql,(attractionId,))
		db_results = cursor.fetchall()
		cursor.close()
		connection.close() # return connection to the pool.

		# 將查出的資訊轉成json格式
		rows = []
		results = {}
		for rs in db_results:
			row = {}
			row["id"] = rs[0]
			row["name"] = rs[1]
			row["category"] = rs[2]
			row["description"] = rs[3]
			row["address"] = rs[4]
			row["transport"] = rs[5]
			row["mrt"] = rs[6]
			row["lat"] = rs[7]
			row["lng"] = rs[8]
			img_url_list =[] #圖片list
			print(rs[9].find(","))

			if rs[9].find(",") == -1:#只有一張圖片的時候
				img_url_list.append(rs[9])

			else:#有多張圖片的時候

				i2 = 1
				tp_att_url = rs[9] #景點圖片url
				last_index = 0

				while tp_att_url.find(",",i2) != -1: #loop直到找不到http
					if i2 ==1 :
						img_url_list.append(tp_att_url[:tp_att_url.find(",",i2)])
						last_index = tp_att_url.find(",",i2)
						i2 = tp_att_url.find(",",last_index+1)
					else:
						img_url_list.append(tp_att_url[last_index:tp_att_url.find(",",i2)])
						last_index = tp_att_url.find(",",i2)
						i2 = tp_att_url.find(",",last_index+1)

						if tp_att_url.find(",",i2) == -1:
							img_url_list.append(tp_att_url[last_index:])
						else:
							pass
			row["images"] = img_url_list #回傳所有網址
			# rows.append(row)

		#景點資料
		results['data'] = row

		if db_results == []:
			raise HTTPException(status_code=400, detail={"error":True, "message":"景點編號不正確"})
		else:
			return results
	

	except:
		if db_results == []:
			raise HTTPException(status_code=400, detail={"error":True, "message":"景點編號不正確"})
		else:
			raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})

#取得捷運站站點資訊
@app.get("/api/mrts")
def get_mrt_info():
	try:
		#連到資料庫連接池，查資料
		connection = pool.get_connection()
		cursor = connection.cursor()

		# sql = "SELECT COUNT(MRT) MRT FROM taipei_attractions ;" #找所有景點的MRT
		# sql = "SELECT DISTINCT MRT FROM taipei_attractions"
		sql = "select MRT, count(*) as count from taipei_attractions group by MRT order by count desc;"
		cursor.execute(sql)
		db_results = cursor.fetchall()
		cursor.close()
		connection.close() # return connection to the pool.

		all_att_mrt_name_list=[]
		for mrt in db_results:
			if mrt[0] ==None:
				pass
			else:
				all_att_mrt_name_list.append(mrt[0])

		return {"data":all_att_mrt_name_list}

	except Exception as e:
		print(e)
		raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})





"""
註冊一個新的會員
200:註冊成功
202:註冊失敗
500:伺服器內部錯誤
"""
@app.post("/api/user", include_in_schema=False)
async def user(request: Request, body = Body(None)):
	try:
		data = json.loads(body)
		new_user_name = data["name"]
		new_user_email = data["email"]
		new_user_password = data["password"]

		connection = pool.get_connection()
		cursor = connection.cursor()

		#查是否已經有相同mail
		db_sql = "SELECT COUNT(*) FROM member WHERE member_email = %s;"
		cursor.execute(db_sql,(new_user_email,))#依據頁數查詢資料
		search_count = cursor.fetchall()
		cursor.close()
		connection.close()

		count = search_count[0][0]
		
		# 如果沒有找到相同的，就建立
		if count==0:
			print("222")
			print(new_user_password)

			# 密碼做哈希編碼
			try:
				pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
				new_user_password_hash = pwd_context.hash(new_user_password)	
				print("333")
			except Exception as e:
				print(e)

			connection = pool.get_connection()
			cursor = connection.cursor()
			db_sql = "insert into member (member_name, member_email, member_password, member_hash_password) values (%s,%s,%s,%s);"
			add_data = (new_user_name, new_user_email, new_user_password, new_user_password_hash)
			cursor.execute(db_sql, add_data)
			connection.commit()
			cursor.close()
			connection.close()

			return {"ok": True} #註冊成功
		
		else:
			#回傳錯誤訊息
			return JSONResponse(content={"error": True, "message": "系統中已存在該Email"}, status_code=400)
		
	except:
		# 500:伺服器內部錯誤(中斷)
		raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})



"""
取得當前登入的會員資訊
200: 註冊成功
400: 註冊失敗
500: 伺服器內部錯誤
# """
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# secret_key = "12345678"
# algorithm = "HS256"
secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")


@app.get("/api/auth", include_in_schema=False)
# async def decode_user_signin_info(token: str = Depends(oauth2_scheme)):
async def decode_user_signin_info(Authorization: str = Header(None)):
	#解碼
	Authorization_splite = Authorization.split()
	token = Authorization_splite[1]
	try:
		decoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])
		print(decoded_jwt)
		print(type(decoded_jwt))
		print(decoded_jwt['email'])
		user_signin_info={
			"id":decoded_jwt['id'],
			"name":decoded_jwt['name'],
			"email":decoded_jwt['email'],
			}
		return{"data":user_signin_info}
	
	except:
		return{"data":None}



"""
登入會員帳戶，取得token
200: 登入成功，取得有效期為七天的 JWT 加密字串
400: 登入失敗，帳號或密碼錯誤或其他原因
500: 伺服器內部錯誤
"""
@app.put("/api/auth", include_in_schema=False)
async def user_signin(request: Request, body = Body(None)):
	# data = json.loads(body) 
	# print(body)
	# print(type(body))
	# print(data["password"])
	#連到資料庫連接池
	user_email = body['email']
	user_password = body['password']

	connection = pool.get_connection()
	cursor = connection.cursor()

	#搜尋db密碼是不是正確
	db_sql = "select id, member_name, member_email, member_password , member_hash_password from member where member_email = %s;"
	cursor.execute(db_sql,(user_email,))#依據頁數查詢資料
	search_results = cursor.fetchall()
	cursor.close()
	connection.close()


	#1. 確認密碼是不是正確的
	#2. 如果正確，利用JWT去產生回傳提供TOKEN
	#3. 如果失敗就回傳失敗訊息
	try:
		#1.沒查到該email
		if len(search_results)==0:
			return JSONResponse(content={"error": True, "message": "無此email"}, status_code=400)
		
		else:
			# 確認做完哈希的密碼
			pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
			
			var_hash_password = pwd_context.verify(user_password, search_results[0][4])
		

		#2.登入成功，取得token
			try:
				if user_email == search_results[0][2] and var_hash_password:
					payload = {
								'id': search_results[0][0],
								'name': search_results[0][1],
								'email': search_results[0][2],
								"exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=3600*7)
								#'exp': 1743580563  # 過期時間 (Unix timestamp)
								}
					
					#編碼
					encoded_jwt = jwt.encode(payload, secret_key, algorithm=algorithm)
					# print(encoded_jwt)
					return {"token": encoded_jwt}
				
			#3.密碼錯誤
				else:
					return JSONResponse(content={"error": True, "message": "密碼錯誤"}, status_code=400)

			except Exception as e:
				print(e)

	except:
		raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})






@app.post("/api/booking", include_in_schema=False)
async def build_booking_fun(request: Request, Authorization: str = Header(None), body = Body(None)):
	booking_data = BookingFunction.build_booking(Authorization, body)
	return booking_data

@app.get("/api/booking", include_in_schema=False)
async def get_booking_info(Authorization: str = Header(None)):
	search_booking_data = BookingFunction.booking_db_search(Authorization)
	return {"data":search_booking_data}


@app.delete("/api/booking", include_in_schema=False)
async def delete_booking(Authorization: str = Header(None)):
	result_message = BookingFunction.delete_booking_function(Authorization)
	print(result_message)
	return result_message




#連接付款、建立訂單
@app.post("/api/orders", include_in_schema=False)
async def build_orders_fun(request: Request, Authorization: str = Header(None), body = Body(None)):
	order_payment_status = await OrderFunction.order_db_import(Authorization, body)
	return order_payment_status


#取得訂單資訊
@app.get("/api/order/{order_num}", include_in_schema=False)
async def get_order_info(request: Request, order_num: int, Authorization: str = Header(None)):
	order_data_search = await OrderFunction.order_db_search(Authorization, order_num)
	return {"data":order_data_search}



@app.get("/thankyou", include_in_schema=False)
async def thank_page(request: Request, number):
	return FileResponse("./static/ThankPage.html", media_type="text/html")


# Static Pages (Never Modify Code in this Block)以下是靜態文件
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")

app.mount("/", StaticFiles(directory="static" ,html=True))#所有靜態文件資料夾
