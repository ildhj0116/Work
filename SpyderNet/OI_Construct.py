# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:58:47 2018

@author: Administrator
"""

import pandas as pd
from WindPy import w
from datetime import datetime,timedelta
import copy

w.start()
def exchange_of_cmt(cmt):
    return cmt[-3:]

def code_of_cmt(cmt):
    return cmt[:-4]

def oi_download_process(date,df):
    tmp_df = df[df["date"]==date].copy()
    tmp_df.set_index("member_name",inplace=True)
    tmp_df.drop([u"前五名合计",u"前十名合计",u"前二十名合计"],inplace=True)
    return tmp_df

def OI_Construct(cnt_series):
    cmt = cnt_series.name
    unique_cnt_list = cnt_series.dropna().unique()
    exchange = exchange_of_cmt(cmt)
    oi_df_list = []
    date_list = []
    total_oi_vol_list =[]
    for cnt in unique_cnt_list:
        part_cnt = cnt_series[cnt_series==cnt]
        tmp_start_date = part_cnt.index[0]
        tmp_end_date = part_cnt.index[-1]
        if exchange=='DCE':
            tmp_oi_data = w.wset("futureoir","startdate="+tmp_start_date+";enddate="+tmp_end_date+\
                                 "varity="+cmt+";wind_code="+cnt+";order_by=long;ranks=all;field=date,"+\
                                 "member_name,long_position,long_position_increase,short_position,"+\
                                 "short_position_increase,vol")                
            
            tmp_oi_data = pd.DataFrame(tmp_oi_data.Data, index=tmp_oi_data.Fields).T
            tmp_date_list = tmp_oi_data["date"].unique().tolist()
            tmp_date_list.reverse()
            for d in tmp_date_list:
                tmp_df = oi_download_process(d,tmp_oi_data)                    
                oi_df_list.append(tmp_df)
                date_list.append(d)
        else:
            tmp_long_data = w.wset("futureoir","startdate="+tmp_start_date+";enddate="+tmp_end_date+\
                                 "varity="+cmt+";wind_code="+cnt+";order_by=long;ranks=all;field=date,"+\
                                 "member_name,long_position,long_position_increase")
            tmp_long_data = pd.DataFrame(tmp_long_data.Data, index=tmp_long_data.Fields).T
            tmp_short_data = w.wset("futureoir","startdate="+tmp_start_date+";enddate="+tmp_end_date+\
                                 "varity="+cmt+";wind_code="+cnt+";order_by=short;ranks=all;field=date,"+\
                                 "member_name,short_position,short_position_increase")   
            tmp_short_data = pd.DataFrame(tmp_short_data.Data, index=tmp_short_data.Fields).T

            tmp_vol_data = w.wset("futurevir","startdate="+tmp_start_date+";enddate="+tmp_end_date+\
                                 "varity="+cmt+";wind_code="+cnt+";ranks=all;field=date,"+\
                                 "member_name,vol")            
            tmp_vol_data = pd.DataFrame(tmp_vol_data.Data, index=tmp_vol_data.Fields).T
            tmp_date_list = tmp_long_data["date"].unique().tolist()
            tmp_date_list.reverse()
            for d in tmp_date_list:
                tmp_long_df = oi_download_process(d,tmp_long_data)
                tmp_short_df = oi_download_process(d,tmp_short_data)
                tmp_short_df.drop("date",axis=1,inplace=True)
                tmp_vol_df = oi_download_process(d,tmp_vol_data)
                tmp_vol_df.drop("date",axis=1,inplace=True)
                tmp_df = pd.concat([tmp_long_df,tmp_short_df,tmp_vol_df],axis=1)
                tmp_nan_df = tmp_df[tmp_df.T.isnull().any()]
                tmp_notnan_df = tmp_df[~tmp_df.T.isnull().any()].copy()
                tmp_notnan_df.loc["others"] = tmp_nan_df.drop("date",axis=1).sum()
                oi_df_list.append(tmp_notnan_df)
                date_list.append(d)
        #下载总成交量和持仓量
        tmp_total = w.wsd(cnt,"volume,oi",tmp_start_date,tmp_end_date,"")
        tmp_total = pd.DataFrame(tmp_total.Data, index=tmp_total.Fields,columns=tmp_total.Times).T
        total_oi_vol_list.append(tmp_total)
        print cnt+"处理完毕"
    tmp_series = pd.Series(oi_df_list,index=date_list,name=cmt)
    total_oi_volume_df = pd.concat(total_oi_vol_list)
    return tmp_series,total_oi_volume_df
                    
    
if __name__ == "__main__":
    main_cnt_df = pd.read_csv("main_cnt_revised.csv",index_col=0)
    main_cnt_df["date"] = [datetime.strptime(x,"%Y-%m-%d") for x in main_cnt_df.index]
    start_date = datetime.strptime("2009-12-31","%Y-%m-%d")
    end_date = datetime.strptime("2018-1-25","%Y-%m-%d")
    main_cnt_target = main_cnt_df[(main_cnt_df["date"]>start_date) & (main_cnt_df["date"]<end_date)].copy()
    main_cnt_target.drop("date",axis=1,inplace=True)
    
    for cmt in ["IF.CFE"]:
        chart_df,total_oi_volume = OI_Construct(main_cnt_target[cmt])    
        chart_df.to_pickle("OI_data\OI_" + code_of_cmt(cmt) + ".tmp")
        total_oi_volume.to_csv("OI_data\OI_total_" + code_of_cmt(cmt) + ".csv")
        print cmt + "下载完毕"
        
    #try_df = pd.read_pickle("OI.tmp")
    

    
    