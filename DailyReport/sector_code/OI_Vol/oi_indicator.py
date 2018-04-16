# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 15:21:46 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
from WindPy import w
#from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def color_setting(ret):
    colors = ['r' if x>0 else 'g' for x in ret]
    return colors
m_cmt = ["IC.CFE","IF.CFE","IH.CFE","T.CFE","TF.CFE"]



def position_rank_api(cmt,main_cnt_list_today,relative_data_path,compute_date_str,last_days):
    Tday_1d = last_days[0]
    Tday_1w = last_days[1]
    Tday_1m = last_days[2]
    main_cnt = main_cnt_list_today.loc[cmt]
    tmp_vol = pd.read_csv(relative_data_path + "/data_vol/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
    tmp_oi = pd.read_csv(relative_data_path + "/data_oi/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
    tmp_oi_rank = w.wset("futureoir","startdate="+compute_date_str+";enddate="+compute_date_str+\
                         ";varity="+cmt+";wind_code="+main_cnt+";order_by=long;ranks=all;field="+\
                         "member_name,long_potion_rate,short_position_rate,net_position_rate")                        
    tmp_oi_rank = pd.DataFrame(tmp_oi_rank.Data, index=tmp_oi_rank.Fields).T    
    
    tmp_oi_rank_d = w.wset("futureoir","startdate="+Tday_1d+";enddate="+Tday_1d+\
                         ";varity="+cmt+";wind_code="+main_cnt+";order_by=long;ranks=all;field="+\
                         "member_name,long_potion_rate,short_position_rate")                        
    tmp_oi_rank_d = pd.DataFrame(tmp_oi_rank_d.Data, index=tmp_oi_rank_d.Fields).T
    
    tmp_oi_rank_w = w.wset("futureoir","startdate="+Tday_1w+";enddate="+Tday_1w+\
                         ";varity="+cmt+";wind_code="+main_cnt+";order_by=long;ranks=all;field="+\
                         "member_name,long_potion_rate,short_position_rate")                        
    tmp_oi_rank_w = pd.DataFrame(tmp_oi_rank_w.Data, index=tmp_oi_rank_w.Fields).T 
    
    tmp_oi_rank_m = w.wset("futureoir","startdate="+Tday_1m+";enddate="+Tday_1m+\
                         ";varity="+cmt+";wind_code="+main_cnt+";order_by=long;ranks=all;field="+\
                         "member_name,long_potion_rate,short_position_rate")                        
    tmp_oi_rank_m = pd.DataFrame(tmp_oi_rank_m.Data, index=tmp_oi_rank_m.Fields).T 
    
    main_cnt_vol = tmp_vol[main_cnt].dropna().copy()
    main_cnt_vol.name = cmt
    main_cnt_oi = tmp_oi[main_cnt].dropna().copy()
    main_cnt_oi.name = cmt
    if len(tmp_oi_rank) == 0:
        long_1d = np.nan
        short_1d = np.nan
        long_1w = np.nan
        short_1w = np.nan
        long_1m = np.nan
        short_1m = np.nan
        TopN_oi_rate_series = pd.Series([np.nan,np.nan,np.nan],index=["long_potion_rate","short_position_rate","net_position_rate"],
                                        name=cmt)
    else:
        TopN_oi_rate_series = tmp_oi_rank.iloc[1,:]
        TopN_oi_rate_series.loc["short_position_rate"] = -TopN_oi_rate_series.loc["short_position_rate"]
        TopN_oi_rate_series.loc["net_position_rate"] = TopN_oi_rate_series["long_potion_rate"] + TopN_oi_rate_series["short_position_rate"]
        TopN_oi_rate_series.name = cmt
    
        if len(tmp_oi_rank_d) == 0:
            long_1d = np.nan
            short_1d = np.nan
        else:            
            long_1d = TopN_oi_rate_series["long_potion_rate"] / tmp_oi_rank_d.loc[1,"long_potion_rate"] - 1
            short_1d = -TopN_oi_rate_series["short_position_rate"] / tmp_oi_rank_d.loc[1,"short_position_rate"] - 1
        if len(tmp_oi_rank_w) == 0:
            long_1w = np.nan
            short_1w = np.nan
        else:                
            long_1w = TopN_oi_rate_series["long_potion_rate"] / tmp_oi_rank_w.loc[1,"long_potion_rate"] - 1
            short_1w = -TopN_oi_rate_series["short_position_rate"] / tmp_oi_rank_w.loc[1,"short_position_rate"] - 1
        if len(tmp_oi_rank_m) == 0:
            long_1m = np.nan
            short_1m = np.nan
        else:
            long_1m = TopN_oi_rate_series["long_potion_rate"] / tmp_oi_rank_m.loc[1,"long_potion_rate"] - 1
            short_1m = -TopN_oi_rate_series["short_position_rate"] / tmp_oi_rank_m.loc[1,"short_position_rate"] - 1
    rate_pchg_series = pd.Series([long_1d,long_1w,long_1m,short_1d,short_1w,short_1m],index=
                                 ["long_1d","long_1w","long_1m","short_1d","short_1w","short_1m"],name=cmt)
    return TopN_oi_rate_series,rate_pchg_series

def position_rank_local(cmt,relative_data_path,compute_date_str,last_days):
    Tday_1d = last_days[0]
    Tday_1w = last_days[1]
    Tday_1m = last_days[2]
                     
    tmp_oi_rank = pd.read_csv(relative_data_path+"/position_rank/cmt/"+compute_date_str+"/"+cmt[:-4]+".csv",encoding="utf_8_sig",
                              index_col=0)
    tmp_oi_rank_d = pd.read_csv(relative_data_path+"/position_rank/cmt/"+Tday_1d+"/"+cmt[:-4]+".csv",encoding="utf_8_sig",
                              index_col=0)    
    tmp_oi_rank_w = pd.read_csv(relative_data_path+"/position_rank/cmt/"+Tday_1w+"/"+cmt[:-4]+".csv",encoding="utf_8_sig",
                              index_col=0)
    tmp_oi_rank_m = pd.read_csv(relative_data_path+"/position_rank/cmt/"+Tday_1m+"/"+cmt[:-4]+".csv",encoding="utf_8_sig",
                              index_col=0)    
    
    if len(tmp_oi_rank) == 0:
        long_1d = np.nan
        short_1d = np.nan
        long_1w = np.nan
        short_1w = np.nan
        long_1m = np.nan
        short_1m = np.nan
    else:
        TopN_oi_rate_series = tmp_oi_rank.loc[u"前十名合计",:]
        TopN_oi_rate_series.loc["short_position_rate"] = -TopN_oi_rate_series.loc["short_position_rate"]
        TopN_oi_rate_series.loc["net_position_rate"] = TopN_oi_rate_series["long_potion_rate"] + TopN_oi_rate_series["short_position_rate"]
        TopN_oi_rate_series.name = cmt
    
        if len(tmp_oi_rank_d) == 0:
            long_1d = np.nan
            short_1d = np.nan
        else:            
            long_1d = TopN_oi_rate_series["long_potion_rate"] / tmp_oi_rank_d.loc[u"前十名合计","long_potion_rate"] - 1
            short_1d = -TopN_oi_rate_series["short_position_rate"] / tmp_oi_rank_d.loc[u"前十名合计","short_position_rate"] - 1
        if len(tmp_oi_rank_w) == 0:
            long_1w = np.nan
            short_1w = np.nan
        else:                
            long_1w = TopN_oi_rate_series["long_potion_rate"] / tmp_oi_rank_w.loc[u"前十名合计","long_potion_rate"] - 1
            short_1w = -TopN_oi_rate_series["short_position_rate"] / tmp_oi_rank_w.loc[u"前十名合计","short_position_rate"] - 1
        if len(tmp_oi_rank_m) == 0:
            long_1m = np.nan
            short_1m = np.nan
        else:
            long_1m = TopN_oi_rate_series["long_potion_rate"] / tmp_oi_rank_m.loc[u"前十名合计","long_potion_rate"] - 1
            short_1m = -TopN_oi_rate_series["short_position_rate"] / tmp_oi_rank_m.loc[u"前十名合计","short_position_rate"] - 1
    rate_pchg_series = pd.Series([long_1d,long_1w,long_1m,short_1d,short_1w,short_1m],index=
                                 ["long_1d","long_1w","long_1m","short_1d","short_1w","short_1m"],name=cmt)
    return TopN_oi_rate_series,rate_pchg_series



        
def vol_oi_indicator(main_cnt_list_today,cmt_list,compute_date_str,relative_data_path):
    fig_list = []
    vol_series_list = []
    oi_series_list = []
    TopN_oi_series_list = []
    oi_rank_pchg_series_list = []
    Tday_1d = w.tdaysoffset(-1, compute_date_str, "TradingCalendar=SHFE")
    Tday_1d = Tday_1d.Data[0][0].strftime("%Y-%m-%d")
    Tday_1w = w.tdaysoffset(-5, compute_date_str, "TradingCalendar=SHFE")
    Tday_1w = Tday_1w.Data[0][0].strftime("%Y-%m-%d")
    Tday_1m = w.tdaysoffset(-20, compute_date_str, "TradingCalendar=SHFE")
    Tday_1m = Tday_1m.Data[0][0].strftime("%Y-%m-%d")
    last_days = [Tday_1d, Tday_1w, Tday_1m]
    for cmt in cmt_list.index.tolist():
        if cmt in m_cmt:
            continue
        else:
            tmp_vol = pd.read_csv(relative_data_path + "/data_vol/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
            tmp_oi = pd.read_csv(relative_data_path + "/data_oi/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
            main_cnt = main_cnt_list_today.loc[cmt]                
            TopN_oi_rate_series,rate_pchg_series = position_rank_local(cmt,relative_data_path,compute_date_str,last_days)            
            main_cnt_vol = tmp_vol[main_cnt].dropna().copy()
            main_cnt_vol.name = cmt
            main_cnt_oi = tmp_oi[main_cnt].dropna().copy()
            main_cnt_oi.name = cmt
            vol_series_list.append(main_cnt_vol)
            oi_series_list.append(main_cnt_oi)
            TopN_oi_series_list.append(TopN_oi_rate_series)
            oi_rank_pchg_series_list.append(rate_pchg_series)
        
    vol_df = pd.concat(vol_series_list,axis=1)
    oi_df = pd.concat(oi_series_list,axis=1)
    TopN_oi_df = pd.concat(TopN_oi_series_list,axis=1)
    TopN_oi_df.columns = cmt_list.loc[TopN_oi_df.columns.tolist(),:]["Chinese"].tolist()
    oi_rank_pchg_df = pd.concat(oi_rank_pchg_series_list,axis=1)
    oi_rank_long_1d = oi_rank_pchg_df.loc["long_1d",:].dropna().copy()
    oi_rank_long_1w = oi_rank_pchg_df.loc["long_1w",:].dropna().copy()
    oi_rank_long_1m = oi_rank_pchg_df.loc["long_1m",:].dropna().copy()
    oi_rank_short_1d = oi_rank_pchg_df.loc["short_1d",:].dropna().copy()
    oi_rank_short_1w = oi_rank_pchg_df.loc["short_1w",:].dropna().copy()
    oi_rank_short_1m = oi_rank_pchg_df.loc["short_1m",:].dropna().copy()
    oi_rank_long_1d.sort_values(ascending=False,inplace=True)
    oi_rank_long_1w.sort_values(ascending=False,inplace=True)
    oi_rank_long_1m.sort_values(ascending=False,inplace=True)
    oi_rank_short_1d.sort_values(ascending=False,inplace=True)
    oi_rank_short_1w.sort_values(ascending=False,inplace=True)
    oi_rank_short_1m.sort_values(ascending=False,inplace=True)
    oi_rank_long_1d.index = cmt_list.loc[oi_rank_long_1d.index.tolist(),:]["Chinese"].tolist()
    oi_rank_long_1w.index = cmt_list.loc[oi_rank_long_1w.index.tolist(),:]["Chinese"].tolist()
    oi_rank_long_1m.index = cmt_list.loc[oi_rank_long_1m.index.tolist(),:]["Chinese"].tolist()
    oi_rank_short_1d.index = cmt_list.loc[oi_rank_short_1d.index.tolist(),:]["Chinese"].tolist()
    oi_rank_short_1w.index = cmt_list.loc[oi_rank_short_1w.index.tolist(),:]["Chinese"].tolist()
    oi_rank_short_1m.index = cmt_list.loc[oi_rank_short_1m.index.tolist(),:]["Chinese"].tolist()
    head_oi_rank_long_1d = oi_rank_long_1d.head().index.tolist()
    tail_oi_rank_long_1d = list(reversed(oi_rank_long_1d.tail().index.tolist()))
    head_oi_rank_short_1d = oi_rank_short_1d.head().index.tolist()
    tail_oi_rank_short_1d = list(reversed(oi_rank_short_1d.tail().index.tolist()))
    head_oi_rank_long_1w = oi_rank_long_1w.head().index.tolist()
    tail_oi_rank_long_1w = list(reversed(oi_rank_long_1w.tail().index.tolist()))
    head_oi_rank_short_1w = oi_rank_short_1w.head().index.tolist()
    tail_oi_rank_short_1w = list(reversed(oi_rank_short_1w.tail().index.tolist()))
    head_oi_rank_long_1m = oi_rank_long_1m.head().index.tolist()
    tail_oi_rank_long_1m = list(reversed(oi_rank_long_1m.tail().index.tolist()))
    head_oi_rank_short_1m = oi_rank_short_1m.head().index.tolist()
    tail_oi_rank_short_1m = list(reversed(oi_rank_short_1m.tail().index.tolist()))
    #成交、持仓量变化比率
    vol_chg_df = (vol_df - vol_df.shift(1)) / vol_df.shift(1)
    vol_chg = vol_chg_df.iloc[-1,:]    
    vol_chg_positive = vol_chg[vol_chg>0].copy()
    vol_chg_negative = vol_chg[vol_chg<0].copy()
    vol_chg_positive.sort_values(ascending=False,inplace=True)
    vol_chg_negative.sort_values(ascending=True,inplace=True)
    vol_chg_positive.index = cmt_list.loc[vol_chg_positive.index.tolist(),:]["Chinese"].tolist()
    vol_chg_negative.index = cmt_list.loc[vol_chg_negative.index.tolist(),:]["Chinese"].tolist()
    head_vol_chg_positive = vol_chg_positive.head().index.tolist()
    tail_vol_chg_negative = vol_chg_negative.head().index.tolist()

    
    stat_head_df = pd.DataFrame([head_vol_chg_positive,head_oi_rank_long_1d,head_oi_rank_short_1d,head_oi_rank_long_1w,
                                 head_oi_rank_short_1w,head_oi_rank_long_1m,head_oi_rank_short_1m],index=[u"成交量变化",u"日多头持仓占比变化",
                                u"日空头持仓占比变化",u"周多头持仓占比变化",u"周空头持仓占比变化",u"月多头持仓占比变化",u"月空头持仓占比变化"]).T
    stat_tail_df = pd.DataFrame([tail_vol_chg_negative,tail_oi_rank_long_1d,tail_oi_rank_short_1d,tail_oi_rank_long_1w,
                                 tail_oi_rank_short_1w,tail_oi_rank_long_1m,tail_oi_rank_short_1m],index=[u"成交量变化",u"日多头持仓占比变化",
                                u"日空头持仓占比变化",u"周多头持仓占比变化",u"周空头持仓占比变化",u"月多头持仓占比变化",u"月空头持仓占比变化"]).T
    #换手率
#    turn = vol_df.iloc[-1,:] / oi_df.iloc[-1,:]
#    turn.sort_values(ascending=False,inplace=True)
#    turn.index = cmt_list.loc[turn.index.tolist(),:]["Chinese"].tolist()
    
            
    #画图
    #成交手数变化    
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    vol_chg_positive.plot.bar(ax=axis,color=['red'])
    axis.axhline(0, color='k')
    plt.xticks(rotation=0)
    axis.grid(axis='y',which="both",linestyle='--')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"增幅",fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    plt.title(u"品种成交手数增加幅度排名",fontsize=20)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    fig_list.append(fig)
    
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    vol_chg_negative.plot.bar(ax=axis,color=['green'])
    axis.axhline(0, color='k')
    plt.xticks(rotation=0)
    axis.grid(axis='y',which="both",linestyle='--')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"减幅",fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    plt.title(u"品种成交手数减少幅度排名",fontsize=20)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    fig_list.append(fig)
    
    #换手率
#    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
#    axis = fig.add_subplot(111)
#    turn.plot.bar(ax=axis)
#    plt.xticks(rotation=0)
#    axis.grid(axis='y',which="both",linestyle='--')
#    axis.axhline(0, color='k')
#    plt.xlabel(u"品种",fontsize=15)
#    plt.ylabel(u"换手率",fontsize=15)
#    plt.xticks(fontsize=12)
#    plt.yticks(fontsize=15)
#    plt.title(u"品种日换手率",fontsize=20)
#    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
#    fig_list.append(fig)
    
    #前十持仓比例
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    TopN_oi_df.loc["long_potion_rate",:].plot.bar(ax=axis,color=['red'],label=u"多头")
    TopN_oi_df.loc["short_position_rate",:].plot.bar(ax=axis,color=['green'],label=u"空头") 
    TopN_oi_df.loc["net_position_rate",:].plot(ax=axis,label=u"净头寸",linewidth=2,color="blue")
    axis.grid(which="both",linestyle='--')
    axis.axhline(0, color='k')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"持仓量占比",fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    plt.title(u"排名前十会员持仓占比",fontsize=20)
    plt.legend()
    fig_list.append(fig)
    
    #
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    oi_rank_long_1d.plot.bar(ax=axis,color=[tuple(color_setting(oi_rank_long_1d))])
    axis.axhline(0, color='k')
    plt.xticks(rotation=0)
    axis.grid(which="both",linestyle='--')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"增幅",fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    plt.title(u"排名前十会员持多头占比1日增幅",fontsize=20)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    fig_list.append(fig)
    
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    oi_rank_long_1w.plot.bar(ax=axis,color=[tuple(color_setting(oi_rank_long_1w))])
    axis.axhline(0, color='k')
    plt.xticks(rotation=0)
    axis.grid(which="both",linestyle='--')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"增幅",fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    plt.title(u"排名前十会员持多头占比1周增幅",fontsize=20)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    fig_list.append(fig)
    
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    oi_rank_long_1m.plot.bar(ax=axis,color=[tuple(color_setting(oi_rank_long_1m))])
    axis.axhline(0, color='k')
    plt.xticks(rotation=0)
    axis.grid(which="both",linestyle='--')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"增幅",fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    plt.title(u"排名前十会员持多头占比1月增幅",fontsize=20)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    fig_list.append(fig)
    
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    oi_rank_short_1d.plot.bar(ax=axis,color=[tuple(color_setting(oi_rank_short_1d))])
    axis.axhline(0, color='k')
    plt.xticks(rotation=0)
    axis.grid(which="both",linestyle='--')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"增幅",fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    plt.title(u"排名前十会员持空头占比1日增幅",fontsize=20)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    fig_list.append(fig)
    
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    oi_rank_short_1w.plot.bar(ax=axis,color=[tuple(color_setting(oi_rank_short_1w))])
    axis.axhline(0, color='k')
    plt.xticks(rotation=0)
    axis.grid(which="both",linestyle='--')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"增幅",fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    plt.title(u"排名前十会员持空头占比1周增幅",fontsize=20)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    fig_list.append(fig)
    
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    oi_rank_short_1m.plot.bar(ax=axis,color=[tuple(color_setting(oi_rank_short_1m))])
    axis.axhline(0, color='k')
    plt.xticks(rotation=0)
    axis.grid(which="both",linestyle='--')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"增幅",fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    plt.title(u"排名前十会员持空头占比1月增幅",fontsize=20)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    fig_list.append(fig)
    return fig_list,stat_head_df,stat_tail_df
    