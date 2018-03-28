# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:03:05 2018

@author: LHYM
"""
import pandas as pd
from WindPy import w
w.start()
commodities={
    'DCE':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I'],
    'CZC':['CF','SR','OI','RM','TA','FG','MA','ZC'],
    'SHF':['CU','ZN','AL','NI','AU','AG','BU','RU','HC','RB','SN'],
    'CFE':['IC','IH','IF','T','TF'],
    'ALL':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I',
           'CF','SR','OI','RM','TA','FG','MA','ZC','CU','ZN','AL',
           'NI','AU','AG','SN','BU','RU','HC','RB','IC','IH','IF','T','TF']}
    
def variety_code(cmt):
    """
    将品种名称变成交易所品种编码，如A变为A.DCE。根据上面的字典添加交易所后缀
    """
    if cmt in commodities['DCE']:
        return cmt + '.DCE'
    elif cmt in commodities['CZC']:
        return cmt + '.CZC'
    elif cmt in commodities['SHF']:
        return cmt + '.SHF'
    else:
        return cmt + '.CFE'
    

def contract_code(cmt_dict,start_date,end_date):
    """
    根据品种分类，对每个品种分别下载其所有合约，包括目前存在和已经退市的，下载的内容包括
    合约代码、上市退市日期等，为了之后在某一日期筛选当日有效合约准备。下载后所有合约信息
    拼成一个大df，作为中间变量使用
    """
    #cmt_dict是板块名和板块包含品种名的字典     
    cmt_code = [variety_code(v) for v in cmt_dict["all_cmt"]]
    cmt_variety = zip(cmt_dict["all_cmt"],cmt_code)
    cmt_list = []
    for cmt in cmt_variety:
        data = w.wset("futurecc","startdate="+start_date+";enddate="+end_date+";wind_code="+cmt[1])
        df = pd.DataFrame(data.Data, index=data.Fields).T
        cmt_list.append(df)
    total_cnt = pd.concat(cmt_list)
    return total_cnt
    
    
    