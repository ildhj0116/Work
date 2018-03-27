# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 09:47:05 2018

@author: Administrator
"""
from WindPy import w
import pandas as pd
import matplotlib.pyplot as plt

start_date = "2017-09-24"
end_date = "2018-03-23"


#下载南华商品指数并画图
NH_Data = w.wsd("NH0100.NHF", "close", start_date, end_date, "")
NH_Data = pd.DataFrame(NH_Data.Data,columns=NH_Data.Times,index=NH_Data.Fields).T
fig = plt.figure(1)
axis = fig.add_subplot(111)
NH_Data.plot(ax=axis)

#商品指数收益率
ret = (NH_Data - NH_Data.shift(1)) / NH_Data
ret.columns = ["ret"]
fig = plt.figure(2)
axis = fig.add_subplot(111)
ret.plot(ax=axis)

#品种收益率
#Nanhua_code_series = pd.read_csv("../../Futures_Data/cmt_list/Nanhua_code_list.csv",index_col=0)
#cmt_list = pd.read_csv("../../Futures_Data/cmt_list/cmt_daily_list.csv").loc[:,"cmt"].tolist()
#cmt_windcode = [Nanhua_code_series.loc[x[:-4]] for x in cmt_list]
