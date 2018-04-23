# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:38:12 2018

@author: Administrator
"""

import pandas as pd


if __name__ == "__main__":
    head = pd.read_csv("head_all.csv",index_col=0,header=[0,1],encoding="utf_8_sig")
    tail = pd.read_csv("tail_all.csv",index_col=0,header=[0,1],encoding="utf_8_sig")
    for tdate,head_group in head.groupby(head.index):
        tail_group = tail[tail.index==tdate]
        long_head = head_group.loc[:,("日多头持仓占比变化".decode("utf_8_sig"),"cmt")].tolist()
        short_tail = tail_group.loc[:,("日空头持仓占比变化".decode("utf_8_sig"),"cmt")].tolist()
        inter = list(set(long_head).intersection(set(short_tail)))
        if len(inter) != 0:
            for cmt in inter:
                tmp_df = head_group[head_group.loc[:,("日多头持仓占比变化".decode("utf_8_sig"),"cmt")]==cmt]
                ret = tmp_df.loc[:,("日多头持仓占比变化".decode("utf_8_sig"),"ret")].iloc[0]
                
    