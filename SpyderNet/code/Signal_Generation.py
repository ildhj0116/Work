# -*- coding: utf-8 -*-
"""
Created on Thu Mar 08 16:47:34 2018

@author: 李弘一萌
"""
import pandas as pd

def SpyderNet_1_Signal_Generation(index_name,cmt_index_series,para_lambda):
    cmt = cmt_index_series.name
    if index_name == "ITS":    
        cmt_signal_series = pd.Series(0,index=cmt_index_series.index,name=cmt+"_ITS_signal")
        cmt_signal_series[cmt_index_series>para_lambda]= 1
        cmt_signal_series[cmt_index_series<para_lambda]= -1
    elif index_name == "UTS":
        cmt_signal_series = pd.Series(0,index=cmt_index_series.index,name=cmt+"_UTS_signal")
        cmt_signal_series[cmt_index_series>para_lambda]= -1
        cmt_signal_series[cmt_index_series<para_lambda]= 1 
    return cmt_signal_series


def OI_Factor_Signal_Generation(factor_num,cmt_index_series,para_lambda):
    cmt = cmt_index_series.name 
    cmt_signal_series = pd.Series(0,index=cmt_index_series.index,name=cmt+"OI_factor_"+str(factor_num))
    cmt_signal_series[cmt_index_series>para_lambda]= 1
    cmt_signal_series[cmt_index_series<para_lambda]= -1
    return cmt_signal_series

def Signal_Generation_Main(index_name,cmt_index_series,paras):
    if (index_name == "ITS") or (index_name == "UTS"):
        index_series = SpyderNet_1_Signal_Generation(index_name,cmt_index_series,paras)
    elif (type(index_name) == tuple) and (index_name[0]== "oi_factor"):
        index_series = OI_Factor_Signal_Generation(index_name[1],cmt_index_series,paras)
    return index_series
    
