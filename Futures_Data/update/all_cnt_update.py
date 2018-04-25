# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 10:44:20 2018

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

def data_download(cmt,start_date,end_date):
    tmp_cnt_list = w.wset("futurecc","startdate="+start_date+";enddate="+end_date+";wind_code="+cmt+";field=wind_code")
    tmp_cnt_list = tmp_cnt_list.Data[0]
    tmp_download_cl_list = []
    tmp_download_open_list = []
    tmp_download_vol_list = []
    tmp_download_oi_list = []
    tmp_download_high_list = []
    tmp_download_low_list = []
    for cnt in tmp_cnt_list:
        tmp_download_data = w.wsd(cnt, "close,open,volume,oi,high,low", start_date, end_date, "")
        time_index = [datetime.strptime(str(x),"%Y-%m-%d") for x in tmp_download_data.Times]
        tmp_cl = pd.Series(tmp_download_data.Data[0],index=time_index,name=cnt)
        tmp_open = pd.Series(tmp_download_data.Data[1],index=time_index,name=cnt)
        tmp_vol = pd.Series(tmp_download_data.Data[2],index=time_index,name=cnt)
        tmp_oi = pd.Series(tmp_download_data.Data[3],index=time_index,name=cnt)
        tmp_high = pd.Series(tmp_download_data.Data[4],index=time_index,name=cnt)
        tmp_low = pd.Series(tmp_download_data.Data[5],index=time_index,name=cnt)
        tmp_download_cl_list.append(tmp_cl)
        tmp_download_open_list.append(tmp_open)
        tmp_download_vol_list.append(tmp_vol)
        tmp_download_oi_list.append(tmp_oi)
        tmp_download_high_list.append(tmp_high)
        tmp_download_low_list.append(tmp_low)
    tmp_update_cl = pd.concat(tmp_download_cl_list,axis=1)
    tmp_update_open = pd.concat(tmp_download_open_list,axis=1)
    tmp_update_vol = pd.concat(tmp_download_vol_list,axis=1)
    tmp_update_oi = pd.concat(tmp_download_oi_list,axis=1)
    tmp_update_high = pd.concat(tmp_download_vol_list,axis=1)
    tmp_update_low = pd.concat(tmp_download_oi_list,axis=1)
    return tmp_update_cl,tmp_update_open,tmp_update_vol,tmp_update_oi,tmp_update_high,tmp_update_low


def quotes_data_update(today):    
    for cmt in cmt_list:
        try:
            tmp_close = pd.read_csv("../data_cl/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
            tmp_open = pd.read_csv("../data_open/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
            tmp_vol = pd.read_csv("../data_vol/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
            tmp_oi = pd.read_csv("../data_oi/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
            tmp_high = pd.read_csv("../data_high/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
            tmp_low = pd.read_csv("../data_low/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0)
        except IOError:
            print "没有品种历史行情数据:" + cmt + "，将新建文件。"
            start_date = today
            end_date = today
            tmp_update_cl,tmp_update_open,tmp_update_vol,tmp_update_oi,tmp_update_high,tmp_update_low = data_download(cmt,start_date,
                                                                                                                      end_date)
            tmp_update_cl.to_csv("../data_cl/"+cmt[:-4]+".csv")
            tmp_update_open.to_csv("../data_open/"+cmt[:-4]+".csv")
            tmp_update_vol.to_csv("../data_vol/"+cmt[:-4]+".csv")
            tmp_update_oi.to_csv("../data_oi/"+cmt[:-4]+".csv")
            tmp_update_high.to_csv("../data_high/"+cmt[:-4]+".csv")
            tmp_update_low.to_csv("../data_low/"+cmt[:-4]+".csv")
        else:
            start_date = (min([tmp_close.index[-1],tmp_open.index[-1],tmp_vol.index[-1],tmp_oi.index[-1],tmp_high.index[-1],tmp_low.index[-1]]).date() 
                          + timedelta(days=1)).strftime("%Y-%m-%d")
            end_date = today
            if datetime.strptime(start_date,"%Y-%m-%d") > datetime.strptime(end_date,"%Y-%m-%d"):
                print cmt + "日期错误，无法更新行情数据"
            else:
                tmp_update_cl,tmp_update_open,tmp_update_vol,tmp_update_oi,tmp_update_high,tmp_update_low = data_download(cmt,start_date,
                                                                                                                          end_date)
                if len(tmp_update_cl) > 0:
                    update_cnt_list = [x for x in list(tmp_update_cl.columns.values) if x not in list(tmp_close.columns.values)]
                    new_cnt_list = list(tmp_close.columns.values)
                    new_high_low_list = list(tmp_high.columns.values)
                    new_cnt_list.extend(update_cnt_list)
                    new_high_low_list.extend(update_cnt_list)
                    tmp_close_new = tmp_close.append(tmp_update_cl)
                    tmp_open_new = tmp_open.append(tmp_update_open)
                    tmp_vol_new = tmp_vol.append(tmp_update_vol)
                    tmp_oi_new = tmp_oi.append(tmp_update_oi)
                    tmp_high_new = tmp_high.append(tmp_update_high)
                    tmp_low_new = tmp_low.append(tmp_update_low)
                    if cmt in ["IC.CFE","IF.CFE","IH.CFE"]:
                        his_cnt_list = pd.read_csv("../cnt_list/"+cmt[:-4]+".csv",index_col=0).index.tolist()
                        new_cnt_list = [x for x in his_cnt_list if x in new_cnt_list]
                    tmp_close_new = tmp_close_new[new_cnt_list]
                    tmp_open_new = tmp_open_new[new_cnt_list]
                    tmp_vol_new = tmp_vol_new[new_cnt_list]
                    tmp_oi_new = tmp_oi_new[new_cnt_list]
                    tmp_high_new = tmp_high_new[new_high_low_list]
                    tmp_low_new = tmp_low_new[new_high_low_list]
                    tmp_close_new.to_csv("../data_cl/"+cmt[:-4]+".csv")
                    tmp_open_new.to_csv("../data_open/"+cmt[:-4]+".csv")
                    tmp_vol_new.to_csv("../data_vol/"+cmt[:-4]+".csv")
                    tmp_oi_new.to_csv("../data_oi/"+cmt[:-4]+".csv")
                    tmp_high_new.to_csv("../data_high/"+cmt[:-4]+".csv")
                    tmp_low_new.to_csv("../data_low/"+cmt[:-4]+".csv")
                    print cmt + "行情数据更新完毕"
                else:
                    print cmt + "已更新，无需更新"
    
def high_low_download(start_date,end_date):
    cmt_list = ["T.CFE","TF.CFE"]
    for cmt in cmt_list:

        tmp_cnt_list = w.wset("futurecc","startdate="+start_date+";enddate="+end_date+";wind_code="+cmt+";field=wind_code")
        tmp_cnt_list = tmp_cnt_list.Data[0]
        tmp_download_high_list = []
        tmp_download_low_list = []

        for cnt in tmp_cnt_list:
            tmp_download_data = w.wsd(cnt, "high,low", start_date, end_date, "")
            time_index = [datetime.strptime(str(x),"%Y-%m-%d") for x in tmp_download_data.Times]
            tmp_high = pd.Series(tmp_download_data.Data[0],index=time_index,name=cnt)
            tmp_low = pd.Series(tmp_download_data.Data[1],index=time_index,name=cnt)

            tmp_download_high_list.append(tmp_high)
            tmp_download_low_list.append(tmp_low)

        tmp_update_high = pd.concat(tmp_download_high_list,axis=1)
        tmp_update_low = pd.concat(tmp_download_low_list,axis=1)

        
        tmp_update_high.to_csv("../data_high/"+cmt[:-4]+".csv")
        tmp_update_low.to_csv("../data_low/"+cmt[:-4]+".csv")
        print cmt + "下载完毕"
       

if __name__ == "__main__":
    start_date = "2015-01-01"
    end_date = "2018-04-24"
    high_low_download(start_date,end_date)
        
        
        
        
