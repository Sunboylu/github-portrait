#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pymongo
import requests
from portrayal.repos.repos import repos,good_language
from portrayal.basic_info.basic_info import infor
from portrayal.influence.influence import influence,join,friend
from portrayal.interest.interest import repo_des_label
from portrayal.interest.tag import deal_label1

#get commit次数
def commit(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    user = db.User_commit.find_one({'login': select_user})
    total_count = user['count']
    return total_count

def user_profile(select_user):
    #code信息
    code = repos(select_user)
    #擅长的语言
    good_lang = good_language(select_user)
    #基础信息
    information = infor(select_user)
    #影响力
    user_influence = influence(select_user)
    #项目关键词
    # repo_lable = repo_des_label(select_user)
    #项目参与度
    # repo_join = join(select_user)
    #friends
    friends = friend(select_user)
    #commit次数
    commits = commit(select_user)
    # temp = []
    # #所有各个项目的关键词和参与度
    # for x in repo_join:
    #     for y in repo_lable:
    #         if y[0] == x[0]:
    #             temp1 = (x[0],x[1],x[2],y[1])
    #             # print(temp1)
    #             temp.append(temp1)
    #主题词
    # 项目关键词
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    user = db.ghusers.find_one({'login': select_user})
    user2 = db.user_analyze3.find_one({'login': select_user})
    doc_complete = []
    # 整合文档数据
    for i in user['repos']:
        repos_des = i[1]
        # print(star_des)
        if not repos_des is None:
            doc_complete.append(repos_des)
    if doc_complete == [] or doc_complete == ['']:
        repo_lable1 = []
    else:
        repo_lable1 = deal_label1(doc_complete)

    # star项目的主题词
    doc_complete1 = []
    user1 = db.ghusers.find_one({'login': select_user})
    # 整合文档数据
    for i in user1['star']:
        star_des = i[2]
        # print(star_des)
        if not star_des is None:
            doc_complete1.append(star_des)
    if doc_complete1 == []:
        star_repo = []
    else:
        star_repo = deal_label1(doc_complete1)

    vital_lable = []
    for i in repo_lable1:
        for j in star_repo:
            if i == j:
                vital_lable.append(i)
    # print(vital_lable)
    lable = [vital_lable,repo_lable1,star_repo]

    score = user2["score"]
    user=[]
    user.append({
        'user': select_user,
        'code_infor' : code,
        'good_languages'  : good_lang,
        'informations'  : information,
        'influences'  : user_influence,
        # 'repo_lables_join' : temp,
        'lable' : lable,
        'commits' : commits,
        'score' : score,
        'friends':friends
    })
    save(user)
    print(user)
    return user

#保存用户画像数据
def save(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.tag_user.find_one({"user":ghuser[0]["user"]},{})
    if not result:
         db.tag_user.insert(ghuser)
    else:
        db.tag_user.update({"user":ghuser[0]["user"]},ghuser[0])

if __name__ == '__main__':
    user_profile("torvalds")