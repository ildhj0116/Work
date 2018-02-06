# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 13:34:00 2018

@author: 李弘一萌
"""
import pandas as pd



def signal_spyder_for_index(all_df):
    cmt_list =all_df.columns.tolist()
    target_cmt_list = cmt_list
    cmt_ITS_series_list = []
    cmt_UTS_series_list = []
    
    for cmt in target_cmt_list:
        if cmt not in cmt_list:
            print cmt+"不存在"
            continue
        else:
            cmt_oi_series = all_df[cmt].copy()
            cmt_oi_series.dropna(inplace=True)
            cmt_ITS_list = []
            cmt_UTS_list = []
            for i in range(len(cmt_oi_series)):
                tmp_oi_df = cmt_oi_series[i]
                if len(tmp_oi_df)<=2:
                    ITS=0
                    UTS=0
                else:                    
                    tmp_oi_df["Stat"] = (tmp_oi_df["long_position"]+tmp_oi_df["short_position"])/tmp_oi_df["vol"]
                    total_oi = tmp_oi_df.drop("date",axis=1).sum()
                    total_stat = (total_oi.loc["long_position"]+total_oi.loc["short_position"])/total_oi.loc["vol"]
                    informed_trader = tmp_oi_df[tmp_oi_df["Stat"]>=total_stat]
                    uninformed_trader = tmp_oi_df[tmp_oi_df["Stat"]<total_stat]
                    IT_B = informed_trader["long_position"].sum()
                    IT_S = informed_trader["short_position"].sum()                    
                    UT_B = uninformed_trader["long_position"].sum()
                    UT_S = uninformed_trader["short_position"].sum()
                    if ((IT_B+IT_S)==0) or ((UT_B+UT_S)==0):
                        ITS = 0
                        UTS = 0
                    else:
                        ITS = (IT_B-IT_S)/(IT_B+IT_S)
                        UTS = (UT_B-UT_S)/(UT_B+UT_S)
                cmt_ITS_list.append(ITS)
                cmt_UTS_list.append(UTS)
            cmt_ITS_series = pd.Series(cmt_ITS_list,index=cmt_oi_series.index,name=cmt)
            cmt_UTS_series = pd.Series(cmt_UTS_list,index=cmt_oi_series.index,name=cmt)
            cmt_ITS_series_list.append(cmt_ITS_series)
            cmt_UTS_series_list.append(cmt_UTS_series)
    
    cmt_ITS_df = pd.concat(cmt_ITS_series_list,axis=1) 
    cmt_UTS_df = pd.concat(cmt_UTS_series_list,axis=1) 
    cmt_ITS_signal_df = pd.DataFrame(0,index=cmt_ITS_df.index,columns=cmt_ITS_df.columns)
    cmt_ITS_signal_df[cmt_ITS_df>0]= 1
    cmt_ITS_signal_df[cmt_ITS_df<0]= -1
    cmt_UTS_signal_df = pd.DataFrame(0,index=cmt_UTS_df.index,columns=cmt_UTS_df.columns)
    cmt_UTS_signal_df[cmt_UTS_df>0]= -1
    cmt_UTS_signal_df[cmt_UTS_df<0]= 1
    return cmt_ITS_signal_df, cmt_UTS_signal_df



def SpyderNet_Bktest(signal,main_cnt_list,start_date,end_date):
    open_list = main_cnt_list.shift(1)
    close_list = main_cnt_list.shift(2)
    date_list = main_cnt_list.index.tolist()
    
    
    
    
    
    
if __name__ =="__main__":
    all_df = pd.read_pickle("OI.tmp")
    main_cnt_df = pd.read_csv("main_cnt_test.csv",index_col=0)
    a,b = signal_spyder_for_index(all_df)


















