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

def repo_des_label(select_user):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    # 整合文档数据
    query = {"owner":select_user}
    all_lable = []
    for user in db.items.find(query):
        doc_complete = []
        repos_des = user['description']
        # print(repos_des)
        if not repos_des is None:
            doc_complete.append(repos_des)
            lable = deal_label(doc_complete)
        else:
            lable = None
        temp = (user['item_name'],lable)
        all_lable.append(temp)

        # print(lable)

    # print(all_lable)
    return all_lable
def deal_label(doc_complete):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    exclude1 = set(string.digits)
    lemma = WordNetLemmatizer()

    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        num_free = ''.join(i for i in punc_free if i not in exclude1)
        normalized = " ".join(lemma.lemmatize(word) for word in num_free.split())
        filter = nltk.pos_tag(normalized.split(" "))
        doc1 = [w for w, pos in filter if
                not pos.startswith("VB") and not pos.startswith("CD") and not pos.startswith("RB")]
        test3 = " ".join(i for i in doc1)
        return test3

    doc_clean = [clean(doc).split() for doc in doc_complete]

    # 创建语料的词语词典，每个单独的词语都会被赋予一个索引
    dictionary = corpora.Dictionary(doc_clean)

    # 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # 使用 gensim 来创建 LDA 模型对象
    # 在 DT 矩阵上运行和训练 LDA 模型
    lda = LdaModel(doc_term_matrix,num_topics=1,id2word=dictionary,passes=200)
    temp = lda.print_topics(num_topics=1, num_words=3)
    lable = []
    for i in temp:
        temp1 = i[1].split('"')
        if len(temp1)>1:
            lable.append(temp1[1])
        if len(temp1) > 3:
            lable.append(temp1[3])
        if len(temp1) > 5:
            lable.append(temp1[5])
    # 输出结果
    # print(temp)
    # print(lable)
    return lable

# if __name__ == '__main__':
#     repo_des_label('alexwohlbruck')