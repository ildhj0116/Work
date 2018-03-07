# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 09:50:06 2017

@author: 李弘一萌
"""
import sys

commodities={
'DCE':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I'],
'CZC':['CF','SR','RM','TA','FG','MA','ZC'],
'SHF':['CU','ZN','AL','NI','AU','AG','BU','RU','HC','RB'],
'CFE':['IC','IH','IF','T','TF'],
'ALL':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I',
       'CF','SR','RM','TA','FG','MA','ZC','CU','ZN','AL',
       'NI','AU','AG','BU','RU','HC','RB','IC','IH','IF','T','TF']}


def exchange(cmt):
        if cmt in commodities['DCE']:
            return cmt+'.DCE'
        elif cmt in commodities['CZC']:
            return cmt+'.CZC'
        elif cmt in commodities['SHF']:
            return cmt+'.SHF'
        else:
            return cmt+'.CFE'

Main_cnt_Version = {
        1:"连续n天次主力持仓量大于主力，在下一天进行直接换月"
        }


if __name__ == "__main__":
###############################################################################
#设置参数    
    para_base_date = "2009-12-31"
    para_end_date = "2018-03-06"
    para_version = str(1)
    
    para_single = False
    para_single_cmt = ["MA.CZC"]
    para_file_name = "MA"
    
###############################################################################    
    
    if para_single == False:
        cnt_list = commodities['ALL']    
        cmt_list = [exchange(x) for x in cnt_list]
        file_name = "total"
    else:
        file_name = para_file_name
        cmt_list = para_single_cmt
        
    my_path = "./main_cnt_V" + para_version
    sys.path.append(my_path)
    from Main_Contract import Main_Contract
    
    main_cnt_df = Main_Contract(cmt_list,para_base_date,para_end_date)
    main_cnt_df.to_csv("../data/main_cnt_"+file_name+".csv")

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    