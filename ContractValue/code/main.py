# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 14:01:52 2018
计算期货市场的沉淀资金并分版块画图
@author: LHYM
"""
from contract_code import contract_code
from CV_Compute import CV_Compute
from plotCV import plotCV
from WindPy import w 
w.start()

agri_cmt = ['A','C','CS','M','Y','P','JD','CF','SR','OI','RM']
chem_cmt = ['L','PP','V','TA','MA','BU','RU']
fmt_cmt = ['RB','I','HC','J','JM','ZC','FG']
nfmt_cmt = ['CU','NI','AL','ZN','SN']
gld_cmt = ['AU','AG']
all_cmt = agri_cmt + chem_cmt + fmt_cmt + nfmt_cmt + gld_cmt
cmt_dict = {"agri_cmt":agri_cmt, "chem_cmt":chem_cmt, "fmt_cmt":fmt_cmt, "nfmt_cmt":nfmt_cmt,
            "gld_cmt":gld_cmt, "all_cmt":all_cmt}


filename = "ContractValue.csv"
###############################################################################    
start_date = '2017-09-01'
end_date = '2018-03-01'

# 下载所有品种所有合约列表
total_cnt = contract_code(cmt_dict,start_date,end_date) 
print "合约制作完毕"

#根据下载的合约列表在所给时间段中每日下载持仓量、收盘价和乘数并计算合约价值，并存入csv文件中

CV_Compute(total_cnt,start_date,end_date,cmt_dict,filename)


#画总合约价值和版块合约价值图（2*3 subplots）并存储
plotCV(filename)







