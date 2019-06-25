#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# data = pd.read_csv('D:/MongoDB/Server/4.0/bin/user_analyze_1.csv')
# # sns.pairplot(data,x_vars=['TV','radio','newspaper'],y_vars='sales',size=7,aspect=0.8,kind='reg')
# # plt.show()
# feature_cols = ['commit','issue','follower','repos','languages']
# X = data[feature_cols]
# print(X.head())
# print(type(X))
# print(X.shape)
#
# # select a Series from the DataFrame
# y = data['score']
# # equivalent command that works if there are no spaces in the column name
# # print the first 5 values
# print(y.head())
#
# #<pre name="code" class="python"><span style="font-size:14px;">##构造训练集和测试集
# from sklearn.cross_validation import train_test_split  #这里是引用了交叉验证
# X_train,X_test, y_train, y_test = train_test_split(X, y, random_state=1)
# print(X_train.shape)
# print(y_train.shape)
# print (X_test.shape)
# print (y_test.shape)
# #
# from sklearn.linear_model import LinearRegression
# linreg = LinearRegression()
# model=linreg.fit(X_train, y_train)
# print(model)
# print (linreg.intercept_)
# print (linreg.coef_)
#
# # pair the feature names with the coefficients
# zip(feature_cols, linreg.coef_)
#
# y_pred = linreg.predict(X_test)
# print (y_pred)
#
# #<pre name="code" class="python">#计算Sales预测的RMSE
# print (type(y_pred),type(y_test))
# print (len(y_pred),len(y_test))
# print (y_pred.shape,y_test.shape)
# from sklearn import metrics
# import numpy as np
# sum_mean=0
# for i in range(len(y_pred)):
#     sum_mean+=(y_pred[i]-y_test.values[i])**2
# sum_erro=np.sqrt(sum_mean/50)
# # calculate RMSE by hand
# print( "RMSE by hand:",sum_erro)
#
# import matplotlib.pyplot as plt
# plt.figure()
# plt.plot(range(len(y_pred)),y_pred,'b',label="predict")
# plt.plot(range(len(y_pred)),y_test,'r',label="test")
# plt.legend(loc="upper right") #显示图中的标签
# plt.xlabel("the number of sales")
# plt.ylabel('value of sales')
# plt.show()