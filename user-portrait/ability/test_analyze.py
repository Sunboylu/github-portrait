#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pymongo

#保存计算后的5项维度-数据
def save(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.user_analyze3.find_one({"login": ghuser[0]["login"]})
    if not result:
        db.user_analyze3.insert(ghuser)
    else:
        db.user_analyze3.update({"login": ghuser[0]["login"]}, ghuser[0])

#项目经验计算
def repos(public_repos,num_languages):
    #总项目数
    repos_counts = public_repos
    #总fork数、watches、star
    fork_count=0
    watch_count=0
    star_count=0
    for i in num_languages:
        #i[0]项目名称，i[1]项目语言,i[2]fork,i[3]watch,i[4]star
        fork_count = fork_count+i[2]
        watch_count = watch_count + i[3]
        star_count = star_count + i[4]
    #项目经验
    count = repos_counts*0.2+fork_count*0.3+watch_count*0.3+star_count*0.2
    return count

def takesecond(elem):
    return elem[3]
def languages(message):
    #每个语言的项目
    user_language={}
    for i in message:
        #i[0]项目名称，i[1]项目语言,i[2]fork,i[3]watch,i[4]star
        if  not i[1] is None:
            if (i[1] in user_language):
                user_language[i[1]].append([i[0],i[2],i[3],i[4]])
            else:
                user_language[i[1]] = [[i[0],i[2],i[3],i[4]]]
    #语言数量
    language_count = len(user_language)
    #语言熟练度
    language=[]
    for item,value in user_language.items():
        fork_count = 0
        watch_count = 0
        star_count = 0
        for i in user_language[item]:
            fork_count = fork_count+i[1]
            watch_count = watch_count+i[2]
            star_count = star_count + i[3]
        temp = (item,fork_count,watch_count,star_count,len(user_language[item]))
        language.append(temp)
    language.sort(key=takesecond,reverse=True)
    count = 0
    if len(language)>0:
        count = language[0][1]*0.2+language[0][2]*0.3+language[0][3]*0.3+language[0][4]*0.2+language_count
    return int(count)

def deal_data():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    nums = db.user_3.count()
    # print(nums)
    user = db.user_3.find({},{'login':1,"public_repos":1,"num_languages":1,"followers":1,"commits":1,"issues":1,"_id":0})
    num_commits = []
    num_issues = []
    num_followers = []
    num_repos = []
    num_languages = []
    for i in range(0, nums):
        userone = user[i]
        num_commits.append(userone['commits'])
        num_issues.append(userone['issues'])
        num_followers.append(userone['followers'])
        num_repos.append(repos(userone['public_repos'],userone['num_languages']))
        num_languages.append( languages(userone['num_languages']))
    max_commits = max(num_commits)
    min_commits = min(num_commits)

    max_issues = max(num_issues)
    min_issues = min(num_issues)

    max_followers = max(num_followers)
    min_followers = min(num_followers)

    max_repos = max(num_repos)
    min_repos = min(num_repos)

    max_languages = max(num_languages)
    min_languages = min(num_languages)

    for i in range(0, nums):
        new_user = []

        #commit处理
        commit_temp = user[i]['commits']
        commit_temp_change = round((commit_temp-min_commits)/(max_commits-min_commits),6)

        #issues处理
        issue_temp = user[i]['issues']
        issue_temp_change = round((issue_temp - min_issues) / (max_issues - min_issues), 6)

        #followers处理
        followers_temp = user[i]['followers']
        followers_temp_change = round((followers_temp - min_followers) / (max_followers - min_followers), 6)

        # repos处理
        repos_temp = repos(user[i]['public_repos'],user[i]['num_languages'])
        repos_temp_change = round((repos_temp - min_repos) / (max_repos - min_repos), 6)

        #language处理
        languages_temp = languages(user[i]['num_languages'])
        languages_temp_change = round((languages_temp - min_languages) / (max_languages - min_languages), 6)


        #活跃度
        w1 = 0.05
        #贡献度
        w2 = 0.15
        #社区影响力
        w3 = 0.7
        #项目经验
        w4 = 0.05
        #语言能力
        w5 = 0.05
        score = round(w1*issue_temp_change + w2*commit_temp_change + w3*followers_temp_change + w4*repos_temp_change + w5*languages_temp_change,6)

        new_user.append({
            'login': user[i]["login"],
            'commit': commit_temp_change,
            'issue':  issue_temp_change,
            'follower': followers_temp_change,
            'repos':  repos_temp_change,
            'languages':  languages_temp_change,
            'score': score
        })
        print(new_user)
        save(new_user)

if __name__ == '__main__':
    deal_data()
