# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 14:34:37 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta

def color_setting(ret):
    colors = ['r' if x>0 else 'g' for x in ret]
    return colors
    

cmt_list = pd.read_csv("../../Futures_Data/cmt_list/cmt_daily_list.csv").loc[:,"cmt"].tolist()
main_cnt_df = pd.read_csv("../../Futures_Data/main_cnt/data/main_cnt_total.csv",parse_dates=[0],index_col=0)


compute_date = datetime.strptime("2018-03-22","%Y-%m-%d")

try:
    main_cnt_list_today = main_cnt_df.loc[compute_date,:].copy()
except:
    print "主力合约列表无更新日期数据，不能进行计算"
else:
    del main_cnt_df
    cl_series_list = []
    for cmt in cmt_list:
        tmp_cl = pd.read_csv("../../Futures_Data/data_cl/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
        main_cnt = main_cnt_list_today.loc[cmt]
        main_cnt_cl = tmp_cl[main_cnt].dropna().copy()
        main_cnt_cl.name = cmt
        del tmp_cl
        cl_series_list.append(main_cnt_cl)
    cl_df = pd.concat(cl_series_list,axis=1)
    
    interval = 30
    cl_last_interval = cl_df[cl_df.index>(compute_date-timedelta(days=interval))]
    #新高
    cl_max = cl_last_interval.iloc[:-1,:].max(axis=0)
    new_high = cl_max < cl_last_interval.iloc[-1,:]
    #新低
    cl_min = cl_last_interval.iloc[:-1,:].min(axis=0)
    new_low = cl_min > cl_last_interval.iloc[-1,:]
    print "新高：" + ','.join(cl_df.columns[new_high].tolist())
    print "新低：" + ','.join(cl_df.columns[new_low].tolist())
    
    
    
    
    
    
    