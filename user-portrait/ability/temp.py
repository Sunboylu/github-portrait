# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# from lxml import etree
# import requests
#
# url = 'https://wangchujiang.com/github-rank'
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
#
# response = requests.get(url,headers=headers)
# html = response.text
#
# movie_name_xpath = '/html/body/ul/li[*]/div[2]/div[1]/a/i/text()'
#
# s = etree.HTML(html)
# movie_name = s.xpath(movie_name_xpath)
# print(movie_name)











# import requests
# import json
# from requests.exceptions import RequestException
# from lxml import etree
# import time
# from multiprocessing import Pool
# from urllib.parse import urljoin
# import json
# import pymongo
#
# num = 20
#
#
# def get_one_page(url):
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
#         }
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             return response.text
#         return None
#     except RequestException:
#         return None
#
#
# def parse_one_page(html):
#     html = etree.HTML(html)
#     user_name = html.xpath('//*[@id="list"]/div/div[3]/h2/span/text()')
#     user_rank = html.xpath('//*[@id="list"]/div/div[1]/text()')
#
#     for i in range(num):
#         user = {}
#         user['name'] = user_name[i]
#         user['rank'] = user_rank[i]
#         print(user)
#         yield user
#
#
# def save(data):
#     client = pymongo.MongoClient('localhost', 27017)
#     db = client.local
#     # result = db.paqu.find_one({"login": ghuser[0]["login"]})
#     # if not result:
#     #     db.paqu.insert(ghuser)
#     # else:
#     #     db.paqu.update({"login": ghuser[0]["login"]}, ghuser[0])
#     db.rank1.insert(data)
#
#
# def main(pageId):
#     url = "http://39.105.63.219:8080/rank-developer?&pageId={}&platform=0".format(pageId)
#     print(url)
#     html = get_one_page(url)
#     result = parse_one_page(html)
#     result = list(result)
#     print(result)
#     save(result)
#
#
# if __name__ == '__main__':
#     for i in range(10):
#         main(pageId=i+1)

import requests
import json
from requests.exceptions import RequestException
from lxml import etree
import time
from multiprocessing import Pool
from urllib.parse import urljoin
import json
import pymongo

num = 500


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    html = etree.HTML(html)
    user_name = html.xpath('/html/body/ul/li/div[2]/div[1]/a/i/text()')
    user_rank = html.xpath('/html/body/ul/li/div[2]/div[1]/span/text()')
    # user_location=html.xpath('/html/body/ul/li/div[2]/div[2]/span/text()')

    for i in range(num):
        user = {}
        user['name'] = user_name[i]
        user['rank'] = user_rank[i]
        # user['location'] = user_location[i]
        print(user)
        yield user


def save(data):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    # result = db.paqu.find_one({"login": ghuser[0]["login"]})
    # if not result:
    #     db.paqu.insert(ghuser)
    # else:
    #     db.paqu.update({"login": ghuser[0]["login"]}, ghuser[0])
    db.rank2.insert(data)


def main():
    url = "https://wangchujiang.com/github-rank/index.html"
    print(url)
    html = get_one_page(url)
    result = parse_one_page(html)
    result = list(result)
    print(result)
    save(result)


if __name__ == '__main__':
    main()