# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 09:50:06 2017

@author: LHYM
"""

from Main_Contract import Main_Contract


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



if __name__ == "__main__":
    cnt_list = commodities['ALL']
    base_date = "2009-12-31"
    end_date = "2018-01-17"    
    cmt_list = [exchange(x) for x in cnt_list]
    main_cnt_df = Main_Contract(["A.DCE"],base_date,end_date)
    """
    main_cnt_df = Main_Contract(cmt_list,base_date,end_date)
    main_cnt_df.to_csv("main_cnt.csv")
    """
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    