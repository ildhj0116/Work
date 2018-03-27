# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:40:06 2018

@author: Administrator
"""

import talib as ta
from WindPy import w
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cmt_list = pd.read_csv("../../Futures_Data/cmt_list/cmt_daily_list.csv").loc[:,"cmt"].tolist()
main_cnt_df = pd.read_csv("../../Futures_Data/main_cnt/data/main_cnt_total.csv",parse_dates=[0],index_col=0)

compute_date_str = "2018-03-22"
compute_date = datetime.strptime(compute_date_str,"%Y-%m-%d")

try:
    main_cnt_list_today = main_cnt_df.loc[compute_date,:].copy()
except:
    print "主力合约列表无更新日期数据，不能进行计算"
else:
    del main_cnt_df
    ATR_list = []
    pre_close_list = []
    for cmt in cmt_list:
        main_cnt = main_cnt_list_today.loc[cmt]
        tmp_dl_data = w.wsd(main_cnt, "high,low,close", "ED-15TD", compute_date_str, "")
        high = tmp_dl_data.Data[0]
        low = tmp_dl_data.Data[1]
        close = tmp_dl_data.Data[2]
        ATR = ta.ATR(np.array(high),np.array(low),np.array(close),14)
        ATR_list.append(ATR[-1])
        pre_close_list.append(close[-2])
    df = pd.DataFrame([ATR_list,pre_close_list],columns=cmt_list,index=["ATR","pre_close"]).T
    df["amplitude"] = df["ATR"] / df["pre_close"]
    amp = df["amplitude"].sort_values(ascending=False).copy()
    
    fig = plt.figure(1)
    axis = fig.add_subplot(111)
    amp.plot.bar(ax=axis,color=[plt.cm.hot(np.arange(0,5*len(amp),5))])
    axis.axhline(0, color='k')