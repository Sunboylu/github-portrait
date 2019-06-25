#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
import pymongo
from crawler.header import headers
import time
# #项目贡献者数据收集
# def deal_contributor_api(select_url):
#     url = select_url + '?page={}'
#     contributor = []
#     for i in range(1, 20 + 1):
#         header = headers()
#         url1 = url.format(i)
#         # print(url1)
#         response = requests.get(url1,headers=header,auth=('###', '###'))
#         if (response.status_code != 200):
#            print('contributor error: fail to request')
#            return None
#         j = response.json()
#         if len(j) > 0:
#             for k in range(len(j)):
#                 pro = j[k]
#                 temp =(pro["login"],pro["contributions"])
#                 contributor.append(temp)
#         else:
#             break
#     return contributor
#
# #项目commit数据收集
# def deal_commit_api(select_api):
#     url = select_api + '?page={}'
#     commit = []
#     for i in range(1, 10 + 1):
#         header = headers()
#         url1 = url.format(i)
#         print(url1)
#         response = requests.get(url1, headers=header,auth=('###', '###'))
#         if (response.status_code != 200):
#             print('commit error: fail to request')
#             return None
#         j = response.json()
#         if len(j) > 0:
#             for k in range(len(j)):
#                 if len(j)>0:
#                     pro = j[k]
#                     temp = (pro["committer"],pro["commit"]["message"])
#                     commit.append(temp)
#         else:
#             break
#     return commit
# #项目content数据收集
# def deal_content_api(select_api):
#     url = select_api
#     header = headers()
#     # print(url)
#     response = requests.get(url,headers=header,auth=('###', '###'))
#     if (response.status_code != 200):
#         print('content error: fail to request')
#         return None
#     j = response.json()
#     content = []
#     for i in range(len(j)):
#         pro = j[i]
#         temp = (pro["name"],pro["size"])
#         content.append(temp)
#     return content

#项目数据收集
def get_repos2(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    repos = db.Repository.find({"owner.login": select_user})
    for j in repos:
        ghitem = []
        item_name = j["name"]
        full_name = j["full_name"]
        owner = j["owner"]["login"]
        description = j["description"]
        language = j["language"]
        size = j["size"]
        watchers_count = j["watchers_count"]
        forks_count = j["forks_count"]
        if 'parent' in j.keys():
            parent_name = j["parent"]["name"]
            parent_fork = j["parent"]["forks_count"]
        else:
            parent_name = "null"
            parent_fork = "null"
        updated_time = j["updated_at"]

        # contributors = deal_contributor_api(j["contributors_url"])
        # commit = deal_commit_api(j["commits_url"].split("{")[0])
        # content = deal_content_api(j["contents_url"].split("{")[0][:-1])

        ghitem.append({
        'item_name': item_name,
        'full_name': full_name,
        'owner': owner,
        'description': description,
        'language': language,
        'size': size,
        'watchers_count': watchers_count,
        'forks_count': forks_count,
        'parent_name': parent_name,
        'parent_fork': parent_fork,
        'updated_time': updated_time
        # 'contributors': contributors,
        # 'commit' : commit,
        # 'content' : content
        })
        save(ghitem)

#保存用户的项目数据
def save(ghitem):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.items.find_one({"full_name":ghitem[0]["full_name"]})
    if not result:
        db.items.insert(ghitem)
    else:
        db.items.update({"full_name":ghitem[0]["full_name"]},ghitem[0])
def get_blog(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    user = db.USER.find({"login": select_user})
    for j in user:
        ghuser = []
        login = j["login"]
        blog = j["blog"]
        ghuser.append({
        'login':login,
        'blog': blog
        })
        save_blog(ghuser)
#保存用户的项目数据
def save_blog(ghitem):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.blog.find_one({"login":ghitem[0]["login"]})
    if not result:
        db.blog.insert(ghitem)
    else:
        db.blog.update({"login":ghitem[0]["login"]},ghitem[0])
if __name__ == '__main__':
    # select_user = 'calvinmetcalf'
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    user = db.USER.find()
    for i in range(0, 207):
        print(i)
        print(user[i]["login"])
        start = time.perf_counter()
        # if user[i]["login"] == "chriscoyier":
        #     print(i)
        get_blog(user[i]["login"])
        end = time.perf_counter()
        print(end - start)
