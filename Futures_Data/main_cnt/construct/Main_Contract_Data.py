# -*- coding: utf-8 -*-
"""
Created on Wed Mar 07 16:38:36 2018

@author: 李弘一萌
"""

from WindPy import w
import pandas as pd
w.start()

def MainCnt_trade_start_end(cnt_series):
    #返回各主力合约的开始和结束时间
    cnt_unique = cnt_series.dropna().unique()
    start_date_list = []
    end_date_list = []
    for cnt in cnt_unique:
        tmp_date_list = cnt_series[cnt_series==cnt].index.tolist()
        start_date_list.append(tmp_date_list[0])
        end_date_list.append(tmp_date_list[-1])
    df = pd.DataFrame([start_date_list,end_date_list],index=["start_date","end_date"],columns=cnt_unique).T    
    return df

def Price_Generation(main_cnt_list):
    trade_date_table = MainCnt_trade_start_end(main_cnt_list)
    cnt_unique = main_cnt_list.dropna().unique()
    open_price_list = []
    close_price_list = []
    open_interest_list = []
    volume_list = []
    for cnt in cnt_unique:
        tmp_open = w.wsd(cnt,"open",trade_date_table.loc[cnt,"start_date"],\
                         trade_date_table.loc[cnt,"end_date"],"") 
        tmp_open = pd.DataFrame(tmp_open.Data,index=["open"],columns=tmp_open.Times).T
        tmp_close = w.wsd(cnt,"close",trade_date_table.loc[cnt,"start_date"],\
                         trade_date_table.loc[cnt,"end_date"],"") 
        tmp_close = pd.DataFrame(tmp_close.Data,index=["close"],columns=tmp_close.Times).T
        tmp_oi = w.wsd(cnt,"oi",trade_date_table.loc[cnt,"start_date"],\
                         trade_date_table.loc[cnt,"end_date"],"") 
        tmp_oi = pd.DataFrame(tmp_oi.Data,index=["oi"],columns=tmp_oi.Times).T
        tmp_volume = w.wsd(cnt,"volume",trade_date_table.loc[cnt,"start_date"],\
                         trade_date_table.loc[cnt,"end_date"],"") 
        tmp_volume = pd.DataFrame(tmp_volume.Data,index=["volume"],columns=tmp_volume.Times).T
        open_price_list.append(tmp_open)
        close_price_list.append(tmp_close)
        open_interest_list.append(tmp_oi)
        volume_list.append(tmp_volume)
    open_price_table = pd.concat(open_price_list)
    close_price_table = pd.concat(close_price_list)
    open_interest_table = pd.concat(open_interest_list)
    volume_table = pd.concat(volume_list)
    price_table = pd.concat([open_price_table,close_price_table,open_interest_table,volume_table],axis=1)   
    return price_table

###############################################################################
if __name__ == "__main__":
    main_cnt_df = pd.read_csv("../data/main_cnt_total.csv",parse_dates=[0],index_col=0)
    cmt_list = main_cnt_df.columns.tolist()
    open_list = []
    close_list = []
    oi_list = []
    volume_list = []
    for cmt in cmt_list:
        cmt_series = main_cnt_df[cmt]
        price_table = Price_Generation(cmt_series)
        open_series = price_table["open"]
        close_series = price_table["close"]
        oi_series = price_table["oi"]
        volume_series = price_table["volume"]
        open_series.name,close_series.name,oi_series.name,volume_series.name = cmt,cmt,cmt,cmt
        open_list.append(open_series)
        close_list.append(close_series)
        oi_list.append(oi_series)
        volume_list.append(volume_series)
        print cmt + "下载完毕"
    open_df = pd.concat(open_list,axis=1)
    close_df = pd.concat(close_list,axis=1)
    oi_df = pd.concat(oi_list,axis=1)
    volume_df = pd.concat(volume_list,axis=1)
    
    open_df.to_csv("../data/main_cnt_open.csv")
    close_df.to_csv("../data/main_cnt_close.csv")
    oi_df.to_csv("../data/main_cnt_oi.csv")
    volume_df.to_csv("../data/main_cnt_volume.csv")
    
    
    
    
    
    
    
    


