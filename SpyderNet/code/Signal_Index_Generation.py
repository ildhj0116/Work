# -*- coding: utf-8 -*-
"""
Created on Thu Mar 08 14:44:30 2018

@author: 李弘一萌
"""

import pandas as pd
import numpy as np

def sign(x):
    if x>0:
        return 1
    elif x<0:
        return -1
    else:
        return 0
    
    
    
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


def OI_Factor_Generation(factor_num,cmt_oi_series,total_vol_oi_df,para_r,para_n):
    cmt_oi_series.dropna(inplace=True)
    cmt = cmt_oi_series.name
    long_oi_list = []
    short_oi_list = []
    total_list = []
    
    for i in range(len(cmt_oi_series)):
        tmp_oi_df = cmt_oi_series[i]        
        if len(tmp_oi_df)<=2:
            long_oi_list.append(np.nan)
            short_oi_list.append(np.nan)
            total_list.append(np.nan)               
        else:
            total_oi_vol = total_vol_oi_df.iloc[i,:]
            tmp_TopN = tmp_oi_df.iloc[:para_n,:]
            long_oi_list.append(tmp_TopN["long_position"].sum())
            short_oi_list.append(tmp_TopN["short_position"].sum())
            total_list.append(total_oi_vol["OI"])
    oi = pd.DataFrame([long_oi_list,short_oi_list,total_list],index=["long_position","short_position","total_position"],\
                              columns=cmt_oi_series.index).T
        
    if factor_num == 1:
        cmt_index_series = (oi["long_position"] - oi["short_position"]) / (oi["long_position"] - oi["short_position"]).shift(para_r) - 1 
    elif factor_num == 2:
        cmt_index_series = (oi["long_position"] - oi["short_position"]) / oi["total_position"] - \
                           ((oi["long_position"] - oi["short_position"]) / oi["total_position"]).shift(para_r)  
    elif factor_num == 3:
        cmt_index_series = (oi["long_position"] - oi["short_position"]) / (oi["long_position"] + oi["short_position"])
    elif factor_num == 4:
        cmt_index_series = oi["long_position"]/ oi["long_position"].shift(para_r) - 1
    elif factor_num == 5:
        cmt_index_series = - (oi["short_position"] / oi["short_position"].shift(para_r) - 1)
    elif factor_num == 6:
        cmt_index_series = (oi["long_position"] / oi["total_position"]) - (oi["long_position"] / oi["total_position"]).shift(para_r) 
    elif factor_num == 7:
        cmt_index_series = - ((oi["short_position"] / oi["total_position"]) - (oi["short_position"] - oi["total_position"]).shift(para_r))
    elif factor_num == 8:
        cmt_index_series = ((oi["long_position"] / oi["long_position"].shift(para_r) - 1).apply(sign) + (oi["short_position"].shift(para_r) / oi["short_position"] - 1).apply(sign)).apply(sign)
    elif factor_num == 9:
        cmt_index_series = (oi["long_position"] / oi["long_position"].shift(para_r) - 1).apply(sign)
    elif factor_num == 10:
        cmt_index_series = (oi["short_position"].shift(para_r) / oi["short_position"] - 1).apply(sign)        
    cmt_index_series.name = cmt                                     
    return cmt_index_series



def Signal_Index_Generation_Main(index_name,cmt_oi_series,total_vol_oi_df,para_r,para_n):
    if (index_name == "ITS") or (index_name == "UTS"):
        index_series = SpyderNet_1_ITS_UTS_Generation(index_name,cmt_oi_series,total_vol_oi_df)
    elif (type(index_name) == tuple) and (index_name[0]== "oi_factor"):
        index_series = OI_Factor_Generation(index_name[1],cmt_oi_series,total_vol_oi_df,para_r,para_n)
    return index_series


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




