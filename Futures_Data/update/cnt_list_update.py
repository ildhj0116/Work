# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 10:31:41 2018

@author: Administrator
"""

import pandas as pd
from WindPy import w
w.start()

def cnt_list_download(end_date):
    start_date = "1999-01-01"
    cmt_list = pd.read_csv("../cmt_list/cmt_list.csv",index_col=0).index.tolist()
    for cmt in cmt_list:        
        cnt_df = w.wset("futurecc","startdate="+start_date+";enddate="+end_date+";wind_code="+cmt+";\
                        field=wind_code,contract_issue_date,last_trade_date")
        cnt_df = pd.DataFrame(cnt_df.Data[1:],index=cnt_df.Fields[1:],columns=cnt_df.Data[0]).T
        cnt_df.to_csv("../cnt_list/"+cmt[:-4]+".csv")
    print "全部合约列表更新完毕"


if __name__ == "__main__":
    end_date = "2018-04-19"
    cnt_list_download(end_date)
    
    
    
#    cmt_list = ["IF","IC","IH"]
#    for cmt in cmt_list:
#        cnt_list = pd.read_csv("../cnt_list/"+cmt+".csv",index_col=0).index.tolist()
#        cl = pd.read_csv("../data_cl/"+cmt+".csv",index_col=0,parse_dates=[0])
#        oi = pd.read_csv("../data_oi/"+cmt+".csv",index_col=0,parse_dates=[0])
#        op = pd.read_csv("../data_open/"+cmt+".csv",index_col=0,parse_dates=[0])
#        vol = pd.read_csv("../data_vol/"+cmt+".csv",index_col=0,parse_dates=[0])
#        new_list = [x for x in cnt_list if x in cl.columns.tolist()]
#        new_cl = cl[new_list].copy()
#        new_oi = oi[new_list].copy()
#        new_op = op[new_list].copy()
#        new_vol = vol[new_list].copy()
#        new_cl.to_csv("../data_cl/"+cmt+".csv")
#        new_oi.to_csv("../data_oi/"+cmt+".csv")
#        new_op.to_csv("../data_open/"+cmt+".csv")
#        new_vol.to_csv("../data_vol/"+cmt+".csv")
    