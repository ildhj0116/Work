# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 17:13:10 2018

@author: Administrator
"""
import pandas as pd
from Trend import TriTrend
from Basis import Basis_Rate
from Spread import Spread
from Seasonal import Seasonal_Winning_Rate
from Deviation import Deviation
from Hour_Trend import Hour_Trend
import numpy as np


def standarlize(series):
    std_series = (series * 2 - 1)/5
    return std_series.tolist()
    
    
    
if __name__ == "__main__":
    ma_param_df = pd.read_csv("parmt.csv",index_col=0)
    main_cnt_df = pd.read_csv("../Futures_data/main_cnt/data/main_cnt_total.csv",index_col=0,parse_dates=[0])
    tdate_series = pd.read_csv("../Futures_data/others/trade_date.csv",index_col=0)
    tdate = "2018-04-25"
    pre_tdate = tdate_series.loc[:tdate].index[-2]
    
    trend = TriTrend(tdate,ma_param_df,main_cnt_df).sort_values()
    h_trend = Hour_Trend(tdate,pre_tdate,main_cnt_df)
    basis_rate_series = Basis_Rate(tdate,main_cnt_df)    
    spread_rate_series = Spread(main_cnt_df,tdate)    
    seasonal_winrate = Seasonal_Winning_Rate(main_cnt_df,tdate)
    deviation_df = Deviation(tdate,main_cnt_df,trend)
    
    df = pd.concat([trend,h_trend,deviation_df,basis_rate_series,spread_rate_series,seasonal_winrate], axis=1)
    
    
#    df["basis"] = df[u"贴水率"].fillna(-10).copy()
#    df["spread"] = (-df[u"价差贴水率"]).copy()
#    df["std_season"] = standarlize(df[u"季节性胜率"])
#    df["point"] = 0.4 * df["basis"] + 0.3 * df[u"价差贴水率"] + 0.3 * df["std_season"]
    df.sort_values(by=[u"日线趋势",u"小时线趋势"],ascending=[True,False],inplace=True)
    df["basis_rank"] = df.groupby([u"日线趋势",u"小时线趋势"])[u"基差贴水率"].rank(ascending=False)
    df["basis_nan"] = [1 if np.isnan(x) else 0 for x in df["basis_rank"].tolist()]
    df["spread_rank"] = df.groupby([u"日线趋势",u"小时线趋势"])[u"价差贴水率"].rank(ascending=False)
    df["seasonal_rank"] = df.groupby([u"日线趋势",u"小时线趋势"])[u"季节性胜率"].rank(ascending=False)
    df["point"] = df[["seasonal_rank","basis_rank","spread_rank"]].sum(axis=1)
    df.sort_values(by=[u"日线趋势",u"小时线趋势","basis_nan","point"],ascending=[True,False,True,True],inplace=True)
    df_final = df[[u"日线趋势",u"小时线趋势",u"KDJ背离",u"MACD背离",u"基差贴水率",u"价差贴水率",u"季节性胜率"]]
    df_final.to_csv("output/" + tdate + ".csv",encoding="gbk")
    


