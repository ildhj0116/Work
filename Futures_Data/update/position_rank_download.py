# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 09:35:00 2018

@author: Administrator
"""

import pandas as pd
from WindPy import w
from datetime import datetime,date
from WindError import *
import os

w.start()

def position_rank_download_cmt(start_date,end_date,cmt):
    long_position = w.wset("futureoir","startdate="+start_date+";enddate="+end_date+";varity="+cmt+";order_by=long;ranks=all;\
                           field=date,member_name,long_position,long_position_increase,long_potion_rate")
    WindCheck(long_position)
    long_position = pd.DataFrame(long_position.Data,index=long_position.Fields).T
    short_position = w.wset("futureoir","startdate="+start_date+";enddate="+end_date+";varity="+cmt+";order_by=short;ranks=all;\
                            field=date,member_name,short_position,short_position_increase,short_position_rate")
    short_position = pd.DataFrame(short_position.Data,index=short_position.Fields).T
    vol = w.wset("futurevir","startdate="+start_date+";enddate="+end_date+";varity="+cmt+";ranks=all;\
                 field=date,member_name,vol,vol_increase,vol_rate")
    vol = pd.DataFrame(vol.Data,index=vol.Fields).T
    long_position = long_position.set_index([long_position["date"],long_position["member_name"]])
    short_position = short_position.set_index([short_position["date"],short_position["member_name"]])
    
    long_position = long_position.set_index(["date","member_name"],drop=True)
    short_position = short_position.set_index(["date","member_name"],drop=True)
    vol = vol.set_index(["date","member_name"],drop=True)
    df = pd.concat([long_position,short_position,vol],axis=1)
    return df
    
def position_rank_update(start_date,end_date):
    cmt_list = pd.read_csv("../cmt_list/cmt_daily_list.csv")        
    for cmt in cmt_list.iloc[:,0].values:
        tmp_position_rank = position_rank_download_cmt(start_date,end_date,cmt)
        for name,group in tmp_position_rank.groupby(level=0):
            group.index = group.index.droplevel()
            today = name.to_pydatetime().strftime("%Y-%m-%d")
            tmp_path = "../position_rank/cmt/" + today
            if not os.path.exists(tmp_path):
                os.makedirs(tmp_path)
            group.to_csv(tmp_path+"/"+cmt[:-4]+".csv",encoding="utf_8_sig")
        print cmt + "持仓排名更新完毕"
        
def position_rank_without_cmt(start_date,end_date,cmt_list):       
    for cmt in cmt_list:
        try:
            tmp_position_rank = position_rank_download_cmt(start_date,end_date,cmt)
        except WindError as we:
            print cmt + " " + we.errorinfo
            raise
        except EmptyError as ee:
            print cmt + ee.errorinfo
            continue
        else:
            for name,group in tmp_position_rank.groupby(level=0):
                group.index = group.index.droplevel()
                today = name.to_pydatetime().strftime("%Y-%m-%d")
                tmp_path = "../position_rank/cmt/" + today
                if not os.path.exists(tmp_path):
                    os.makedirs(tmp_path)
                group.to_csv(tmp_path+"/"+cmt[:-4]+".csv",encoding="utf_8_sig")
            print cmt + "持仓排名更新完毕"        

    
if __name__ == "__main__":
    cmt_list = pd.read_csv("../main_cnt/data/main_cnt_total.csv",index_col=0)
    cmt_list = cmt_list.columns.tolist()
    start_date = "2014-01-01"
    end_date = "2014-12-31"
    position_rank_without_cmt(start_date,end_date,cmt_list)




###############################################################################
"""
删除模块
"""        
############################################################################### 
#   
#    date_list = main_cnt_df.index[main_cnt_df.index > datetime(2018,1,1)].tolist()
#    date_list = [x.to_pydatetime().strftime("%Y-%m-%d") for x in date_list]
#    for tmp_date in date_list:
#        for cmt in cmt_list:
#            tmp_df = pd.read_csv("../position_rank/cmt/"+tmp_date+"/"+cmt+".csv", index_col=0, encoding="utf_8_sig")
#            tmp_df.to_csv("../position_rank/cmt/"+tmp_date+"/"+cmt[:-4]+".csv",encoding="utf_8_sig")
#            os.remove("../position_rank/cmt/"+tmp_date+"/"+cmt+".csv")
#            
            
            
            
            
            
            
            
            
            
    