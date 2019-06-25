#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymongo
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel

#停用词
stop = set(stopwords.words('english'))
# print("6",stop)
#标点符号
exclude = set(string.punctuation)
# print("5",exclude)
#数字
exclude1 = set(string.digits)
# print("11",exclude1)
#词性还原
lemma = WordNetLemmatizer()
# print("4",lemma)
def clean(doc):
        # print("2",doc)
        # print(doc.lower())
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        # print("3",stop_free)
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        # print("7",punc_free)
        num_free = ''.join(i for i in punc_free if i not in exclude1)
        # print("99",num_free)
        normalized = " ".join(lemma.lemmatize(word) for word in num_free.split())
        # print("8",normalized)
        filter = nltk.pos_tag(normalized.split(" "))
        # print(filter)
        doc1 = [w for w,pos in filter if not pos.startswith("VB") and not pos.startswith("CD") and not pos.startswith("RB")]
        # print(doc1)
        test3 = " ".join(i for i in doc1)
        # print(test3)
        return test3

def deal_label1(doc_complete):
    doc_clean = []
    for doc in doc_complete:
        if " " in doc:
            doc_clean.append(clean(doc).split())
        else:
            doc = doc + " lu"
            doc_clean.append(clean(doc).split())
    # doc_clean = [clean(doc).split() for doc in doc_complete]
    # print("1",doc_clean)
    # 创建语料的词语词典，每个单独的词语都会被赋予一个索引
    dictionary = corpora.Dictionary(doc_clean)

    # 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # 使用 gensim 来创建 LDA 模型对象
    # 在 DT 矩阵上运行和训练 LDA 模型
    lda = LdaModel(doc_term_matrix,num_topics=3,id2word=dictionary,passes=200)
    temp = lda.print_topics(num_topics=3, num_words=10)
    # print(temp)
    lable = []
    for i in temp:
        # print(i)
        temp1 = i[1].split('"')
        length = len(temp1)
        if length >=2:
            if not temp1[1] in lable:
                lable.append(temp1[1])
        if length >=4:
            if not temp1[3] in lable:
                lable.append(temp1[3])
        if length >= 6:
            if not temp1[5] in lable:
                lable.append(temp1[5])
        if length >= 8:
            if not temp1[7] in lable:
                lable.append(temp1[7])
        if length >= 10:
            if not temp1[9] in lable:
                lable.append(temp1[9])
        if length >= 12:
            if not temp1[11] in lable:
                lable.append(temp1[11])
        if length >= 14:
            if not temp1[13] in lable:
                lable.append(temp1[13])
        if length >= 16:
            if not temp1[15] in lable:
                lable.append(temp1[15])
        if length >= 18:
            if not temp1[17] in lable:
                lable.append(temp1[17])
        if length >= 20:
            if not temp1[19] in lable:
                lable.append(temp1[19])
    # 输出结果
    # print(temp)
    # print(lable)
    return lable

if __name__ == '__main__':
    select_user = 'JakeWharton'
    doc_complete = []
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    user = db.ghusers.find_one({'login': select_user})
    # 整合文档数据
    for i in user['star']:
        star_des = i[2]
        # print(star_des)
        if not star_des is None:
            doc_complete.append(star_des)

    # print(doc_complete)
    deal_label1(doc_complete)