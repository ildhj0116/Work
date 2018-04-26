# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:33:15 2018

@author: Administrator
"""

import pandas as pd
from datetime import datetime
from WindPy import w
w.start()


def histroy_same_date(tdate,years=10):
    his_list = []
    for y in range(-years,0):
        his_y = w.tdaysoffset(y, "2018-04-24", "Period=Y;TradingCalendar=DCE")
        his_y = his_y.Data[0][0]
        his_list.append(his_y)
    return his_list
    
def Seasonal_Winning_Rate(main_cnt_df,tdate):
    tdate = datetime.strptime(tdate,"%Y-%m-%d")
    historic_tdate_list = histroy_same_date(tdate)
    winning_rate_list = []
    main_cnt_list = []
    for cmt in main_cnt_df.columns.tolist():
        main_cnt_series = main_cnt_df[cmt].dropna()
        tmp_his_list = [x for x in historic_tdate_list if x in main_cnt_series.index.tolist()]
        main_cnt_his = main_cnt_series.loc[tmp_his_list]
        tmp_cl = pd.read_csv("../Futures_data/data_cl/"+cmt[:-4]+".csv", index_col=0, parse_dates=[0])
        back = [tmp_cl.loc[:x,main_cnt_his.loc[x]].iloc[-30:].mean() for x in main_cnt_his.index.tolist()]
        forward = [tmp_cl.loc[x:,main_cnt_his.loc[x]].iloc[:30].mean() for x in main_cnt_his.index.tolist()]
        his_df = pd.DataFrame([back,forward],index=["back","forward"],columns=main_cnt_his.index).T
        his_df["WnL"] = his_df["back"] < his_df["forward"]
        winning_rate = float(his_df["WnL"].sum()) / len(his_df["WnL"])
        winning_rate_list.append(winning_rate)
        main_cnt_list.append(main_cnt_df.loc[tdate,cmt][:-4])
    seasonal_winrate = pd.Series(winning_rate_list,index=main_cnt_list,name=u"季节性胜率")
    return seasonal_winrate


if __name__ == "__main__":
    main_cnt_df = pd.read_csv("../Futures_data/main_cnt/data/main_cnt_total.csv",index_col=0,parse_dates=[0])
    tdate = "2018-04-26"
    seasonal_winrate = Seasonal_Winning_Rate(main_cnt_df,tdate)
    
    
    
    
    
    
    
    
    
    
    
    
    