# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from WindPy import *
import math
from datetime import datetime

def get_data(date):
    w.start()
    datestr = "tradeDate=" + date
    code_df = pd.read_csv('../output/TopContractList.csv', encoding = 'gb2312', index_col = 0 )
    output_df = pd.DataFrame()
    passive_flow = []
    active_flow = []
    flow = []
    contracts = []
    commodity = []
    top_num = code_df.columns.size
    contract_num = len(code_df)
    not_NaN = code_df.notnull()
    for row_num in range(contract_num):
        for col_num in range(top_num):
            
            i = row_num * top_num + col_num + 1
            cnt_name = code_df.iloc[row_num,col_num]
            if not_NaN.iloc[row_num,col_num]:
                data =  w.wss(cnt_name,"His_oichange, margin, contractmultiplier, His_close, pre_close, His_oi", datestr)
                oi_today = data.Data[5][0]
                oi_diff = data.Data[0][0]
                oi_last = oi_today - oi_diff
                margin = data.Data[1][0]
                mltplyer = data.Data[2][0]
                close_today = data.Data[3][0]
                close_last = data.Data[4][0]
                passive_fund = round( (close_today - close_last)*oi_last*margin/100*mltplyer / 100000000.0, 2)
                active_fund = round( (oi_today - oi_last)*close_today*margin/100*mltplyer / 100000000.0, 2)
                fund = round(passive_fund + active_fund, 2)
                passive_flow.append(passive_fund)
                active_flow.append(active_fund)
                flow.append(fund)
                contracts.append(cnt_name)
                commodity.append(code_df.index[row_num])
            else:
                continue
    output_df['passive_flow'] = passive_flow
    output_df['active_flow'] = active_flow
    output_df['flow'] = flow
    output_df['commodity_name'] = commodity
    output_df['contract'] = contracts
    return output_df



