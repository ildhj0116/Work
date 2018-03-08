# -*- coding: utf-8 -*-
"""
Created on Thu Mar 08 14:44:30 2018

@author: Administrator
"""

import pandas as pd
import numpy as np

def SpyderNet_1_ITS_UTS_Generation(index_name,cmt_oi_series,total_vol_oi_df):
    cmt_oi_series.dropna(inplace=True)
    cmt = cmt_oi_series.name
    cmt_index_list = []
    cmt_B_list = []
    cmt_S_list = []
    
    for i in range(len(cmt_oi_series)):
        tmp_oi_df = cmt_oi_series[i]
        
        if len(tmp_oi_df)<=2:
            index=0
            B = np.nan
            S = np.nan                
        else:
            oi_sum = tmp_oi_df.drop("date",axis=1).sum()
            total_oi_vol = total_vol_oi_df.iloc[i,:]
            tmp_oi_df.loc["others","vol"] = total_oi_vol.loc["VOLUME"] - oi_sum["vol"]
            tmp_oi_df.loc["others","long_position"] = total_oi_vol.loc["OI"] - oi_sum["long_position"]
            tmp_oi_df.loc["others","short_position"] = total_oi_vol.loc["OI"] - oi_sum["short_position"]
            tmp_oi_df["Stat"] = (tmp_oi_df["long_position"]+tmp_oi_df["short_position"])/tmp_oi_df["vol"]                        
            total_stat = total_oi_vol.loc["OI"] * 2 / total_oi_vol.loc["VOLUME"]
            informed_trader = tmp_oi_df[tmp_oi_df["Stat"]>=total_stat]
            uninformed_trader = tmp_oi_df[tmp_oi_df["Stat"]<total_stat]
            if index_name == "ITS":
                B = informed_trader["long_position"].sum()
                S = informed_trader["short_position"].sum()
            elif index_name == "UTS":                    
                B = uninformed_trader["long_position"].sum()
                S = uninformed_trader["short_position"].sum()
            if B+S==0:
                index = 0
            else:
                index = (B-S)/(B+S)
        cmt_B_list.append(B)
        cmt_S_list.append(S)
        cmt_index_list.append(index)
        
    cmt_index_series = pd.Series(cmt_index_list,index=cmt_oi_series.index,name=cmt)
    return cmt_index_series


def OI_Factor_Generation(factor_num,cmt_oi_series):
    pass



def Signal_Index_Generation_Main(index_name,cmt_oi_series,total_vol_oi_df):
    if (index_name == "ITS") or (index_name == "UTS"):
        index_series = SpyderNet_1_ITS_UTS_Generation(index_name,cmt_oi_series,total_vol_oi_df)
    elif (type(index_name) == tuple) and (index_name[0]== "oi_factor"):
        index_series = OI_Factor_Generation(index_name[1],cmt_oi_series)
    return index_series


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




