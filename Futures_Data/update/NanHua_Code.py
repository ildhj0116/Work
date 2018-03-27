# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 08:25:41 2018

@author: Administrator
"""
import pandas as pd

code_list = ["NH00" + str(x).zfill(2) + ".NHF" for x in range(1,41)]
code_list.extend(["NHCS.NHF","NHLR.NHF","NHNI.NHF","NHSF.NHF","NHSM.NHF","NHSN.NHF","NH0100.NHF"])

cmt_list = ["A","Y","C","L","WH","CF","SR","AU","ZN","FU","TA","CU","AL","RU","M","RB","WR","RI","V","OI","P","J","PB",
            "MA","AG","FG","RS","RM","JM","ZC","BU","I","JD","JR","BB","FB","PP","HC","CY","AP","CS","LR","NI","SF","SM","SN","Commodity"]

NanHua_Index_code = pd.Series(code_list,index=cmt_list,name="code")
NanHua_Index_code.to_csv("../cmt_list/Nanhua_code_list.csv",header=True)

