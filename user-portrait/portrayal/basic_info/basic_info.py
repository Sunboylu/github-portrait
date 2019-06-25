#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pymongo

def infor(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    user = db.ghusers.find_one({'login': select_user})
    user_information = {}
    # print(user['name'])
    user_information["user_name"] = user['name']
    user_information["user_login"] = user['login']
    user_information["user_company"] = user['company']
    num = 0
    for i in user['organizations']:
        temp = i
        if (num > 0):
            user_information["user_organization"].append(temp)
        else:
            user_information["user_organization"] = [temp]
        num = num+1

    #用户建立时间
    start_1 = user['creat_time'].split('-')[0]
    start_2 = user['creat_time'].split('-')[1]
    update_1 = user['update_time'].split('-')[0]
    update_2 = user['update_time'].split('-')[1]
    year = int(update_1)-int(start_1)
    month = int(update_2)-int(start_2)
    temp_time = year*12+month
    user_information["user_time"] = temp_time
    #location
    user_information["location"] = user['location']
    return user_information