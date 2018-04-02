# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 14:01:52 2018
计算期货市场的沉淀资金并分版块画图
@author: LHYM
"""
from contract_code import contract_code
from CV_Compute import CV_Compute
from plotCV import plotCV_sector,plotCV_sector_one_graph,plotCV_all
from WindPy import w 
w.start()

agri_cmt = ['A','C','CS','M','Y','P','JD','CF','SR','RM']
chem_cmt = ['L','PP','V','TA','MA','BU','RU']
fmt_cmt = ['RB','I','HC','J','JM','ZC','FG']
nfmt_cmt = ['CU','NI','AL','ZN']
gld_cmt = ['AU','AG']
all_cmt = agri_cmt + chem_cmt + fmt_cmt + nfmt_cmt + gld_cmt
cmt_dict = {"agri_cmt":agri_cmt, "chem_cmt":chem_cmt, "fmt_cmt":fmt_cmt, "nfmt_cmt":nfmt_cmt,
            "gld_cmt":gld_cmt, "all_cmt":all_cmt}

filename_sector = "ContractValue.csv"

def fund_main(start_date,end_date,cmt_list,date_interval):
    #制作合约列表
    total_cnt = contract_code(cmt_dict,start_date,end_date) 
   
    #根据下载的合约列表在所给时间段中每日下载持仓量、收盘价和乘数并计算合约价值，并存入csv文件中
    Contract_Value_sector, Contract_Value_allcmt = CV_Compute(total_cnt,start_date,end_date,cmt_dict)
    cmt_list.index = [x[:-4] for x in cmt_list.index.tolist()]
    Contract_Value_allcmt.columns = cmt_list.loc[Contract_Value_allcmt.columns.tolist(),:]["Chinese"].tolist()    
    Contract_Value_sector = Contract_Value_sector.iloc[-date_interval:,:].copy()
    Contract_Value_allcmt = Contract_Value_allcmt.iloc[-date_interval:,:].copy()
    #画总合约价值和版块合约价值图（2*3 subplots）并存储
    fig_sector = plotCV_sector_one_graph(Contract_Value_sector)
    
    #画所有品种资金沉淀
    fig_allcmt = plotCV_all(Contract_Value_allcmt)
    return [fig_sector,fig_allcmt]




if __name__ == "__main__":
    
    
    ###############################################################################    
    start_date = '2017-09-01'
    end_date = '2018-03-27'
    
    # 下载所有品种所有合约列表
    total_cnt = contract_code(cmt_dict,start_date,end_date) 
    #print "合约制作完毕"
    
    #根据下载的合约列表在所给时间段中每日下载持仓量、收盘价和乘数并计算合约价值，并存入csv文件中
    Contract_Value_sector, Contract_Value_allcmt =CV_Compute(total_cnt,start_date,end_date,cmt_dict)
    
    
    #画总合约价值和版块合约价值图（2*3 subplots）并存储
    plotCV_sector(Contract_Value_sector)
    #画所有品种资金沉淀
    plotCV_all(Contract_Value_allcmt)






