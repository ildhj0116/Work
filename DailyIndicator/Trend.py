# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 09:02:07 2018

@author: Administrator
"""

import pandas as pd
from datetime import datetime
def MA(price,m_window):
    return price.rolling(m_window).mean()

def TriMA2Trend(ma_price):
    if ma_price["ma_s"] > ma_price["ma_l"] and ma_price['close'] > ma_price["ma_l"]:  
        if ma_price["ma_s"] > ma_price["ma_m"] and ma_price['close'] > ma_price["ma_m"]:
            return 'Long_1'
        elif ma_price["ma_s"] < ma_price["ma_m"] and ma_price['close'] > ma_price["ma_s"]:
            return 'Long_2'
    if ma_price["ma_s"] < ma_price["ma_l"] and ma_price['close'] < ma_price["ma_l"]:   
        if ma_price["ma_s"] < ma_price["ma_m"] and ma_price['close'] < ma_price["ma_m"]:
            return 'Short_1'
        elif ma_price["ma_s"] > ma_price["ma_m"] and ma_price['close'] < ma_price["ma_s"]:
            return 'Short_2'
    return "Null"

def TriTrend(tdate,ma_param_df,main_cnt_df):
    cmt_list = main_cnt_df.columns.tolist()
    tdate = datetime.strptime(tdate,"%Y-%m-%d")
    trend_list = []
    main_cnt_list = []
    for cmt in cmt_list:
        tmp_cl = pd.read_csv("../Futures_data/data_cl/"+cmt[:-4]+".csv", index_col=0, parse_dates=[0])
        main_cnt = main_cnt_df.loc[tdate,cmt]
        main_cl = tmp_cl.loc[:tdate,main_cnt].dropna()
        if cmt[:-4] in ma_param_df.index.tolist():
            ma_param_series = ma_param_df.loc[cmt[:-4],:]
            tmp_ma_price = [MA(main_cl,x).iloc[-1] for x in ma_param_series]
        else:
            ma_param_list = [5,10,60]
            tmp_ma_price = [MA(main_cl,x).iloc[-1] for x in ma_param_list]
        tmp_ma_price.append(main_cl.iloc[-1])
        ma_price = pd.Series(tmp_ma_price,index=["ma_s","ma_m","ma_l","close"],name=main_cnt[:-4])
        trend_lvl = TriMA2Trend(ma_price)
        trend_list.append(trend_lvl)
        main_cnt_list.append(main_cnt[:-4])
    trend_series = pd.Series(trend_list,index=main_cnt_list,name=u"日线趋势")
    return trend_series
    

if __name__ == "__main__":
    ma_param_df = pd.read_csv("parmt.csv",index_col=0)
    main_cnt_df = pd.read_csv("../Futures_data/main_cnt/data/main_cnt_total.csv",index_col=0,parse_dates=[0])
    tdate = "2018-04-23"
    trend = TriTrend(tdate,ma_param_df,main_cnt_df)
    
    
    
    
    
    