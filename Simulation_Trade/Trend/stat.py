# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 14:14:56 2018

@author: Administrator
"""
import pandas as pd
import numpy as np
agri_cmt=['A','C','CS','M','Y','P','JD','CF','SR','OI','RM']
chem_cmt=['L','PP','V','TA','MA','BU','RU']
fmt_cmt=['RB','I','HC','J','JM','ZC','FG']
nfmt_cmt=['CU','NI','AL','ZN','SN','SF']
gld_cmt=['AU','AG']
index_cmt=['IC','IH','IF','T','TF']

def Cnt2Cmt(contract):
    return ''.join([letter for letter in contract[:2] if letter.isalpha()])
def cmtclass(cmt):
    if cmt in agri_cmt:
        return u"农产品"
    elif cmt in chem_cmt:
        return u"化工"
    elif cmt in fmt_cmt:
        return u"黑色"
    elif cmt in nfmt_cmt:
        return u"有色"    
    elif cmt in gld_cmt:
        return u"贵金属"    
    elif cmt in index_cmt:
        return u"金融"    
    
def find(close,cnt,new_list,position):
    index = close[u"平仓合约"].tolist().index(cnt)
    new_list.append(close.iloc[index,:])
    new_position = close.iloc[index,:][u"平仓手数"]
    close.drop([index],inplace=True)
    close.index = range(len(close_df_left))    
    if position == new_position:
        return close,new_list
    else:
        return find(close,cnt,new_list,position - new_position)

    
    
code_df = pd.read_excel('total_deal.xlsx',encoding = 'gb2312')
code_df = code_df.iloc[range(1,3578,2),:].copy()
deal = code_df[code_df[u"交易所"] != u"小计"]
deal = deal.drop([u"平仓盈亏",u"成交额"],axis=1)
deal.columns = ["exchange","contract","date","direction","position_dir","position","price","cost"]
tmp_list = []
tmp_df = pd.DataFrame(columns=deal.columns)
open_list = []
close_list = []

position_df = pd.DataFrame()
tmp_deal_list = []

for i in range(len(deal)):
    tmp_series = deal.iloc[i,:]
    if len(tmp_list) == 0:
        tmp_list.append(tmp_series)
    else:
        tmp_last = tmp_list[-1]
        if tmp_last.iloc[:5].equals(tmp_series.iloc[:5]):
            tmp_list.append(tmp_series)
        else:
            tmp_stat = tmp_last.copy()
            tmp_df = pd.concat(tmp_list,axis=1).T
            tmp_df["weight"] = tmp_df["position"] / tmp_df["position"].sum()
            tmp_stat["position"] = tmp_df["position"].sum()
            tmp_stat["cost"] = tmp_df["cost"].sum()
            tmp_stat["price"] = (tmp_df["weight"] * tmp_df["price"]).sum()
                                    
            if tmp_stat["position_dir"] == u"开":
                if len(position_df) == 0:
                    position_df = pd.concat([position_df,tmp_stat]).T
                else:
                    if tmp_stat["contract"] in position_df["contract"].tolist():
                        original = position_df[position_df["contract"]==tmp_stat["contract"]]
                        original.loc["date"] = tmp_stat["date"]
                        original.loc["price"] = ((tmp_stat["price"] * tmp_stat[u"position"] + original["price"] * original["position"])
                                                   / (tmp_stat["position"] + original["position"]))
                        original["position"] = tmp_stat["position"] + original["position"]
                        original["position"] = tmp_stat["position"] + original["position"]
                    else:
                        position_df = pd.concat([position_df.T,tmp_stat],axis=1).T
            else:
                deal_position = tmp_stat["position"]
                index = position_df[position_df["contract"]==tmp_stat["contract"]].index[0]
                open_series = position_df.loc[index,:].copy()
                open_series["position"] = deal_position
                open_series.index = ["open_" + x for x in open_series.index.tolist()]
                tmp_stat.index = ["close_" + x for x in tmp_stat.index.tolist()]
                tmp_deal_series = pd.concat([open_series,tmp_stat],ignore_index=True)
                index_list = open_series.index.tolist()
                index_list.extend(tmp_stat.index.tolist())
                tmp_deal_series.index = index_list
                tmp_deal_list.append(tmp_deal_series)
                if deal_position == position_df.loc[index,"position"]:
                    position_df = position_df[position_df["contract"]!=tmp_stat["close_contract"]]
                else:
                    position_df.loc[index,"position"] -= deal_position                                            
                        
            tmp_list = [tmp_series]
            


            
if len(tmp_list)!= 0:
    tmp_last = tmp_list[-1]
    tmp_stat = tmp_last.copy()
    tmp_df = pd.concat(tmp_list,axis=1).T
    tmp_df["weight"] = tmp_df["position"] / tmp_df["position"].sum()
    tmp_stat["position"] = tmp_df["position"].sum()
    tmp_stat["cost"] = tmp_df["cost"].sum()
    tmp_stat["price"] = (tmp_df["weight"] * tmp_df["price"]).sum()
    if tmp_stat["position_dir"] == u"开":
        if len(position_df) == 0:
            position_df = pd.concat([position_df,tmp_stat]).T
        else:
            if tmp_stat["contract"] in position_df["contract"].tolist():
                original = position_df[position_df["contract"]==tmp_stat["contract"]]
                original.loc["date"] = tmp_stat["date"]
                original.loc["price"] = ((tmp_stat["price"] * tmp_stat["position"] + original["price"] * original["position"])
                                           / (tmp_stat["position"] + original["position"]))
                original["position"] = tmp_stat["position"] + original["position"]
                original["position"] = tmp_stat["position"] + original["position"]
            else:
                position_df = pd.concat([position_df,tmp_stat])
    else:
        deal_position = tmp_stat["position"]
        index = position_df[position_df["contract"]==tmp_stat["contract"]].index[0]
        open_series = position_df.loc[index,:].copy()
        open_series["position"] = deal_position
        open_series.index = ["open_" + x for x in open_series.index.tolist()]
        tmp_stat.index = ["close_" + x for x in tmp_stat.index.tolist()]
        tmp_deal_series = pd.concat([open_series,tmp_stat],ignore_index=True)
        index_list = open_series.index.tolist()
        index_list.extend(tmp_stat.index.tolist())
        tmp_deal_series.index = index_list
        tmp_deal_list.append(tmp_deal_series)
        if deal_position == position_df.loc[index,"position"]:
            position_df = position_df[position_df["contract"]!=tmp_stat["close_contract"]]
        else:
            position_df.loc[index,"position"] -= deal_position  

arranged_deal_df = pd.concat(tmp_deal_list,axis=1).T
arranged_deal_df["cost"] =  arranged_deal_df["open_cost"] + arranged_deal_df["close_cost"]

      
#open_df = pd.concat(open_list,axis=1).T
#close_df = pd.concat(close_list,axis=1).T
#   
#open_df.columns = [u"开仓" + x for x in open_df.columns.tolist()]
#close_df.columns = [u"平仓" + x for x in close_df.columns.tolist()]
#open_df.index = range(len(open_df))
#close_df.index = range(len(close_df))
#
#position_df = pd.DataFrame()
#finished_deal_open_list = []
#
#for i in range(len(close_df)):
#    
#
#
#
#
##    else:
##        close_new_list.append(np.nan)
#close_new_df =pd.concat(tmp_close_series_list,axis=1).T
    
    
    
    
    
    
    
    
#code_df.to_excel("result.xlsx")


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


