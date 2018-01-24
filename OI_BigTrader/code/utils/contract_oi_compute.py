# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:33:31 2017
生成全部公司指定日期的全部在交易合约的持仓情况
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

def generate_contract_table(start_date, end_date):
    w.start()
    variety_code_list = [x + '.' + exchange(x) for x in all_commodities if x not in ['IC','IH','IF','T','TF'] ]
    # 产生合约列表(只看商品)
    cnt_list =[]
    for v in variety_code_list:
        cnt_download = w.wset("futurecc","wind_code="+v)
        condition = np.all([np.array(cnt_download.Data[7])>datetime.today(),np.array(cnt_download.Data[6])
                        <datetime.today()],axis=0)
        effective_cnt_list = np.array(cnt_download.Data[2])[condition]
        cnt_list.extend(effective_cnt_list)
    
    # 下载数据
    oi_df_list = []
    start_date = '2017-12-13'
    end_date = '2017-12-13'
    # 删除列的列表
    drop_list = ['settle', 'ranks', 'date', 'long_position', 'short_position', 'long_position_increase',
                 'short_position_increase', 'long_potion_rate', 'short_position_rate']
    for contract in cnt_list:
        params = "startdate=" + start_date + ";enddate=" + end_date + ";wind_code=" + contract + ";order_by=long;ranks=all"
        data = w.wset("futureoir",params)
        if len(data.Data)==0:
            continue
        else:
            df = pd.DataFrame(data.Data, index=data.Fields).T
            df = df.drop(drop_list, axis=1)
            df.drop(range(3),inplace=True)
            df.index=df['member_name']
            del df['member_name']
            # 新产生一列net_position，若net_long有值则用net_long, 否则用net_short的相反数
            df['net_position'] = df['net_long_position']
            df.loc[pd.isnull(df['net_position']),'net_position'] = \
                            -df['net_short_position'].loc[pd.isnull(df['net_position'])].fillna(0)
            df['net_position_increase'] = df['net_long_position_increase']
            df.loc[pd.isnull(df['net_position_increase']),'net_position_increase'] = \
                    -df['net_short_position_increase'].loc[pd.isnull(df['net_position_increase'])].fillna(0)
            df = df.stack(dropna=False)
            df.name = contract
            oi_df_list.append(df) #将每个合约的dataframe暂时存在一个列表中
    
    # 将所有合约的dataframe合并成一个大dataframe
    whole_table = oi_df_list[0]  
    for i in range(1,len(oi_df_list)):
        whole_table = pd.concat([whole_table, oi_df_list[i]], axis=1)
    contract_oi_file = 'Company_Contract_OpenInterest.csv'
    whole_table.to_csv('../output/'+contract_oi_file, encoding = 'gbk')    
    return contract_oi_file




