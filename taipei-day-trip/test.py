from model.DB_function import DB_Function
from model.attraction import attractionsFunction, MRTFunction
from model.Account_Function import AccountFunction

# from model.order import order as OrderFunction


# aaa = DB_Function()
# sql = "SELECT COUNT(*) FROM taipei_attractions;"
# sql2 = "SELECT COUNT(*) FROM taipei_attractions WHERE MRT = %s;"
# parameter = ("劍潭",)

# num = aaa.search(sql)
# num = aaa.search(sql2,parameter)
# print(num)



# attraction_page_search


# aaa = attractionsFunction()
# # num = aaa.attraction_count_search()
# num = aaa.attraction_page_search(0,"劍潭")
# print(num)


# db_count = attractionsFunction.attraction_keyword_search_count()
# db_results = attractionsFunction.attraction_page_search(page=page, keyword=keyword)

# print(db_count)

# MRTInfoFunction = MRTFunction()
# mrt_info = MRTInfoFunction.MRT_info_search()
# print(mrt_info)


# data = {"name":"gg",
#         "email":'aaa@gmail.com',
#         "password":"gg"}

# accountFunction=AccountFunction()
# result = accountFunction.Register(data)


# data = {"email":"aaa@gmail.com",
#         "password":"aaa"}

# from model.Account_Function import AccountFunction
# accountFunction=AccountFunction()
# result = accountFunction.account_exist(data)
# print(result)

# print(len(result))

# data = {"name":"gg",
#         "email":'aaa@gmail.com',
#         "password":"gg"}
# accountFunction=AccountFunction()
# result = accountFunction.SingIn_Auth(data)




