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
from model.attraction import attractionsFunction, MRTFunction
from model.Account_Function import AccountFunction
from model.user_info_function import user_info



# # 載入 .env 檔案
# load_dotenv()


# # # 讀取環境變數
# db_name = os.getenv("db_name")
# db_user = os.getenv("db_user")
# db_password = os.getenv("db_password")


# dbconfig = {
#     "database": db_name,
#     "user": db_user,
#     "password": db_password,
#     "host": "localhost",
#     # "port": "8080"
# 	}

# pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="wehelp_stage2_DB_pool",
#                                                     pool_size=5,
#                                                     pool_reset_session=True,
#                                                     **dbconfig)

app=FastAPI()

@app.get("/api/attractions")
def attractions(page:str, keyword:str=None):
	"""
	page:str 要取得的分頁，每頁 12 筆資料(最小值0，必填欄位)
	keyword:str 用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選
	"""
	try:
		attPageFunction = attractionsFunction()
		db_count = attPageFunction.attraction_keyword_search_count(keyword=keyword)
		db_results = attPageFunction.attraction_page_search(page=page, keyword=keyword)

		results = attPageFunction.search_result_to_API_Json_format(page=page, db_results=db_results, db_count=db_count)
		return results
	
	except:
		raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})


@app.get("/api/attraction/{attractionId}")
def attractions_id(attractionId:Annotated[int ,None]):
	"""
	attractionId: int 根據id查詢那個景點的資料
	"""
	try:
		attInfoFunction = attractionsFunction()
		db_results = attInfoFunction.attraction_info_search(attractionId)

		if db_results == []:
			raise HTTPException(status_code=400, detail={"error":True, "message":"景點編號不正確"})
		else:
			json_results = attInfoFunction.attraction_info_search_to_API_Json_format(db_results)
			return json_results
	
	except:
		if db_results == []:
			raise HTTPException(status_code=400, detail={"error":True, "message":"景點編號不正確"})
		else:
			raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})


#取得捷運站站點資訊
@app.get("/api/mrts")
def get_mrt_info():
	try:
		MRTInfoFunction = MRTFunction()
		mrt_info = MRTInfoFunction.MRT_info_search()
		return mrt_info

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
		accountFunction=AccountFunction()
		result = accountFunction.Register(data)
		if result['ok']==True:
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
"""
@app.get("/api/auth", include_in_schema=False)
async def decode_user_signin_info(Authorization: str = Header(None)):
	#解碼
	try:
		accountFunction=AccountFunction()
		result = accountFunction.authenticator(Authorization)
		return result

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
	accountFunction=AccountFunction()

	try:
		singin_result = accountFunction.SingIn_Auth(data=body)

		if singin_result['ok']==True:
			return {"token": singin_result['token']} #登入成功傳回token
		else:
			if singin_result['message']==1:
				return JSONResponse(content={"error": True, "message": "無此email"}, status_code=400)
			else:
				return JSONResponse(content={"error": True, "message": "密碼錯誤"}, status_code=400)
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



# 連接付款、建立訂單
@app.post("/api/orders", include_in_schema=False)
async def build_orders_fun(request: Request, Authorization: str = Header(None), body = Body(None)):
	order_payment_status = await OrderFunction.order_db_import(Authorization, body)
	return order_payment_status

# 取得訂單資訊
@app.get("/api/order/{order_num}", include_in_schema=False)
async def get_order_info(request: Request, order_num: int, Authorization: str = Header(None)):
	order_data_search = await OrderFunction.order_db_search(Authorization, order_num)
	return {"data":order_data_search}


# 取得歷史訂單資訊
@app.get("/api/order_history", include_in_schema=False)
async def user_order_history(request: Request, Authorization: str = Header(None)):
	user_order_history = await OrderFunction.user_order_history(Authorization)

	return {"data":user_order_history}




# 感謝訂購畫面
@app.get("/thankyou", include_in_schema=False)
async def thank_page(request: Request, number):
	return FileResponse("./static/ThankPage.html", media_type="text/html")


# 會員中心畫面
@app.get("/user_info", include_in_schema=False)
async def user_center(request: Request, userid):
	return FileResponse("./static/user_info_page.html", media_type="text/html")

# 會員中心上傳照片
@app.post("/api/user_img_upload", include_in_schema=False)
async def user_img_upload(request: Request, Authorization: str = Header(None), body = Body(None)):
	upload_img = user_info.user_img_upload(Authorization, body)
	return upload_img


# 會員中心密碼更新
@app.post("/api/user_password_update", include_in_schema=False)
async def password_update(request: Request, Authorization: str = Header(None), body = Body(None)):
	update_result = user_info.user_password_update(Authorization, body)

	if update_result["ok"]==True:
		return {"ok":True}
	else:
		return {"ok":False,"message":update_result["message"]}





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
