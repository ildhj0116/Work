# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 09:08:52 2018

@author: Administrator
"""

import pandas as pd
import os

main_cnt_df = pd.read_csv("../../Futures_data/main_cnt/data/main_cnt_total.csv",index_col=0,parse_dates=[0])

def ret_tommorrow(date,cmt,tommorrow):
    main_cnt = main_cnt_df.loc[tommorrow,cmt]
    tmp_cl = pd.read_csv("../../Futures_data/data_cl/"+cmt[:-4]+".csv",index_col=0,parse_dates=[0])
    i = tmp_cl.index.get_loc(tommorrow)
    ret = tmp_cl.loc[:,main_cnt].iloc[i] / tmp_cl.loc[:,main_cnt].iloc[i-1] - 1
    return ret
    

def adding_ret(df,cmt_list_chinese,tommorrow):
    col = df.columns.tolist()
    col1 = ["cmt"]*len(col)
    df.columns = pd.MultiIndex.from_tuples(list(zip(col,col1)))
    new_columns = []
    for item in col:
        df[(item,"ret")] = [0]*5
        tmp_cmt = df.loc[:,(item,"cmt")].tolist() 
        for i in range(len(tmp_cmt)):
            cmt_e = cmt_list_chinese.loc[tmp_cmt[i]].iloc[0]
            df[(item,"ret")].iloc[i] = ret_tommorrow(df.index[0],cmt_e,tommorrow)
        new_columns.extend([(item,"cmt"),(item,"ret")])
    df = df[new_columns]
    return df
    
    
    
if __name__ == "__main__":
    cmt_list_chinese = pd.read_csv("../../Futures_data/cmt_list/cmt_list_with_Chinese.csv",index_col=1,encoding='gb2312')
    date_list = pd.read_csv("../../Futures_Data/others/trade_date.csv",index_col=0,parse_dates=[0])
    date_list = date_list.index[-69:].tolist()
    counter = 0
    head_list = []
    tail_list = []
    for tdate in date_list[:-1]:
        tmp_head = pd.read_csv("../output/Daily/"+tdate.to_pydatetime().strftime("%Y-%m-%d")+"/head.csv",index_col=0,encoding="utf_8_sig")
        tmp_tail = pd.read_csv("../output/Daily/"+tdate.to_pydatetime().strftime("%Y-%m-%d")+"/tail.csv",index_col=0,encoding="utf_8_sig")
        tmp_head.index = [tdate]*len(tmp_head)
        tmp_tail.index = [tdate]*len(tmp_tail)
        tommorrow = date_list[counter+1]
        tmp_head = adding_ret(tmp_head,cmt_list_chinese,tommorrow)
        tmp_tail = adding_ret(tmp_tail,cmt_list_chinese,tommorrow)
        head_list.append(tmp_head)
        tail_list.append(tmp_tail)
        counter += 1
        print tdate
    head_all = pd.concat(head_list)
    tail_all = pd.concat(tail_list)
    head_all.to_csv("head_all.csv",encoding="utf_8_sig")    
    tail_all.to_csv("tail_all.csv",encoding="utf_8_sig")
        
        
        