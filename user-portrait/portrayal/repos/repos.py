#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pymongo

def repos(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    repos = [db.Repository.find({'owner.login': select_user})]
    #每个语言的项目，大小，及其fork和star数量
    user_language={}
    code_length = 0
    fork_num = 0
    watcher = 0
    for i in repos[0]:
        code_length += i["size"]
        fork_num += i["forks_count"]
        watcher += i["watchers_count"]
        temp = (i["name"],i["size"],i["forks_count"]*0.5+i["watchers_count"]*0.5)
        if  not i["language"] is None:
            if (i["language"] in user_language):
                user_language[i["language"]].append(temp)
            else:
                user_language[i["language"]] = [temp]
    language = {}
    for key in user_language.keys():
        temp1 = user_language[key]
        # print(temp1)
        count = len(temp1)
        language[key] = count
    # print(language)
    # print(user_language)
    code_ability = {}
    code_ability['code_length']=code_length
    code_ability['watcher']=watcher
    code_ability['fork_num']=fork_num
    code_ability['code_num'] = len(user_language)
    code_ability['language'] = language

    return code_ability

def good_language(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    repos = [db.Repository.find({'owner.login': select_user})]
    user_language = {}
    # print(repos)
    for i in repos[0]:
        temp = (i["name"], i["size"], i["forks_count"] * 0.5 + i["watchers_count"] * 0.5)
        if not i["language"] is None:
            if (i["language"] in user_language):
                user_language[i["language"]].append(temp)
            else:
                user_language[i["language"]] = [temp]
    #计算各个语言的项目数量,并排序取第一名
    language_num = {}
    for key in user_language.keys():
        temp1=user_language[key]
        # print(temp1)
        count_item = 0
        code_length = 0
        #所有项目累计权重
        for i in temp1:
            count_item = count_item+i[2]
            code_length = code_length + i[1]
        count_languuage = len(temp1)
        #该语言下的项目数量，所有项目权重之和，所有项目编码长度
        language_num[key]=(count_languuage,count_item,code_length)
    global temp2
    if len(language_num)>0:
        temp2 =  sorted(language_num.items(),key=lambda item:item[1])[len(language_num)-1]
    return temp2

if __name__ == '__main__':
    language=repos('goodfeli')
    good_language = good_language('goodfeli')
    print(language)
    print(good_language)