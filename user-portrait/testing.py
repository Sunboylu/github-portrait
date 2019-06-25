#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from portrayal.user_profile import user_profile
from crawler.user1 import users1
from ability.test import users
from ability.test_analyze import deal_data
from ability.rank import rank
import time,pymongo

def main(select_user):
    #获取初始数据---USER、User_...
    users1(select_user)
    #开发者开发能力维度值 ---user_3
    users(select_user)
    #维度值处理
    deal_data()
    #排序
    rank()
    #用户画像结果
    user_profile(select_user)

if __name__ == '__main__':
    start =time.perf_counter()
    select_user = "tbroyer"
    main(select_user)
    end = time.perf_counter()
    print(end-start)
    # client = pymongo.MongoClient('localhost', 27017)
    # db = client.local
    # user = db.USER.find()
    # #comment从7
    # for i in range(180,207):
    #     print(i)
    #     print(user[i]["login"])
    #     start = time.perf_counter()
    #     # if user[i]["login"] == "chriscoyier":
    #     #     print(i)
    #     main(user[i]["login"])
    #     end = time.perf_counter()
    #     print(end - start)
#chriscoyier