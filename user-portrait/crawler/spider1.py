from crawler.header import headers
import requests
import bisect
import pymongo

#获得用户的following数据
def get_following(select_url):
    # 通过get请求网页信息
    url = select_url.split('{')[0] + '?page={}'
    message = []
    for i in range(1,10+1):
        header = headers()
        url1 = url.format(i)
        response = requests.get(url1,headers=header,auth=('###', '###'))
        if (response.status_code != 200):
            print('error: fail to request')
            return None
        j = response.json()
        if len(j)>0:
            for k in range(len(j)):
                pro = j[k]
                message.append(pro["login"])
        else:
            break
    return message

#获得用户的star项目信息
def get_star(login):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    # 在已有的USER数据库查询
    search = db.User_starrepos.find_one({"login": login})
    stars = search["star_repos"]
    message = []
    for i in stars:
        if "name" not in i.keys():
            break
        name = i["name"]
        owner = i["owner"]["login"]
        description = i["description"]
        language = i["language"]
        message.append([name, owner, description, language])
    return message

#获得用户的repos数据
def get_repos(login):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    # 在已有的Repository数据库查询
    search = db.Repository.find({"owner.login": login})
    message = []
    for i in search:
        name = i["name"]
        description = i["description"]
        language = i["language"]
        message.append([name,description,language])
    return message


#获得用户的organiz数据
def get_organization(login):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    # 在已有的Repository数据库查询
    search = db.User_organize.find({"login": login})
    # 存储repos部分数据
    message = []
    if not search[0]["orgainze"] is None:
        for i in search[0]["orgainze"]:
            message.append(i)
    return message

#获得其好友
def get_friend(login):
    header = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'token  e91fe3b89a7d3145a4b8ed81b9389e6dab539a72',
        'Content-Type': 'application/json',
        'method': 'GET',
        'Accept': 'application/vnd.github.symmetra-preview+json'
    }
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    # 在已有的User_issue数据库查询
    search = db.User_issue.find({"user.login": login})
    # 存储repos部分数据
    friends = []
    comment1 = []
    comment = []
    for i in search:
        comments = i["comments"]
        comments_url = i["comments_url"]
        print(comments_url)
        if comments > 0:
            url = comments_url + '?page={}'
            for i in range(1, 20 + 1):
                url1 = url.format(i)
                response = requests.get(url1, headers=header, auth=('###', '###'))
                if (response.status_code != 200):
                    print('error: fail to request')
                    return None
                j = response.json()
                if len(j) > 0:
                    for h in j:
                        comment.append(h)
                        if h["user"]["login"] != login:
                            friends.append(h["user"]["login"])
                else:
                    break
    comment1.append({
        "login":login,
        "comment":comment
    })
    save_comment(comment1)
    friend = []
    for i in set(friends):
        num = friends.count(i)
        temp = (num, i)
        bisect.insort(friend, temp)
    #取次数最多的10 个
    message = friend[-10:]
    return message

#保存comment数据
def save_comment(ghuser):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    result = db.User_comment.find_one({"login":ghuser[0]["login"]})
    if not result:
         db.User_comment.insert(ghuser[0])
    else:
        db.User_comment.update({"login":ghuser[0]["login"]},ghuser[0])