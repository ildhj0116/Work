# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 15:33:06 2018

@author: Administrator
"""

import pandas as pd
import gc
from datetime import datetime,timedelta
from WindPy import w
w.start()


cmt_list = pd.read_csv("../cmt_list/cmt_list.csv")
cmt_list = cmt_list["cmt"].tolist()
#cmt_list = ["SN.SHF"]

#def data_download(cmt,start_date,end_date):
#    tmp_cnt_list = w.wset("futurecc","startdate="+start_date+";enddate="+end_date+";wind_code="+cmt+";field=wind_code")
#    tmp_cnt_list = tmp_cnt_list.Data[0]
#    tmp_download_cl_list = []
#    tmp_download_open_list = []
#    tmp_download_vol_list = []
#    tmp_download_oi_list = []
#    for cnt in tmp_cnt_list:
#        tmp_download_data = w.wsd(cnt, "close,open,volume,oi", start_date, end_date, "")
#        time_index = [datetime.strptime(str(x),"%Y-%m-%d") for x in tmp_download_data.Times]
#        tmp_cl = pd.Series(tmp_download_data.Data[0],index=time_index,name=cnt)
#        tmp_open = pd.Series(tmp_download_data.Data[1],index=time_index,name=cnt)
#        tmp_vol = pd.Series(tmp_download_data.Data[2],index=time_index,name=cnt)
#        tmp_oi = pd.Series(tmp_download_data.Data[3],index=time_index,name=cnt)
#        tmp_download_cl_list.append(tmp_cl)
#        tmp_download_open_list.append(tmp_open)
#        tmp_download_vol_list.append(tmp_vol)
#        tmp_download_oi_list.append(tmp_oi)
#    tmp_update_cl = pd.concat(tmp_download_cl_list,axis=1)
#    tmp_update_open = pd.concat(tmp_download_open_list,axis=1)
#    tmp_update_vol = pd.concat(tmp_download_vol_list,axis=1)
#    tmp_update_oi = pd.concat(tmp_download_oi_list,axis=1)
#    return tmp_update_cl,tmp_update_open,tmp_update_vol,tmp_update_oi
#
#last_update_date  = "2017-04-02"
#today = "2018-04-03"
#today = datetime.today().date().strftime("%Y-%m-%d")

for cmt in cmt_list:
    try:
        tmp_close = pd.read_csv("../data_cl/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
        tmp_open = pd.read_csv("../data_open/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
        tmp_vol = pd.read_csv("../data_vol/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
        tmp_oi = pd.read_csv("../data_oi/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
    except IOError:
        print "没有品种历史数据:" + cmt + "，将新建文件。"        
    else: 
        # 删除最后一行
#        tmp_close_new = tmp_close.iloc[:-1,:].copy()
#        tmp_open_new = tmp_open.iloc[:-1,:].copy()
#        tmp_vol_new = tmp_vol.iloc[:-1,:].copy()
#        tmp_oi_new = tmp_oi.iloc[:-1,:].copy()
        # 删除最后一列
        tmp_close_new = tmp_close.iloc[:,:-1].copy()
        tmp_open_new = tmp_open.iloc[:,:-1].copy()
        tmp_vol_new = tmp_vol.iloc[:,:-1].copy()
        tmp_oi_new = tmp_oi.iloc[:,:-1].copy()
        tmp_close_new.to_csv("../data_cl/"+cmt[:-4]+".csv")
        tmp_open_new.to_csv("../data_open/"+cmt[:-4]+".csv")
        tmp_vol_new.to_csv("../data_vol/"+cmt[:-4]+".csv")
        tmp_oi_new.to_csv("../data_oi/"+cmt[:-4]+".csv")
        print cmt + "删除完毕"
