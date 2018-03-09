# -*- coding: utf-8 -*-
"""
Created on Fri Mar 09 09:35:28 2018

@author: Administrator
"""
import pandas as pd
###############################################################################
def Data_Analysis(cmt_oi_series):
    cmt_oi_series.dropna(inplace=True)
    net_long_num = []
    net_short_num = []
    for i in range(len(cmt_oi_series)):
        tmp_oi_df = cmt_oi_series[i]
        tmp_oi_df["net_position"] = tmp_oi_df["long_position"] - tmp_oi_df["short_position"]
        net_long_num.append(tmp_oi_df["net_position"][tmp_oi_df["net_position"]>0].count())
        net_short_num.append(tmp_oi_df["net_position"][tmp_oi_df["net_position"]<0].count())
    net_position_stat = pd.DataFrame([net_long_num,net_short_num],columns=cmt_oi_series.index,index=["net_long","net_short"]).T
    net_position_sum = net_position_stat.sum()
    net_position_stat["net_count_indicator"] = 0
    net_position_stat["net_count_indicator"][net_position_stat["net_short"]>net_position_stat["net_long"]] = -1
    net_position_stat["net_count_indicator"][net_position_stat["net_short"]<net_position_stat["net_long"]] = 1
    #net_position_stat["net_count_indicator"].plot()
    return  