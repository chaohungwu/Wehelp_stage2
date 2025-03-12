#In[0] 
import json
import mysql.connector
import pandas as pd

#連接資料庫config
website_db = mysql.connector.connect(
                                    user="root",
                                    password="12345678",
                                    host="localhost",
                                    database="wehelp_stage2_db",
                                    charset="utf8mb4")

#In[1] 處理json檔案
json_data = open(r'G:\05_wehelp\03_week_work\02_stage2\taipei-day-trip\data\taipei-attractions.json','r')
tp_att_data = json.load(json_data)

#In[2] 處理json檔案

#dict轉dataframe
tp_att_data_list = []
for i in range(len(tp_att_data['result']['results'])):
    tp_att_data_list.append(tp_att_data['result']['results'][i])

tp_att_data_df = pd.DataFrame(tp_att_data_list)
check_word_list=[".jpg",".JPG",".png",".PNG"]

#將多張圖片以list存在df中
for i in range(len(tp_att_data['result']['results'])):#loop所有景點
    # print(tp_att_data_df['file'][i]) #圖片網址

    """
    用http做切分，並跳過第一個字
    """
    img_url_list =[] #圖片list
    i2 = 1
    tp_att_url = tp_att_data_df['file'][i] #景點圖片url
    last_index = 0

    while tp_att_url.find("http",i2) != -1: #loop直到找不到http
        if i2 ==1 :
            if tp_att_url[:tp_att_url.find("http",i2)][-4:] in check_word_list:
                img_url_list.append(tp_att_url[:tp_att_url.find("http",i2)])
            else:
                pass
            last_index = tp_att_url.find("http",i2)
            i2 = tp_att_url.find("http",last_index+1)
        else:
            if tp_att_url[last_index:tp_att_url.find("http",i2)][-4:] in check_word_list:
                img_url_list.append(tp_att_url[last_index:tp_att_url.find("http",i2)])
            else:
                pass
            last_index = tp_att_url.find("http",i2)
            i2 = tp_att_url.find("http",last_index+1)

    tp_att_data_df["file"][i]=img_url_list




#In[3] 存入資料庫中

#所有景點跑一次迴圈依次加入資料庫中
tp_att_data_df = tp_att_data_df.rename(columns={"_id":"id"}) #修改欄位名稱
col = tp_att_data_df.columns

for i in range(len(tp_att_data_df)):

    file_list = tp_att_data_df[col[14]][i]
    file_list_str = ','.join(file_list)

    #所有colums都加入資訊
    cursor = website_db.cursor()
    cursor.execute("insert into taipei_attractions (rate, direction, name, date, longitude, REF_WP, avBegin, langinfo, MRT, SERIAL_NO, RowNumber, CAT, MEMO_TIME, POI, file, idpt, latitude, description, id, avEnd, address) values (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s);", 
                    (str(tp_att_data_df[col[0]][i]), tp_att_data_df[col[1]][i], tp_att_data_df[col[2]][i], tp_att_data_df[col[3]][i], tp_att_data_df[col[4]][i], tp_att_data_df[col[5]][i],
                     tp_att_data_df[col[6]][i], tp_att_data_df[col[7]][i],tp_att_data_df[col[8]][i],tp_att_data_df[col[9]][i],tp_att_data_df[col[10]][i],
                     tp_att_data_df[col[11]][i], tp_att_data_df[col[12]][i], tp_att_data_df[col[13]][i], file_list_str , tp_att_data_df[col[15]][i],
                     tp_att_data_df[col[16]][i], tp_att_data_df[col[17]][i],str(tp_att_data_df[col[18]][i]),tp_att_data_df[col[19]][i],tp_att_data_df[col[20]][i],),)
    website_db.commit()






