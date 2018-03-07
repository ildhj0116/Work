# -*- coding: utf-8 -*-
"""
Created on Wed Mar 07 16:38:36 2018

@author: 李弘一萌
"""


import pandas as pd


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

def Price_Generation(main_cnt_list,start_date,end_date):
    trade_date_table = MainCnt_trade_start_end(open_list)
    cnt_unique = open_list.dropna().unique()
    open_price_list = []
    close_price_list = []
    open_interest_list = []
    volume_list = []
    for cnt in cnt_unique:
        tmp_open = w.wsd(cnt,"open",trade_date_table.loc[cnt,"start_date"],\
                         trade_date_table.loc[cnt,"end_date"],"") 
        tmp_open = pd.DataFrame(tmp_open.Data,index=["open"],columns=tmp_open.Times).T
        tmp_open["open_cnt"] = [cnt]*len(tmp_open.index)
        tmp_close = w.wsd(cnt,"close",trade_date_table.loc[cnt,"start_date"],\
                         trade_date_table.loc[cnt,"end_date"],"") 
        tmp_close = pd.DataFrame(tmp_close.Data,index=["close"],columns=tmp_close.Times).T
        tmp_close["close_cnt"] = [cnt]*len(tmp_close.index)
        tmp_oi = w.wsd(cnt,"oi",trade_date_table.loc[cnt,"start_date"],\
                         trade_date_table.loc[cnt,"end_date"],"") 
        tmp_oi = pd.DataFrame(tmp_oi.Data,index=["oi"],columns=tmp_oi.Times).T
        tmp_oi["oi_cnt"] = [cnt]*len(tmp_oi.index)  
        tmp_volume = w.wsd(cnt,"volume",trade_date_table.loc[cnt,"start_date"],\
                         trade_date_table.loc[cnt,"end_date"],"") 
        tmp_volume = pd.DataFrame(tmp_volume.Data,index=["close"],columns=tmp_volume.Times).T
        tmp_volume["volume_cnt"] = [cnt]*len(tmp_volume.index)  
        open_price_list.append(tmp_open)
        close_price_list.append(tmp_close)
        open_interest_list.append(tmp_open)
        volume_list.append(tmp_close)
    open_price_table = pd.concat(open_price_list)
    close_price_table = pd.concat(close_price_list)
    open_interest_table = pd.concat(open_price_list)
    close_price_table = pd.concat(close_price_list)
    price_table = pd.concat([open_price_table,close_price_table],axis=1)   
    return price_table

###############################################################################
if __name__ == "__main__":
    
    
    
    
    
    
    
    
    
    
    


