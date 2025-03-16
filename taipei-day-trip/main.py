from typing import Annotated
from fastapi import FastAPI, Request,Path, Query, Body
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse,FileResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

from starlette.middleware.sessions import SessionMiddleware

templates = Jinja2Templates(directory="templates")  # 指定模板目錄
app = FastAPI()


@app.get("/api/attractions")
def attractions(request: Request, body = Body(None)):
    """
    page 要取得的分頁，每頁 12 筆資料(最小值0，必填欄位)
    keyword 用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選
    """
    data = json.loads(body)
    result = data



    return{"reslut": result}

    # if "user_id" not in request.session: #沒登入就不回傳留言
    #      return {"error":True}
    
    # else:
    #     cursor = website_db.cursor()
    #     cursor.execute("select member.name, message.content, message.id, member.id from message inner join member on message.member_id = member.id order by message.time desc;")#選所有的留言
    #     myresult = cursor.fetchall()#回傳所有資料庫指令結果

    #     cursor = website_db.cursor()
    #     cursor.execute("select name from member where id= %s;",(name_id,))#
    #     myresult2 = cursor.fetchall()#回傳所有資料庫指令結果

    # return{"message": myresult, "siginin_id":name_id, "siginin_name":myresult2[0][0]}


# @app.get("/api/attractions")
# def attractions_id(request: Request):



# ----------靜態物件----------
app.mount("/", StaticFiles(directory="static" ,html=True))#所有靜態文件資料夾
