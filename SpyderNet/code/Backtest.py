# -*- coding: utf-8 -*-
"""
Created on Fri Mar 09 09:27:06 2018

@author: 李弘一萌
"""
import pandas as pd


################################################################################################
#                                                                                              #
#                                          回测模块                                             #
#                                                                                              #
################################################################################################


###############################################################################
def OI_Strat_Bktest(signal,main_cnt_list,price_table,fee_rate=0):
    signal.name = "signal"
    main_cnt_list.name = "main_cnt"
    signal.dropna(inplace=True)
    main_cnt_list.dropna(inplace=True)
    signal_and_cnt = pd.concat([signal,main_cnt_list],axis=1)
    signal_and_cnt.dropna(inplace=True)
    signal_and_price_table = pd.concat([signal_and_cnt,price_table],axis=1) 
    return Bktest_ret(signal_and_price_table["signal"].shift(1),signal_and_price_table["open"],signal_and_price_table["close"],fee_rate)
    
    
def Bktest_ret(signal,open_price,close_price,fee_rate):
    signal.name = "signal"
    open_price.name = "open"
    close_price.name = "close"
    table = pd.concat([signal,open_price,close_price],axis=1)
    table.dropna(inplace=True)
    original_ret = table["close"] / table["open"] - 1
    fee = fee_rate * (table["close"] / table["open"] - 1)
    strat_ret = original_ret * table["signal"] - fee
    strat_ret.name = "ret"
    equity = strat_ret.apply(lambda x:(x+1)).cumprod()
    equity.name = "equity"    
    ret_equity = pd.concat([strat_ret,equity],axis=1)
    return ret_equity

###############################################################################    