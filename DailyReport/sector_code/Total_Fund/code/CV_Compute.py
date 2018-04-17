# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:12:29 2018

@author: LHYM
"""

import pandas as pd
from Cnt2Cmt import Cnt2Cmt
from WindPy import w 
from datetime import datetime
w.start()

def CV_Compute(total_cnt,start_date,end_date,cmt_dict):
    """
    根据前面得到的所有品种历史合约表，在指定时间段内遍历每个交易日，筛选当日有效的合约，
    下载持仓量、收盘价和乘数数据并计算各品种的合约价值。然后再按板块分别归纳统计板块和总
    合约价值，最终将这一时间段所有交易日内的CV计算完成
    """
    # 从wind下载交易日列表
    trade_days = w.tdays(start_date, end_date).Data[0]
    # 初始化品种cv列表，为轴向链接做准备
    cnt_value_list = []    
    for t_date in trade_days:
        #万得下载的列表为datetime对象，这里生成字符串
        target_date = t_date.strftime("%Y-%m-%d")
        #初始化
        cnt_value_pd = pd.DataFrame(columns=cmt_dict["all_cmt"])    
        effective_cmt_df = total_cnt[(total_cnt['contract_issue_date']<t_date) & (total_cnt['last_trade_date']>t_date)]
        cnt_list = ','.join(list(effective_cmt_df['wind_code']))
        data = w.wss(cnt_list, "contractmultiplier,margin,close,oi","tradeDate="+target_date)
        tmp_df = pd.DataFrame(data.Data,index=data.Fields).T.fillna(0)
        tmp_df['cmt'] = [Cnt2Cmt(cnt) for cnt in data.Codes]
        tmp_df[target_date] = tmp_df['CONTRACTMULTIPLIER'] * tmp_df['MARGIN'] / 100 * tmp_df['CLOSE'] * tmp_df['OI'] / 100000000
        cnt_value_pd = tmp_df[target_date].groupby(tmp_df['cmt']).sum()
        cnt_value_list.append(cnt_value_pd)
    
        
    Contract_Value_allcmt = pd.concat(cnt_value_list,axis=1).T
    Contract_Value_total = Contract_Value_allcmt.sum(axis=1)
    Contract_Value_chem = Contract_Value_allcmt[cmt_dict["chem_cmt"]].sum(axis=1)
    Contract_Value_agri = Contract_Value_allcmt[cmt_dict["agri_cmt"]].sum(axis=1)
    Contract_Value_fmt = Contract_Value_allcmt[cmt_dict["fmt_cmt"]].sum(axis=1)
    Contract_Value_nfmt = Contract_Value_allcmt[cmt_dict["nfmt_cmt"]].sum(axis=1)
    Contract_Value_gld = Contract_Value_allcmt[cmt_dict["gld_cmt"]].sum(axis=1)
    Contract_Value_total.rename("total_CV",inplace=True)
    Contract_Value_agri.rename("agri_CV",inplace=True)
    Contract_Value_chem.rename("chem_CV",inplace=True)
    Contract_Value_fmt.rename("fmt_CV",inplace=True)
    Contract_Value_nfmt.rename("nfmt_CV",inplace=True)
    Contract_Value_gld.rename("gld_CV",inplace=True)
    Contract_Value_sector = pd.concat([Contract_Value_total,Contract_Value_agri,Contract_Value_chem,\
                                Contract_Value_fmt,Contract_Value_nfmt,Contract_Value_gld],axis=1)
    
    return Contract_Value_sector, Contract_Value_allcmt

def CV_Compute_local(start_date,end_date,cmt_dict,cmt_list,relative_data_path):
    fund_list = []
    multi_df = pd.read_csv(relative_data_path+"/cmt_list/cmt_profile.csv",index_col=0)
    for cmt in cmt_list:
        tmp_cl = pd.read_csv(relative_data_path+"/data_cl/"+cmt[:-4]+".csv",index_col=0,parse_dates=[0])
        tmp_oi = pd.read_csv(relative_data_path+"/data_oi/"+cmt[:-4]+".csv",index_col=0,parse_dates=[0])
        begin = datetime.strptime(start_date,"%Y-%m-%d")
        end = datetime.strptime(end_date,"%Y-%m-%d")
        effective_cl = tmp_cl[(tmp_cl.index >= begin) & ((tmp_cl.index <= end))].copy().fillna(0)
        effective_oi = tmp_oi[(tmp_oi.index >= begin) & ((tmp_oi.index <= end))].copy().fillna(0)
        fund = pd.Series(index=effective_cl.index,name=cmt)
        for i in range(len(fund)):
            fund.iloc[i] = (effective_cl.iloc[i,:] * effective_oi.iloc[i,:] ).sum()
            fund.iloc[i] = fund.iloc[i] * multi_df.loc[cmt,"margin"] /100 * multi_df.loc[cmt,"multiplier"]/ 100000000
        fund_list.append(fund)    
    Contract_Value_allcmt = pd.concat(fund_list,axis=1)
    Contract_Value_allcmt.columns = [x[:-4] for x in Contract_Value_allcmt.columns.tolist()]
    Contract_Value_total = Contract_Value_allcmt.sum(axis=1)
    Contract_Value_chem = Contract_Value_allcmt[cmt_dict["chem_cmt"]].sum(axis=1)
    Contract_Value_agri = Contract_Value_allcmt[cmt_dict["agri_cmt"]].sum(axis=1)
    Contract_Value_fmt = Contract_Value_allcmt[cmt_dict["fmt_cmt"]].sum(axis=1)
    Contract_Value_nfmt = Contract_Value_allcmt[cmt_dict["nfmt_cmt"]].sum(axis=1)
    Contract_Value_gld = Contract_Value_allcmt[cmt_dict["gld_cmt"]].sum(axis=1)
    Contract_Value_total.rename("total_CV",inplace=True)
    Contract_Value_agri.rename("agri_CV",inplace=True)
    Contract_Value_chem.rename("chem_CV",inplace=True)
    Contract_Value_fmt.rename("fmt_CV",inplace=True)
    Contract_Value_nfmt.rename("nfmt_CV",inplace=True)
    Contract_Value_gld.rename("gld_CV",inplace=True)
    Contract_Value_sector = pd.concat([Contract_Value_total,Contract_Value_agri,Contract_Value_chem,\
                                Contract_Value_fmt,Contract_Value_nfmt,Contract_Value_gld],axis=1)
    
    return Contract_Value_sector, Contract_Value_allcmt
        
        
        
    # 从wind下载交易日列表
    trade_days = w.tdays(start_date, end_date).Data[0]
    # 初始化品种cv列表，为轴向链接做准备
    cnt_value_list = []    
    for t_date in trade_days:
        #万得下载的列表为datetime对象，这里生成字符串
        target_date = t_date.strftime("%Y-%m-%d")
        #初始化
        cnt_value_pd = pd.DataFrame(columns=cmt_dict["all_cmt"])    
        effective_cmt_df = total_cnt[(total_cnt['contract_issue_date']<t_date) & (total_cnt['last_trade_date']>t_date)]
        cnt_list = ','.join(list(effective_cmt_df['wind_code']))
        data = w.wss(cnt_list, "contractmultiplier,close,oi","tradeDate="+target_date)
        tmp_df = pd.DataFrame(data.Data,index=data.Fields).T.fillna(0)
        tmp_df['cmt'] = [Cnt2Cmt(cnt) for cnt in data.Codes]
        tmp_df[target_date] = tmp_df['CONTRACTMULTIPLIER'] * tmp_df['CLOSE'] * tmp_df['OI'] /100000000
        cnt_value_pd = tmp_df[target_date].groupby(tmp_df['cmt']).sum()
        cnt_value_list.append(cnt_value_pd)
    
        
    Contract_Value_allcmt = pd.concat(cnt_value_list,axis=1).T
    Contract_Value_total = Contract_Value_allcmt.sum(axis=1)
    Contract_Value_chem = Contract_Value_allcmt[cmt_dict["chem_cmt"]].sum(axis=1)
    Contract_Value_agri = Contract_Value_allcmt[cmt_dict["agri_cmt"]].sum(axis=1)
    Contract_Value_fmt = Contract_Value_allcmt[cmt_dict["fmt_cmt"]].sum(axis=1)
    Contract_Value_nfmt = Contract_Value_allcmt[cmt_dict["nfmt_cmt"]].sum(axis=1)
    Contract_Value_gld = Contract_Value_allcmt[cmt_dict["gld_cmt"]].sum(axis=1)
    Contract_Value_total.rename("total_CV",inplace=True)
    Contract_Value_agri.rename("agri_CV",inplace=True)
    Contract_Value_chem.rename("chem_CV",inplace=True)
    Contract_Value_fmt.rename("fmt_CV",inplace=True)
    Contract_Value_nfmt.rename("nfmt_CV",inplace=True)
    Contract_Value_gld.rename("gld_CV",inplace=True)
    Contract_Value_sector = pd.concat([Contract_Value_total,Contract_Value_agri,Contract_Value_chem,\
                                Contract_Value_fmt,Contract_Value_nfmt,Contract_Value_gld],axis=1)
    
    return Contract_Value_sector, Contract_Value_allcmt