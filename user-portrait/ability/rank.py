#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pymongo

#保存rank数据
def save_score(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.rank_score.find_one({"login": ghuser[0]["login"]})
    if not result:
        db.rank_score.insert(ghuser)
    else:
        db.rank_score.update({"login": ghuser[0]["login"]}, ghuser[0])

#保存commit数据
def save_commit(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.rank_commit.find_one({"login": ghuser[0]["login"]})
    if not result:
        db.rank_commit.insert(ghuser)
    else:
        db.rank_commit.update({"login": ghuser[0]["login"]}, ghuser[0])

#保存follow数据
def save_follow(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.rank_follow.find_one({"login": ghuser[0]["login"]})
    if not result:
        db.rank_follow.insert(ghuser)
    else:
        db.rank_follow.update({"login": ghuser[0]["login"]}, ghuser[0])

#保存repos数据
def save_repos(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.rank_repos.find_one({"login": ghuser[0]["login"]})
    if not result:
        db.rank_repos.insert(ghuser)
    else:
        db.rank_repos.update({"login": ghuser[0]["login"]}, ghuser[0])

#保存issue数据
def save_issue(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.rank_issue.find_one({"login": ghuser[0]["login"]})
    if not result:
        db.rank_issue.insert(ghuser)
    else:
        db.rank_issue.update({"login": ghuser[0]["login"]}, ghuser[0])

#保存languages数据
def save_languages(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.rank_languages.find_one({"login": ghuser[0]["login"]})
    if not result:
        db.rank_languages.insert(ghuser)
    else:
        db.rank_languages.update({"login": ghuser[0]["login"]}, ghuser[0])

#保存languages数据
def save_rank(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.rank.find_one({"login": ghuser[0]["login"]})
    if not result:
        db.rank.insert(ghuser)
    else:
        db.rank.update({"login": ghuser[0]["login"]}, ghuser[0])

#rank:利用sort
def rank():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    count = db.user_analyze3.count()

    # 根据follow排序
    user_follow = db.user_analyze3.find().sort([("follower", -1)])
    for i in range(0,count):
        follow= []
        follow.append({
            "login":user_follow[i]["login"],
            "follow_rank":i+1
        })
        save_follow(follow)

    #根据score排序
    user_score = db.user_analyze3.find().sort([("score", -1)])
    for i in range(0,count):
        score = []
        score.append({
            "login":user_score[i]["login"],
            "score_rank":i+1
        })
        save_score(score)

    # 根据commit排序
    user_commit = db.user_analyze3.find().sort([("commit", -1)])
    for i in range(0,count):
        commit = []
        commit.append({
            "login":user_commit[i]["login"],
            "commit_rank":i+1
        })
        save_commit(commit)

    # 根据repos排序
    user_repos = db.user_analyze3.find().sort([("repos", -1)])
    for i in range(0, count):
        repos = []
        repos.append({
            "login": user_repos[i]["login"],
            "repos_rank": i + 1
        })
        save_repos(repos)

    # 根据issue排序
    user_issue = db.user_analyze3.find().sort([("issue", -1)])
    for i in range(0, count):
        issue = []
        issue.append({
            "login": user_issue[i]["login"],
            "issue_rank": i + 1
        })
        save_issue(issue)

    # 根据languages排序
    user_languages = db.user_analyze3.find().sort([("languages", -1)])
    for i in range(0, count):
        languages = []
        languages.append({
            "login": user_languages[i]["login"],
            "languages_rank": i + 1
        })
        save_languages(languages)

    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.rank_score.find()
    for i in result:
        data = []
        commit_result = db.rank_commit.find_one({"login": i["login"]})
        follow_result = db.rank_follow.find_one({"login": i["login"]})
        issue_result = db.rank_issue.find_one({"login": i["login"]})
        languages_result = db.rank_languages.find_one({"login": i["login"]})
        repos_result = db.rank_repos.find_one({"login": i["login"]})
        data.append({
            "login":i["login"],
            "score_rank":i["score_rank"],
            "commit_rank":commit_result["commit_rank"],
            "issue_rank": issue_result["issue_rank"],
            "follow_rank": follow_result["follow_rank"],
            "languages_rank": languages_result["languages_rank"],
            "repos_rank": repos_result["repos_rank"],
        })
        print(data)
        save_rank(data)

if __name__ == '__main__':
    rank()
