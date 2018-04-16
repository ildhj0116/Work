# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 14:01:52 2018
计算期货市场的沉淀资金并分版块画图
@author: LHYM
"""
import pandas as pd
from contract_code import contract_code
from CV_Compute import CV_Compute,CV_Compute_local
from plotCV import plotCV_sector,plotCV_sector_one_graph,plotCV_all,plot_chg_sector
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
commodities={
    'DCE':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I'],
    'CZC':['CF','SR','OI','RM','TA','FG','MA','ZC','AP'],
    'SHF':['CU','ZN','AL','NI','AU','AG','BU','RU','HC','RB','SN'],
    'CFE':['IC','IH','IF','T','TF'],
    'INE':['SC'],
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
    elif cmt in commodities['CFE']:
        return cmt + '.CFE'
    else:
        return cmt + '.INE'
    
filename_sector = "ContractValue.csv"

def fund_main(start_date,end_date,cmt_list):
    #制作合约列表
    total_cnt = contract_code(cmt_dict,start_date,end_date) 
   
    #根据下载的合约列表在所给时间段中每日下载持仓量、收盘价和乘数并计算合约价值，并存入csv文件中
    Contract_Value_sector, Contract_Value_allcmt = CV_Compute(total_cnt,start_date,end_date,cmt_dict)
    cmt_list.index = [x[:-4] for x in cmt_list.index.tolist()]
    Contract_Value_allcmt.columns = cmt_list.loc[Contract_Value_allcmt.columns.tolist(),:]["Chinese"].tolist()    
    #画总合约价值和版块合约价值图（2*3 subplots）并存储
    fig_sector = plotCV_sector(Contract_Value_sector)
    
    #画所有品种资金沉淀
    fig_allcmt = plotCV_all(Contract_Value_allcmt)
    return [fig_sector,fig_allcmt]


def fund_main_local(start_date,end_date,cmt_list,relative_data_path):   
    #根据下载的合约列表在所给时间段中每日下载持仓量、收盘价和乘数并计算合约价值，并存入csv文件中
    all_cmt_list = [variety_code(x) for x in all_cmt]
    Contract_Value_sector, Contract_Value_allcmt = CV_Compute_local(start_date,end_date,cmt_dict,all_cmt_list,
                                                                    relative_data_path)
    cmt_list.index = [x[:-4] for x in cmt_list.index.tolist()]
    Contract_Value_allcmt.columns = cmt_list.loc[Contract_Value_allcmt.columns.tolist(),:]["Chinese"].tolist()    
    #画总合约价值和版块合约价值图（2*3 subplots）并存储
    fig_sector = plotCV_sector(Contract_Value_sector)
    
    #画所有品种资金沉淀
    fig_allcmt = plotCV_all(Contract_Value_allcmt)
    return [fig_sector,fig_allcmt]

def fund_main_weekly(start_date,end_date,cmt_list,date_interval):
    #制作合约列表
    total_cnt = contract_code(cmt_dict,start_date,end_date) 
   
    #根据下载的合约列表在所给时间段中每日下载持仓量、收盘价和乘数并计算合约价值，并存入csv文件中
    Contract_Value_sector, Contract_Value_allcmt = CV_Compute(total_cnt,start_date,end_date,cmt_dict)
    cmt_list.index = [x[:-4] for x in cmt_list.index.tolist()]
    Contract_Value_allcmt.columns = cmt_list.loc[Contract_Value_allcmt.columns.tolist(),:]["Chinese"].tolist()    
    Contract_Value_sector = Contract_Value_sector.iloc[-date_interval:,:].copy()
    Contract_Value_allcmt = Contract_Value_allcmt.iloc[-date_interval:,:].copy()
    #画总合约价值和版块合约价值图（2*3 subplots）并存储
    #fig_sector_one_graph = plotCV_sector_one_graph(Contract_Value_sector)
    fig_sector = plotCV_sector(Contract_Value_sector)
    return [fig_sector]


def fund_main_date(start_date,end_date,cmt_list):
    #制作合约列表
    total_cnt = contract_code(cmt_dict,start_date,end_date) 
   
    #根据下载的合约列表在所给时间段中每日下载持仓量、收盘价和乘数并计算合约价值，并存入csv文件中
    Contract_Value_sector, Contract_Value_allcmt = CV_Compute(total_cnt,start_date,end_date,cmt_dict)
    cmt_list.index = [x[:-4] for x in cmt_list.index.tolist()]
    Contract_Value_allcmt.columns = cmt_list.loc[Contract_Value_allcmt.columns.tolist(),:]["Chinese"].tolist()    

    #画总合约价值和版块合约价值图（2*3 subplots）并存储
    fig_sector = plotCV_sector(Contract_Value_sector)
    return [fig_sector]


def fund_main_CV_output(start_date,end_date):
    #制作合约列表
    total_cnt = contract_code(cmt_dict,start_date,end_date) 
   
    #根据下载的合约列表在所给时间段中每日下载持仓量、收盘价和乘数并计算合约价值，并存入csv文件中
    Contract_Value_sector, Contract_Value_allcmt = CV_Compute(total_cnt,start_date,end_date,cmt_dict)  
    #画总合约价值和版块合约价值图（2*3 subplots）并存储
    fig_sector = plotCV_sector(Contract_Value_sector)
    
    return fig_sector,Contract_Value_sector


if __name__ == "__main__":
    
    
    ###############################################################################    
    start_date = '2017-01-01'
    end_date = '2018-04-12'
    
    # 下载所有品种所有合约列表
    fig_sector,cv = fund_main_CV_output(start_date,end_date)
    fig_sector.savefig("cv.jpg",bbox_inches='tight')
    #cv = pd.read_csv("cv.csv")
    jan = cv.iloc[:18,:].mean()
    jan.name = "Jan"
    feb = cv.iloc[18:36,:].mean()
    feb.name = "Feb"
    mar = cv.iloc[36:58,:].mean()
    mar.name = "Mar"
    fund2017 = pd.concat([jan,feb,mar],axis=1)
    jan1 = cv.iloc[244:266,:].mean()
    jan1.name = "Jan1"
    feb1 = cv.iloc[266:281,:].mean()
    feb1.name = "Feb1"
    mar1 = cv.iloc[281:303,:].mean()
    mar1.name = "Mar1"
    fund2017 = pd.concat([fund2017,jan1,feb1,mar1],axis=1)
    fund = fund2017.copy()
    fund["1"] = fund["Jan1"] / fund["Jan"] -1
    fund["2"] = fund["Feb1"] / fund["Feb"] -1
    fund["3"] = fund["Mar1"] / fund["Mar"] -1
    chg = fund[["1","2","3"]]
    chg.columns = [u"一月",u"二月",u"三月"]
    fig1 = plot_chg_sector(chg)
    fig1.savefig("cv_chg.jpg",bbox_inches='tight')
