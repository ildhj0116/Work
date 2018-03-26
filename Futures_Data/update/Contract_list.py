# encoding: UTF-8
# 所有合约

def exchange(cmt,commodities):
        if cmt in commodities['DCE']:
            return 'DCE'
        elif cmt in commodities['CZC']:
            return 'CZC'
        elif cmt in commodities['SHF']:
            return 'SHF'
        else:
            return 'CFE'

commodities_all = {
'DCE':['A','B','BB','C','CS','FB','Y','P','JD','L','PP','V','J','JM','I'],
'CZC':['WH','PM','RI','RS','JR','LR','CY','SF','SM','CF','SR','OI','RM','TA','FG','MA','ZC'],
'SHF':['CU','ZN','AL','PB','SN','NI','AU','AG','SN','BU','RU','HC','RB','WR','FU','SC'],
'CFE':['IC','IH','IF','T','TF'],
'INE':['SC']}

cmt_all_list = [x for l in commodities_all.values() for x in l]
cmt_all_list = [x + '.' + exchange(x,commodities_all) for x in cmt_all_list]

import csv
with open('../cmt_list/cmt_list.csv','wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["cmt"])
    for x in cmt_all_list:
        writer.writerow([x])

