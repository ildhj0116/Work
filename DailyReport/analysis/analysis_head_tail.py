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
    for tdate,head_group in head.groupby(head.index):
        tail_group = tail[tail.index==tdate]
        long_head = head_group.loc[:,("日多头持仓占比变化".decode("utf_8_sig"),"cmt")].tolist()
        short_tail = tail_group.loc[:,("日空头持仓占比变化".decode("utf_8_sig"),"cmt")].tolist()
        short_head = head_group.loc[:,("日空头持仓占比变化".decode("utf_8_sig"),"cmt")].tolist()
        long_tail = tail_group.loc[:,("日多头持仓占比变化".decode("utf_8_sig"),"cmt")].tolist()
        inter_long = list(set(long_head).intersection(set(short_tail)))
        inter_short = list(set(short_head).intersection(set(long_tail)))
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
    