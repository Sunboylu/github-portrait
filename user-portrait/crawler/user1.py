#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import time
import pymongo
from crawler.spider1 import get_following,get_star,get_repos,get_organization,get_friend
from crawler.item import get_repos2
from crawler.get import users
def deal_user(search):
    user = search
    name = user["name"]
    id = user["id"]
    login = user["login"]
    company = user["company"]
    followers_num = user["followers"]
    star = get_star(login)
    repos = get_repos(login)
    organizations = get_organization(login)
    created_at = user["created_at"]
    updated_at = user["updated_at"]
    friends = get_friend(login)
    location = user["location"]
    following = get_following(user["following_url"])
    ghuser = []
    ghuser.append({
                'user_id': id,
                'name' : name,
                'login' : login,
                'company': company,
                'followers_num': followers_num,
                'following': following,
                'star': star,
                'repos' : repos,
                'organizations':organizations,
                'creat_time': created_at,
                'update_time': updated_at,
                'friends' : friends,
                'location' : location
            })
    save(ghuser)

#用户数据处理
def users1(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    #在已有的USER数据库查询
    search = db.USER.find_one({"login": select_user})
    if search is None:
        #查询不到，就api获取，再处理
        users(select_user)
        search2 = db.USER.find_one({"login": select_user})
        deal_user(search2)
        get_repos2(select_user)
    else:
        #查询到，就直接处理
        deal_user(search)
        get_repos2(select_user)

#保存用户数据
def save(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.ghusers.find_one({"login":ghuser[0]["login"]})
    if not result:
         db.ghusers.insert(ghuser)
    else:
        db.ghusers.update({"login":ghuser[0]["login"]},ghuser[0])

if __name__ == '__main__':
    start = time.perf_counter()
    print(start)
    user = users1('scrollie')
    end = time.perf_counter()
    print(end)
    print(end-start)
