# -*- coding:utf-8 -*-

import pandas as pd
from WindPy import w

def get_data(date,code_df):
    w.start()
    datestr = "tradeDate=" + date
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
            cnt_name = code_df.iloc[row_num,col_num]
            if not_NaN.iloc[row_num,col_num]:
                data =  w.wss(cnt_name,"oi_chg, margin, contractmultiplier, close, pre_close, oi", datestr)
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

def get_data_local(start_date,end_date,cmt,cl_df,oi_df):
    start_cl = cl_df.loc[start_date,:].dropna().copy()
    end_cl = cl_df.loc[end_date,:].dropna().copy()
    start_oi = oi_df.loc[start_date,:].dropna().copy()
    end_oi = oi_df.loc[end_date,:].dropna().copy()
    data_df = pd.concat([start_cl,start_oi,end_cl,end_oi],axis=1)
    data_df.columns = ["start_cl","start_oi","end_cl","end_oi"]
    basic_info = w.wss(",".join(data_df.index.tolist()), "margin, contractmultiplier")
    basic_info = pd.DataFrame(basic_info.Data,index=basic_info.Fields,columns=basic_info.Codes).T
    data_df = pd.concat([data_df,basic_info],axis=1)
    data_df.fillna(0,inplace=True)
    data_df["passive_fund"] = (data_df["end_cl"] - data_df["start_cl"]) * data_df["start_oi"] \
                                * data_df["MARGIN"] / 100 * data_df["CONTRACTMULTIPLIER"] / 100000000.0
    data_df["active_fund"] = (data_df["end_oi"] - data_df["start_oi"]) * data_df["end_cl"] \
                                * data_df["MARGIN"] / 100 * data_df["CONTRACTMULTIPLIER"] / 100000000.0
    data_df["fund"] = data_df["passive_fund"] + data_df["active_fund"]
    data_df["fund_start"] = data_df["start_cl"] * data_df["start_oi"] * data_df["MARGIN"] / 100 * data_df["CONTRACTMULTIPLIER"] / 100000000.0
    fund_pct_chg =  round(round(data_df["fund"].sum(),2) / round(data_df["fund_start"].sum(),2),2)
    return round(data_df["passive_fund"].sum(),2), round(data_df["active_fund"].sum(),2), round(data_df["fund"].sum(),2), fund_pct_chg


