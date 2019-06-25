#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
from crawler.header import headers
import pymongo
import time
import os
import urllib.request as req
from gridfs import *

#get commit information
def get_commit(select_user):
    url_basic = 'https://api.github.com/search/commits?q=author:'
    url = url_basic + select_user
    print(url)
    header = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'token  e91fe3b89a7d3145a4b8ed81b9389e6dab539a72',
        'Content-Type': 'application/json',
        'method': 'GET',
        'Accept': 'application/vnd.github.cloak-preview'
    }
    #auth=(email,password)
    response = requests.get(url, headers=header, auth=('###', '###'))
    if (response.status_code != 200):
        print('error: fail to request')
    j = response.json()
    commits = []
    commits.append({
        "login":select_user,
        "count":j['total_count']
    })
    print(commits)
    save_commits(commits)

# #get 头像
def get_png(login,select_url):
    url = select_url
    header = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'token  e91fe3b89a7d3145a4b8ed81b9389e6dab539a72',
        'Content-Type': 'application/json',
        'method': 'GET',
        'Accept': 'application/vnd.github.cloak-preview'
    }
    print(url)
    response = requests.get(url, headers=header, auth=('###', '###'))
    if response.status_code == 200:
        file_path = 'D:\\Anaconda3\\Lib\\site-packages\\django\\bin\\firstsite\\firstapp\\static\\image\\{}.gif'.format(login)
        if not os.path.exists(file_path):
            print('正在下载',login)
            req.urlretrieve(url,file_path)
    img = {
        "login":login,
        "imgage":select_url
    }
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.User_image.find_one({"login": img["login"]})
    if not result:
        db.User_image.insert(img)
    else:
        db.User_image.update({"login": img["login"]}, img)

#get issue 数据
def get_issues(select_user):
    url_basic = 'https://api.github.com/search/issues?q=author:'
    url = url_basic + select_user
    header = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'token  e91fe3b89a7d3145a4b8ed81b9389e6dab539a72',
        'Content-Type': 'application/json',
        'method': 'GET',
        'Accept': 'application/vnd.github.symmetra-preview+json'
    }
    # 通过get请求网页信息
    url1 = url + '&page={}'
    for i in range(1, 20 + 1):
        url2 = url1.format(i)
        print(url2)
        response = requests.get(url2, headers=header, auth=('###', '###'))
        if (response.status_code != 200):
            print('error: fail to request')
            return None
        j = response.json()
        items = j["items"]
        if len(items) > 0:
            for k in items:
                save_issue(k)
        else:
            break


#获得用户的organiz数据
def get_organization(login,select_url):
    url = select_url
    print(url)
    response = requests.get(url,auth=('###', '###'))
    if (response.status_code != 200):
        print('error: fail to request')
        return None
    j = response.json()
    organize = []
    if len(j)>0:
        temp = []
        for i in j:
            temp.append(i["login"])
        organize.append({
            "login": login,
            "orgainze": temp
        })
    else:
        organize.append({
            "login": login,
            "orgainze" : None
        })
    save_organization(organize)


#get user basic information
def users(select_user):
    #访问基础API
    basic_url = 'https://api.github.com/users/'
    url = basic_url + select_user
    print(url)
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    #数据库存在不用继续get
    exist = db.USER.find_one({"login": select_user})
    if exist is None:
        response = requests.get(url,auth=('###', '###'))
        # 检测是否成功
        if (response.status_code != 200):
            print('error: fail to request')
            return None
        # 获取的是json格式的字典对象
        j = response.json()
        save_basic(j)
        #get 项目数据
        get_repos(j["repos_url"])
        #get star项目数据
        get_starrepos(j["login"])
        #get commit数据
        get_commit(j["login"])
        #get issue数据
        get_issues(j["login"])
        #get organize数据
        get_organization(j["login"],j["organizations_url"])
        #get 头像
        get_png(j["login"],j["avatar_url"])

#获得用户的repos数据
def get_repos(select_url):
    url = select_url + '?page={}'
    for i in range(1,20+1):
        header = headers()
        url1 = url.format(i)
        response = requests.get(url1, headers=header,auth=('###', '###'))
        # 检测是否成功
        if (response.status_code != 200):
            print('error: fail to request')
            return None
        j = response.json()
        # 存储repos数据
        if len(j) > 0:
           for k in range(len(j)):
                temp = j[k]
                repos_url = temp["url"]
                print(repos_url)
                repos_response = requests.get(repos_url, headers=header,auth=('###', '###'))
                m = repos_response.json()
                if "full_name" in m.keys():
                    save_repos(m)
        else :
                break

#获得用户的star_repos数据
def get_starrepos(login):
    select_url = 'https://api.github.com/users/' + login + '/starred'
    url = select_url + '?page={}'
    star = []
    repos = []
    for i in range(1,5+1):
        header = headers()
        url1 = url.format(i)
        response = requests.get(url1, headers=header,auth=('###', '###'))
        # 检测是否成功
        if (response.status_code != 200):
            print('error: fail to request')
            return None
        j = response.json()
        # 存储repos数据
        if len(j) > 0:
           for k in range(len(j)):
                temp = j[k]
                repos_url = temp["url"]
                print(repos_url)
                repos_response = requests.get(repos_url, headers=header, auth=('###', '###'))
                m = repos_response.json()
                repos.append(m)
        else :
                break
    star.append({
        "login":login,
        "star_repos":repos
    })
    save_starrepos(star)

#保存用户basic数据
def save_basic(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.USER.find_one({"login":ghuser["login"]})
    if not result:
         db.USER.insert(ghuser)
    else:
        db.USER.update({"login":ghuser["login"]},ghuser)

#保存用户repos数据
def save_repos(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.Repository.find_one({"full_name":ghuser["full_name"]})
    if not result:
         db.Repository.insert(ghuser)
    else:
         db.Repository.update({"full_name":ghuser["full_name"]},ghuser)

#保存用户commmits数据
def save_commits(commits):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.User_commit.find_one({"login":commits[0]["login"]})
    if not result:
         db.User_commit.insert(commits[0])
    else:
         db.User_commit.update({"login":commits[0]["login"]},commits[0])

#保存用户issue数据
def save_issue(issue):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.User_issue.find_one({"id":issue["id"]})
    if not result:
         db.User_issue.insert(issue)
    else:
         db.User_issue.update({"id":issue["id"]},issue)

#保存用户organize数据
def save_organization(organize):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.User_organize.find_one({"login":organize[0]["login"]})
    if not result:
         db.User_organize.insert(organize[0])
    else:
         db.User_organize.update({"login":organize[0]["login"]},organize[0])

#保存用户star_repos数据
def save_starrepos(repos):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.User_starrepos.find_one({"login":repos[0]["login"]})
    if not result:
         db.User_starrepos.insert(repos[0])
    else:
         db.User_starrepos.update({"login":repos[0]["login"]},repos[0])

if __name__ == '__main__':
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    user = db.user_analyze3.find()
    for i in user:
        print(i["login"])
        start = time.perf_counter()
        users(i["login"])
        end = time.perf_counter()
        print(end - start)

    # #单个用户get数据
    # start = time.perf_counter()
    # select_user = 'jakevdp'
    # user =users(select_user)
    # end = time.perf_counter()
    # print(end-start)
