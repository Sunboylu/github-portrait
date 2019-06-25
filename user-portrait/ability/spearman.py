#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pandas as pd
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client.local
result = db.rank_score.find()
#5个维度rank数据+score
issue = []
commit = []
follower = []
repos = []
languages = []
score = []
for i in result:
    login = i["login"]
    result_issue = db.rank_issue.find_one({"login": login})
    issue.append(result_issue["issue_rank"])
    result_commit = db.rank_commit.find_one({"login": login})
    commit.append(result_commit["commit_rank"])
    result_follower = db.rank_follow.find_one({"login": login})
    follower.append(result_follower["follow_rank"])
    result_repos = db.rank_repos.find_one({"login": login})
    repos.append(result_repos["repos_rank"])
    result_languages = db.rank_languages.find_one({"login": login})
    languages.append(result_languages["languages_rank"])
    score.append(i["score_rank"])
print(issue)
print(commit)
print(follower)
print(repos)
print(languages)
print(score)
#
df = pd.DataFrame({'issue':issue,
                   'commit':commit,
                   'follower':follower,
                   'repos':repos,
                   'language': languages,
                   'score': score})
#
# print(df.corr())
#
print(df.corr('spearman'))
#
# print(df.corr('kendall'))
