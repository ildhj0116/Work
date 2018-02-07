# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 13:34:00 2018

@author: 李弘一萌
"""
import pandas as pd
from WindPy import w
w.start() 


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


def MainCnt_trade_start_end(cnt_series):
    cnt_unique = cnt_series.dropna().unique()
    start_date_list = []
    end_date_list = []
    for cnt in cnt_unique:
        tmp_date_list = cnt_series[cnt_series==cnt].index.tolist()
        start_date_list.append(tmp_date_list[0])
        end_date_list.append(tmp_date_list[-1])
    df = pd.DataFrame([start_date_list,end_date_list],index=["start_date","end_date"],columns=cnt_unique).T    
    return df

def Bktest(signal,open_price,close_price):
    signal.name = "signal"
    open_price.name = "open"
    close_price.name = "close"
    table = pd.concat([signal,open_price,close_price],axis=1).dropna(inplace=True)
    original_ret = table["close"] / table["open"] - 1
    strat_ret = original_ret * table["signal"]
    strat_ret.name = "ret"
    equity = strat_ret.apply(lambda x:(x+1)).cumprod()
    equity.name = "equity"    
    ret_equity = pd.concat([strat_ret,equity],axis=1)
    return ret_equity
    
    
    
def SpyderNet_Bktest(signal,main_cnt_list,start_date,end_date):
    open_list = main_cnt_list.shift(1)
    close_list = main_cnt_list.shift(2)
    open_trade_date_table = MainCnt_trade_start_end(open_list)
    close_trade_date_table = MainCnt_trade_start_end(close_list)
    cnt_unique = open_list.dropna().unique()
    open_price_list = []
    close_price_list = []
    for cnt in cnt_unique:
        tmp_open = w.wsd(cnt,"open",open_trade_date_table.loc[cnt,"start_date"],\
                         open_trade_date_table.loc[cnt,"end_date"],"") 
        tmp_open = pd.DataFrame(tmp_open.Data,index=["open"],columns=tmp_open.Times).T
        tmp_open["open_cnt"] = [cnt]*len(tmp_open.index)
        tmp_close = w.wsd(cnt,"close",close_trade_date_table.loc[cnt,"start_date"],\
                         close_trade_date_table.loc[cnt,"end_date"],"") 
        tmp_close = pd.DataFrame(tmp_close.Data,index=["close"],columns=tmp_close.Times).T
        tmp_close["close_cnt"] = [cnt]*len(tmp_close.index)    
        open_price_list.append(tmp_open)
        close_price_list.append(tmp_close)
    open_price_table = pd.concat(open_price_list)
    close_price_table = pd.concat(close_price_list)
    price_table = pd.concat([open_price_table,close_price_table],axis=1)
    signal.name = "signal"
    main_cnt_list.name = "main_cnt"
    signal.dropna(inplace=True)
    main_cnt_list.dropna(inplace=True)
    signal_and_cnt = pd.concat([signal,main_cnt_list],axis=1)
    signal_and_cnt.dropna(inplace=True)
    signal_and_price_table = pd.concat([signal_and_cnt,price_table],axis=1)
    original_ret = signal_and_price_table["close"] / signal_and_price_table["open"].shift(1) - 1
    strat_ret = (original_ret.dropna()) * (signal_and_price_table["signal"].shift(2).dropna())
    # 回测函数框架？
    ret_equity = Bktest(signal_and_price_table["signal"].shift(2),)
    return equity
    
    
    
    
    
    
    
    
    
    
    
        
if __name__ =="__main__":
    main_cnt_df = pd.read_csv("main_cnt_revised.csv",parse_dates=[0],index_col=0)
    ###########################################################################
    
#    all_df = pd.read_pickle("OI.tmp")
#    ITS_signal,UTS_signal = signal_spyder_for_index(all_df)
#    ITS_signal.to_csv("signals\ITS_signals.csv")
#    UTS_signal.to_csv("signals\UTS_signals.csv")

    #测试下一个模块
    ITS_signal = pd.read_csv("signals\ITS_signals.csv",parse_dates=[0],index_col=0)
    UTS_signal = pd.read_csv("signals\UTS_signals.csv",parse_dates=[0],index_col=0)
    ###########################################################################
    #cmt_list = main_cnt_df.columns.tolist()
    cmt_list = ["CS.DCE"]
    for cmt in cmt_list:
        if cmt not in ITS_signal.columns:
            continue
        else:
            equity = SpyderNet_Bktest(ITS_signal[cmt],main_cnt_df[cmt],1,1)
    
















