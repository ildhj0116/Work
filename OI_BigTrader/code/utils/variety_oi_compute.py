# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:33:31 2017
# 生成全部公司公司指定日期的品种总持仓情况
@author: LHYM
"""
from WindPy import w
import pandas as pd
import numpy as np
from datetime import *
from contracts import main_contracts, exchange


commodities={
'DCE':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I'],
'CZC':['CF','SR','OI','RM','TA','FG','MA','ZC'],
'SHF':['CU','ZN','AL','NI','AU','AG','BU','RU','HC','RB'],
'CFE':['IC','IH','IF','T','TF']}

all_commodities = ['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I',
       'CF','SR','OI','RM','TA','FG','MA','ZC','CU','ZN','AL',
       'NI','AU','AG','BU','RU','HC','RB','IC','IH','IF','T','TF']
exchanges = ['DCE','CZC','SHF','CFE']
variety_code_list = [x + '.' + exchange(x) for x in all_commodities]

def generate_variety_table(start_date, end_date):
    w.start()
    oi_df_list = []
    start_date = '2017-12-13'
    end_date = '2017-12-13'
    # 通过品种列表，分别下载每个品种的持仓情况
    drop_list = ['settle', 'ranks', 'date', 'long_position', 'short_position', 'long_position_increase',
                 'short_position_increase', 'long_potion_rate', 'short_position_rate']
    for variety in variety_code_list:
        params = "startdate=" + start_date + ";enddate=" + end_date + ";varity=" + variety + ";order_by=long;ranks=all"
        data = w.wset("futureoir",params)
        if len(data.Data) == 0 or (variety in ['IC','IH','IF','T','TF']):   #只看商品
            continue
        else:
            df = pd.DataFrame(data.Data, index=data.Fields).T
            df = df.drop(drop_list, axis=1)
            df.drop(range(3),inplace=True)
            df.index=df['member_name']
            del df['member_name']
            df['net_position'] = df['net_long_position']
            df.loc[pd.isnull(df['net_position']),'net_position'] = \
                            -df['net_short_position'].loc[pd.isnull(df['net_position'])].fillna(0)
            df['net_position_increase'] = df['net_long_position_increase']
            df.loc[pd.isnull(df['net_position_increase']),'net_position_increase'] = \
                    -df['net_short_position_increase'].loc[pd.isnull(df['net_position_increase'])].fillna(0)
            
            df = df.stack(dropna=False)
            df.name = variety
            oi_df_list.append(df)
            
    # 将每个品种持仓情况的dataframe进行合并
    whole_table = oi_df_list[0]  
    for i in range(1,len(oi_df_list)):
        whole_table = pd.concat([whole_table, oi_df_list[i]], axis=1)
    
        
    # 输出到csv文件中
    variety_oi_file = 'Company_Contract_OpenInterest.csv'
    whole_table.to_csv('../output/'+variety_oi_file, encoding = 'gbk')  
    # 返回文件名
    return variety_oi_file



