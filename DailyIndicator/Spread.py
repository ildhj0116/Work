# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 13:44:34 2018

@author: Administrator
"""

import pandas as pd
from datetime import datetime


def secondary_main_cnt(tdate,main_cnt_series):
    secondary_cnt_list = []
    for cmt in main_cnt_series.index.tolist():
        tmp_oi = pd.read_csv("../Futures_data/data_oi/"+cmt[:-4]+".csv", index_col=0, parse_dates=[0])
        tmp_oi_series = tmp_oi.loc[tdate,main_cnt_series[cmt]:]
        secondary_cnt = tmp_oi_series.iloc[1:].idxmax()
        secondary_cnt_list.append(secondary_cnt)
    secondary_cnt_series = pd.Series(secondary_cnt_list,index=main_cnt_series.index)
    return secondary_cnt_series
        

def Spread(main_cnt_df,tdate):
    tdate = datetime.strptime(tdate,"%Y-%m-%d")
    main_cnt_series = main_cnt_df.loc[tdate,:]
    secondary_cnt_series = secondary_main_cnt(tdate,main_cnt_series)
    cnt_df = pd.DataFrame([main_cnt_series,secondary_cnt_series],index=["main","secondary"],columns=main_cnt_series.index).T
    spread_list = []
    main_cnt_list = []
    for cmt in cnt_df.index.tolist():
        tmp_cl = pd.read_csv("../Futures_data/data_cl/"+cmt[:-4]+".csv", index_col=0, parse_dates=[0])
        main_cl = tmp_cl.loc[tdate,cnt_df.loc[cmt,"main"]]
        secondary_cl = tmp_cl.loc[tdate,cnt_df.loc[cmt,"secondary"]]
        spread_rate = float(main_cl) / secondary_cl - 1
        spread_list.append(spread_rate)
        main_cnt_list.append(main_cnt_df.loc[tdate,cmt][:-4])
    spread_rate_series = pd.Series(spread_list,index=main_cnt_list,name=u"价差贴水率")
    return spread_rate_series
    

if __name__ == "__main__":
    main_cnt_df = pd.read_csv("../Futures_data/main_cnt/data/main_cnt_total.csv",index_col=0,parse_dates=[0])
    tdate = "2018-04-23"
    spread_rate_series = Spread(main_cnt_df,tdate)
    
    
    
    
    