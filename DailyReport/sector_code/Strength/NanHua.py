# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 09:47:05 2018

@author: Administrator
"""
from WindPy import w
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def NanHua(start_date,end_date):
    fig_list = []
    #下载南华商品指数并画图
    NH_Data = w.wsd("NH0100.NHF", "close", start_date, end_date, "")
    NH_Data = pd.DataFrame(NH_Data.Data,columns=NH_Data.Times,index=NH_Data.Fields).T
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    NH_Data.plot(ax=axis)
    plt.xlabel(u"日期",fontsize=15)
    plt.ylabel(u"商品指数点位",fontsize=15)
    plt.title(u"商品指数点位曲线",fontsize=15)
    plt.legend([u"点位"],loc=2)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    fig_list.append(fig)
    
    #商品指数收益率
    ret = (NH_Data - NH_Data.shift(1)) / NH_Data
    ret.columns = ["ret"]
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    ret.plot(ax=axis)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y))) 
    plt.xlabel(u"日期",fontsize=15)
    plt.ylabel(u"商品指数收益率",fontsize=15)
    plt.title(u"商品指数收益率曲线",fontsize=20)
    plt.legend([u"收益率"],loc=2)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    fig_list.append(fig)
    return fig_list
#品种收益率
    
if __name__ == "__main__":
#    Nanhua_code_series = pd.read_csv("../../Futures_Data/cmt_list/Nanhua_code_list.csv",index_col=0)
#    cmt_list = pd.read_csv("../../Futures_Data/cmt_list/cmt_daily_list.csv").loc[:,"cmt"].tolist()
#    cmt_windcode = [Nanhua_code_series.loc[x[:-4]] for x in cmt_list]
    start_date = "2018-01-02"
    end_date = "2018-04-11"
    
    
       
    fig = NanHua(start_date,end_date)
