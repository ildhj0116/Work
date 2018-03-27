# encoding: UTF-8
# 合约列表制作

import csv
def exchange(cmt,commodities):
    if cmt in commodities['DCE']:
        return 'DCE'
    elif cmt in commodities['CZC']:
        return 'CZC'
    elif cmt in commodities['SHF']:
        return 'SHF'
    elif cmt in commodities['CFE']:
        return 'CFE'
    else:
        return 'INE'

def output(data_list,filename):
    with open(filename,'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["cmt"])
        for x in data_list:
            writer.writerow([x])    

def cmt_dict2code(cmt_dict):
    cmt_list = [x for l in cmt_dict.values() for x in l]
    cmt_list = [x + '.' + exchange(x,cmt_dict) for x in cmt_list]
    return cmt_list

commodities_all = {
'DCE':['A','B','BB','C','CS','FB','Y','P','JD','L','PP','V','J','JM','I','M'],
'CZC':['WH','PM','RI','RS','JR','LR','CY','SF','SM','CF','SR','OI','RM','TA','FG','MA','ZC'],
'SHF':['CU','ZN','AL','PB','NI','AU','AG','SN','BU','RU','HC','RB','WR','FU'],
'CFE':['IC','IH','IF','T','TF'],
'INE':['SC']}

commodities_daily = {
'DCE':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I'],
'CZC':['CF','SR','RM','TA','FG','MA','ZC'],
'SHF':['CU','ZN','AL','NI','AU','AG','BU','RU','HC','RB'],
'CFE':['IC','IH','IF','T','TF']}


cmt_all_list = cmt_dict2code(commodities_all)	
cmt_all_list_filename = '../cmt_list/cmt_list.csv'   
output(cmt_all_list,cmt_all_list_filename)

cmt_daily_list = cmt_dict2code(commodities_daily)	
cmt_daily_list_filename = '../cmt_list/cmt_daily_list.csv'   
output(cmt_daily_list,cmt_daily_list_filename)









