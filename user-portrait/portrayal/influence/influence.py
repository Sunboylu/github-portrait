#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pymongo

def influence(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    user = db.ghusers.find_one({'login': select_user})
    user_influence = {}
    #follower数量
    user_followers = user["followers_num"]
    #参与的组织数量
    temp_organization = user["organizations"]
    user_organizes = len(temp_organization)
    temp = int(0.8 * user_followers + 0.2 * user_organizes)
    return  temp
def friend(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    user = db.ghusers.find_one({'login': select_user})
    temp = user["friends"]
    return temp

#计算每个项目的最近参与度
def join(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    query = {'owner': select_user}
    commit = []
    for item in db.items.find(query):
         global num
         num = 0
         # print(item)
         # print(item['item_name'])
         # print(item['commit'])
         if not item['commit'] is None:
            for i in item['commit']:
                # print(i[0])
                if not i[0] is None:
                    # print(i[0]['login'])
                    temp1 = i[0]['login']
                    # print(temp1)
                    if temp1 == select_user:
                        num = num + 1
            if item["parent_name"] == "null":
                fork_temp = item["full_name"]
            else:
                fork_temp = item["parent_name"]
            temp = (item['item_name'],round(num/len(item['commit']),2),fork_temp)
         else:
             if item["parent_name"] == "null":
                 fork_temp = item["full_name"]
             else:
                 fork_temp = item["parent_name"]
             temp=(item['item_name'],0.0,fork_temp)
         commit.append(temp)

    return commit

# if __name__ == '__main__':
#     print(join('ahocevar'))
#     print(join('alexwohlbruck'))
