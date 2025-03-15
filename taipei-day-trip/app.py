from fastapi import *
from typing import Annotated
from fastapi.responses import FileResponse
import json
app=FastAPI()

import mysql.connector
from mysql.connector import pooling

dbconfig = {
    "database": "wehelp_stage2_DB",
    "user": "root",
    "password": "12345678",
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
		#有輸入keyword
		if keyword!= None:
			#連到資料庫連接池，查資料
			connection = pool.get_connection()
			cursor = connection.cursor()

			keyword2 = "%"+keyword+"%"

			# print(keyword)
			# print(keyword2)

			db_count_sql = "SELECT COUNT(*) FROM taipei_attractions WHERE name LIKE %s;"
			cursor.execute(db_count_sql,(keyword,))#依據頁數查詢資料
			db_count = cursor.fetchall()
			cursor.close()
			connection.close() # return connection to the pool.
			# print(db_count[0][0])

			connection = pool.get_connection()
			cursor = connection.cursor()
			sql = "SELECT id ,name, CAT, description, address, direction, MRT, latitude, longitude, file FROM taipei_attractions WHERE MRT = %s OR name LIKE %s Limit %s,%s ;" #從第幾筆到第幾筆
			cursor.execute(sql,(keyword, keyword2,(int(page))*12, 12,))#依據頁數查詢資料
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
				if rs[9].find(",") ==-1:
					row["images"] = rs[9]
				else:
					row["images"] = rs[9][:rs[9].find(",")]#只回傳第一個圖片網址
				rows.append(row)

			#看有沒有下一頁
			# print(db_count)
			if db_count[0][0] - (int(page)*12)>0:
				results['nextPage'] = 1
			else:
				results['nextPage'] = 0
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
			# print(db_count[0][0])

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
				row["images"] = rs[9][:rs[9].find(",")]#只回傳第一個圖片網址
				rows.append(row)

			#看有沒有下一頁
			# print(db_count)
			if db_count[0][0] - (int(page)*12)>0:
				results['nextPage'] = 1
			else:
				results['nextPage'] = 0
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
		print(db_results)

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
			row["images"] = rs[9][:rs[9].find(",")]#只回傳第一個圖片網址
			rows.append(row)

		#景點資料
		results['data'] = rows

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
		sql = "select MRT,count(*) as count from taipei_attractions group by MRT order by count desc;"
		cursor.execute(sql,)
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

	except:
		raise HTTPException(status_code=500, detail={"error":True, "message":"伺服器內部錯誤"})



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