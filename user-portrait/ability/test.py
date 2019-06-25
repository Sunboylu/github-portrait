#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
from crawler.header import headers
import pymongo
import time
#贡献度、收集commit次数
def commit(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    user = db.User_commit.find_one({'login': select_user})
    total_count = user['count']
    return total_count

#活跃度、收集issues次数
def issues(select_user):
    url_basic = 'https://api.github.com/search/issues?q=author:'
    url = url_basic + select_user

    header = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'token  e91fe3b89a7d3145a4b8ed81b9389e6dab539a72',
        'Content-Type': 'application/json',
        'method': 'GET',
        'Accept': 'application/vnd.github.symmetra-preview+json'
    }
    response = requests.get(url, headers=header, auth=('ljj_sunboy@126.com', 'lwdf34698'))
    if (response.status_code != 200):
        print('error: fail to request')
    j = response.json()
    total_count = j['total_count']
    return total_count

#获得用户的organiz数据
def deal_organization_api(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    temp = db.User_organize.find_one({'login': select_user})
    total_count = 0
    if not temp['orgainze'] is None:
        total_count = len(temp['orgainze'])
    return total_count

def users(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    j = db.USER.find_one({'login': select_user})
    users = []
    #用户建立时间
    start_1 = j["created_at"].split('-')[0]
    start_2 = j["created_at"].split('-')[1]
    update_1 = j["updated_at"].split('-')[0]
    update_2 = j["updated_at"].split('-')[1]
    year = int(update_1)-int(start_1)
    month = int(update_2)-int(start_2)
    temp_time = year*12+month

    users.append({
        'name': j["name"],
        'login': j["login"],
        'type': j["type"],
        'company': j["company"],
        'location': j["location"],
        'organizations': deal_organization_api(select_user),
        'followers': j["followers"],
        'public_repos': j["public_repos"],
        'num_languages': deal_repos_api(select_user),
        'commits': commit(select_user),
        'issues':issues(select_user),
        'time': temp_time
    })
    save(users)
    return users

#获得用户的repos数据
def deal_repos_api(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    repos = db.Repository.find({"owner.login": select_user})
    message = []
    for pro in repos:
        message.append([pro["name"], pro["language"], pro["forks"], pro["subscribers_count"], pro["stargazers_count"]])
    return message


def repos(message):
    #每个语言的项目
    user_language={}
    for i in message:
        #i[0]项目名称，i[1]项目语言
        if  not i[1] is None:
            if (i[1] in user_language):
                user_language[i[1]].append(i[0])
            else:
                user_language[i[1]] = [i[1]]
    return len(user_language)

#保存用户数据
def save(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.user_3.find_one({"login":ghuser[0]["login"]})
    if not result:
         db.user_3.insert(ghuser)
    else:
        db.user_3.update({"login":ghuser[0]["login"]},ghuser[0])

if __name__ == '__main__':

    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    user = db.USER.find()
    for i in user:
        print(i["login"])
        start = time.perf_counter()
        users(i["login"])
        end = time.perf_counter()
        print(end - start)
    # select_user = 'ruanyf'
    # user =users(select_user)
    # save(user)
