# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:38:12 2018

@author: Administrator
"""

import pandas as pd


if __name__ == "__main__":
    head = pd.read_csv("head_all.csv",index_col=0,header=[0,1],encoding="utf_8_sig")
    tail = pd.read_csv("tail_all.csv",index_col=0,header=[0,1],encoding="utf_8_sig")
    l_date_list = []
    l_cmt_list = []
    l_ret_list = []
    s_date_list = []
    s_cmt_list = []
    s_ret_list = []
#    head_mean = head.mean()
#    head_mean.index = head_mean.index.get_level_values(0)
#    head_mean.name = u"排名前五"
#    tail_mean = tail.mean()
#    tail_mean.index = tail_mean.index.get_level_values(0)
#    tail_mean.name = u"排名后五"
#    daily_ret_mean = pd.concat([head_mean,tail_mean],axis=1)
#    daily_ret_mean.to_csv("daily_ret.csv",encoding="utf_8_sig")
    for tdate,head_group in head.groupby(head.index):
        tail_group = tail[tail.index==tdate]
        long_head = head_group.loc[:,("日多头持仓占比变化".decode("utf_8_sig"),"cmt")].tolist()
        short_tail = tail_group.loc[:,("日空头持仓占比变化".decode("utf_8_sig"),"cmt")].tolist()
        short_head = head_group.loc[:,("日空头持仓占比变化".decode("utf_8_sig"),"cmt")].tolist()
        long_tail = tail_group.loc[:,("日多头持仓占比变化".decode("utf_8_sig"),"cmt")].tolist()
        ret_head = head_group.loc[:,("1日收益".decode("utf_8_sig"),"cmt")].tolist()
        ret_tail = tail_group.loc[:,("1日收益".decode("utf_8_sig"),"cmt")].tolist()
        
        
        inter_long = list(set(short_tail).intersection(set(ret_head)))
        inter_short = list(set(long_tail).intersection(set(ret_tail)))
        if len(inter_long) != 0:
            for cmt in inter_long:
                tmp_df = head_group[head_group.loc[:,("日多头持仓占比变化".decode("utf_8_sig"),"cmt")]==cmt]
                ret = tmp_df.loc[:,("日多头持仓占比变化".decode("utf_8_sig"),"ret")].iloc[0]
                l_date_list.append(tdate)
                l_cmt_list.append(cmt)
                l_ret_list.append(ret)
        if len(inter_short) != 0:
            for cmt in inter_short:
                tmp_df = head_group[head_group.loc[:,("日空头持仓占比变化".decode("utf_8_sig"),"cmt")]==cmt]
                ret = tmp_df.loc[:,("日空头持仓占比变化".decode("utf_8_sig"),"ret")].iloc[0]
                s_date_list.append(tdate)
                s_cmt_list.append(cmt)
                s_ret_list.append(ret)
    inter_long_df = pd.DataFrame([l_date_list,l_cmt_list,l_ret_list],index=["date","cmt","return"]).T
    inter_short_df = pd.DataFrame([s_date_list,s_cmt_list,s_ret_list],index=["date","cmt","return"]).T
    print "多头收益:" + str(inter_long_df["return"].mean())
    print "空头收益:" + str(inter_short_df["return"].mean())
#    inter_long_df.to_csv("long.csv",encoding="utf_8_sig")
#    inter_short_df.to_csv("short.csv",encoding="utf_8_sig")
#    