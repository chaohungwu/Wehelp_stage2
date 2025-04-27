import json
from passlib.context import CryptContext
from model.DB_function import DB_Function


class attractionsFunction:
    def __init__(self):
        pass

    # 景點數量搜尋
    def attraction_count_search(self):
        DB_function = DB_Function()
        db_count_sql = "SELECT COUNT(*) FROM taipei_attractions;"
        result = DB_function.search(sql = db_count_sql)
        return result
    
    # 捷運站、景點名稱關鍵字與模糊搜尋
    def attraction_keyword_search_count(self, keyword):
        DB_function = DB_Function()
        fuzzy_keyword = '%{}%'.format(keyword)
        parameter=(keyword,fuzzy_keyword,)
        db_count_sql = "SELECT COUNT(*) FROM taipei_attractions WHERE MRT = %s OR name LIKE %s;"
        result = DB_function.search(sql = db_count_sql, parameter=parameter)
        return result


    # 首頁景點頁數判斷_搜尋該頁(每12個)有哪些景點
    def attraction_page_search(self, page, keyword):
        DB_function = DB_Function()
        db_count_sql = "SELECT id ,name, CAT, description, address, direction, MRT, latitude, longitude, file FROM taipei_attractions WHERE MRT = %s OR name LIKE %s Limit %s,%s ;" #以關鍵字搜尋該些景點在哪一頁

        fuzzy_keyword = '%{}%'.format(keyword)
        parameter = (keyword, fuzzy_keyword,(int(page))*12, 12,)
        result = DB_function.search(sql = db_count_sql, parameter=parameter)
        return result

    def search_result_to_API_Json_format(self, page ,db_results, db_count):
        # 該頁數沒有搜尋到景點的話
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



    def attraction_info_search(self, attractionId):
        DB_function = DB_Function()
        sql = "SELECT id ,name, CAT, description, address, direction, MRT, latitude, longitude, file FROM taipei_attractions WHERE id = %s;" #從第幾筆到第幾筆

        parameter = (attractionId,)
        result = DB_function.search(sql = sql, parameter=parameter)
        return result

    def attraction_info_search_to_API_Json_format(self, att_search_data):
        # 將查出的資訊轉成json格式
        rows = []
        results = {}
        for rs in att_search_data:
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
        return results
    


class MRTFunction:
    def __init__(self):
        pass

    def MRT_info_search(self):
        DB_function = DB_Function()
        sql = "select MRT, count(*) as count from taipei_attractions group by MRT order by count desc;"
        db_results = DB_function.search(sql = sql)

        all_att_mrt_name_list=[]
        for mrt in db_results:
            if mrt[0] ==None:
                pass
            else:
                all_att_mrt_name_list.append(mrt[0])

        return {"data":all_att_mrt_name_list}




