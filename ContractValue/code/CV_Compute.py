# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:12:29 2018

@author: LHYM
"""

import pandas as pd
from Cnt2Cmt import Cnt2Cmt
from WindPy import w 
w.start()

def CV_Compute(total_cnt,start_date,end_date,cmt_dict,filename):
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
    Contract_Value = pd.concat([Contract_Value_total,Contract_Value_agri,Contract_Value_chem,\
                                Contract_Value_fmt,Contract_Value_nfmt,Contract_Value_gld],axis=1)
    filename = '../output/'+filename
    Contract_Value.to_csv(filename, encoding = 'gb2312')