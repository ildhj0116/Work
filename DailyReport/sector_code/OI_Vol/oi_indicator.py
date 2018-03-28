# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 15:21:46 2018

@author: Administrator
"""

import pandas as pd
from WindPy import w
#from datetime import datetime
import matplotlib.pyplot as plt


def color_setting(ret):
    colors = ['r' if x>0 else 'g' for x in ret]
    return colors

def vol_oi_indicator(main_cnt_list_today,cmt_list,compute_date_str,relative_data_path):
    vol_series_list = []
    oi_series_list = []
    TopN_oi_series_list = []
    for cmt in cmt_list:
        main_cnt = main_cnt_list_today.loc[cmt]
        tmp_vol = pd.read_csv(relative_data_path + "/data_vol/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
        tmp_oi = pd.read_csv(relative_data_path + "/data_oi/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
        tmp_oi_rank = w.wset("futureoir","startdate="+compute_date_str+";enddate="+compute_date_str+\
                             ";varity="+cmt+";wind_code="+main_cnt+";order_by=long;ranks=all;field="+\
                             "member_name,long_potion_rate,short_position_rate,net_position_rate")                
        
        tmp_oi_rank = pd.DataFrame(tmp_oi_rank.Data, index=tmp_oi_rank.Fields).T        
        
        main_cnt_vol = tmp_vol[main_cnt].dropna().copy()
        main_cnt_vol.name = cmt
        main_cnt_oi = tmp_oi[main_cnt].dropna().copy()
        main_cnt_oi.name = cmt
        TopN_oi_rate_series = tmp_oi_rank.iloc[1,:]
        TopN_oi_rate_series.loc["short_position_rate"] = -TopN_oi_rate_series.loc["short_position_rate"]
        TopN_oi_rate_series.loc["net_position_rate"] = TopN_oi_rate_series["long_potion_rate"] + TopN_oi_rate_series.loc["short_position_rate"]
        TopN_oi_rate_series.name = cmt
        
        del tmp_vol,tmp_oi,tmp_oi_rank
        vol_series_list.append(main_cnt_vol)
        oi_series_list.append(main_cnt_oi)
        TopN_oi_series_list.append(TopN_oi_rate_series)
        
    vol_df = pd.concat(vol_series_list,axis=1)
    oi_df = pd.concat(oi_series_list,axis=1)
    TopN_oi_df = pd.concat(TopN_oi_series_list,axis=1)
    
    #成交、持仓量变化比率
    vol_chg_df = (vol_df - vol_df.shift(1)) / vol_df.shift(1)
    vol_chg = vol_chg_df.iloc[-1,:]    
    vol_chg_positive = vol_chg[vol_chg>0].copy()
    vol_chg_negative = vol_chg[vol_chg<0].copy()
    vol_chg_positive.sort_values(ascending=False,inplace=True)
    vol_chg_negative.sort_values(ascending=True,inplace=True)
    
    #换手率
    turn = vol_df.iloc[-1,:] / oi_df.iloc[-1,:]
        
    
        
    #画图
    #成交手数变化    
    fig = plt.figure()
    axis = fig.add_subplot(111)
    vol_chg_positive.plot.bar(ax=axis,color=['red'])
    axis.axhline(0, color='k')
    fig = plt.figure()
    axis = fig.add_subplot(111)
    vol_chg_negative.plot.bar(ax=axis,color=['green'])
    axis.axhline(0, color='k')
    #换手率
    fig = plt.figure()
    axis = fig.add_subplot(111)
    turn.plot.bar(ax=axis)
    #前十持仓比例
    fig = plt.figure()
    axis = fig.add_subplot(111)
    TopN_oi_df.loc["long_potion_rate",:].plot.bar(ax=axis,color=['red'])
    TopN_oi_df.loc["short_position_rate",:].plot.bar(ax=axis,color=['green']) 
    TopN_oi_df.loc["net_position_rate",:].plot(ax=axis)
    axis.axhline(0, color='k')
    
    
    