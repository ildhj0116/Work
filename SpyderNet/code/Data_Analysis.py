# -*- coding: utf-8 -*-
"""
Created on Fri Mar 09 09:35:28 2018

@author: Administrator
"""
import pandas as pd
from Main import OI_Data_Import
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


def Length_of_OI_Table(original_cmt_list):
    len_series_list = []
    for cmt in original_cmt_list:
        try:
            #导入指定品种主力合约会员持仓数据列表及当日该合约总持仓量列表
            cmt_oi,total_vol_oi_df = OI_Data_Import(cmt)
        except IOError as e:
            #处理不存在该品种持仓数据的情况
            print cmt + "持仓数据导入失败: " + e.strerror            
        else:
            cmt_oi_series = cmt_oi
            len_list = []
            for i in range(len(cmt_oi_series)):
                tmp_oi_df = cmt_oi_series[i]
                len_list.append(len(tmp_oi_df))
            len_series = pd.Series(len_list,index=cmt_oi_series.index,name=cmt)
            len_series_list.append(len_series)
    len_df = pd.concat(len_series_list,axis=1)      
    return len_df

if __name__ =="__main__":
    ###########################################################################
    #数据准备
    
    #导入主力合约时间序列
    main_cnt_df = pd.read_csv("../../Futures_Data/main_cnt/data/main_cnt_total.csv",parse_dates=[0],index_col=0)
    len_df = Length_of_OI_Table(main_cnt_df.columns.tolist())
    
    
  