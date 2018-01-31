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

def oi_download_process(date,df):
    tmp_df = df[df["date"]==date].copy()
    tmp_df.set_index("member_name",inplace=True)
    tmp_df.drop([u"前五名合计",u"前十名合计",u"前二十名合计"],inplace=True)
    #tmp_df.drop("date",axis=1,inplace=True)
    return tmp_df

def OI_Construct(main_cnt_df):
    all_cmt_oi_list = []
    date_list = main_cnt_df.index
    for cmt in main_cnt_df.columns:
        cnt_series = main_cnt_df[cmt]
        unique_cnt_list = cnt_series.unique()
        exchange = exchange_of_cmt(cmt)
        oi_df_list = []
        for cnt in unique_cnt_list:
            part_cnt = cnt_series[cnt_series==cnt]
            tmp_start_date = part_cnt.index[0]
            tmp_end_date = part_cnt.index[-1]
            if exchange=='DCE':
                tmp_oi_data = w.wset("futureoir","startdate="+tmp_start_date+";enddate="+tmp_end_date+\
                                     "varity="+cmt+";wind_code="+cnt+";order_by=long;ranks=all;field=date,"+\
                                     "member_name,long_position,short_position,vol")
                
                tmp_oi_data = pd.DataFrame(tmp_oi_data.Data, index=tmp_oi_data.Fields).T
                #tmp_oi_data.set_index(["date","member_name"],inplace=True)
                tmp_date_list = tmp_oi_data["date"].unique().tolist()
                tmp_date_list.reverse()
                for d in tmp_date_list:
                    tmp_df = oi_download_process(d,tmp_oi_data)                    
                    oi_df_list.append(tmp_df)
            else:
                tmp_long_data = w.wset("futureoir","startdate="+tmp_start_date+";enddate="+tmp_end_date+\
                                     "varity="+cmt+";wind_code="+cnt+";order_by=long;ranks=all;field=date,"+\
                                     "member_name,long_position")
                tmp_long_data = pd.DataFrame(tmp_long_data.Data, index=tmp_long_data.Fields).T
                tmp_short_data = w.wset("futureoir","startdate="+tmp_start_date+";enddate="+tmp_end_date+\
                                     "varity="+cmt+";wind_code="+cnt+";order_by=short;ranks=all;field=date,"+\
                                     "member_name,short_position")   
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
                    tmp_vol_df = oi_download_process(d,tmp_vol_data)
                    tmp_df = pd.concat([tmp_long_df,tmp_short_df,tmp_vol_df],axis=1)
                    tmp_nan_df = tmp_df[tmp_df.T.isnull().any()]
                    tmp_notnan_df = tmp_df[~tmp_df.T.isnull().any()].copy()
                    tmp_notnan_df.loc["others"] = tmp_nan_df.sum()
                    oi_df_list.append(tmp_notnan_df)
            print cnt+"处理完毕"
        tmp_series = pd.Series(oi_df_list,index=date_list,name=cmt)
        all_cmt_oi_list.append(tmp_series)
    oi_report_df = pd.concat(all_cmt_oi_list,axis=1)
    return oi_report_df
                    
            
#        single_cmt_oi_data = pd.concat(oi_df_list)
#        single_cmt_oi_data.columns = pd.MultiIndex.from_product([[cmt],single_cmt_oi_data.columns])
#        all_cmt_oi_list.append(single_cmt_oi_data)    
            
    
if __name__ == "__main__":
    main_cnt_df = pd.read_csv("main_cnt_without_DCE.csv",index_col=0)
    main_cnt_df["date"] = [datetime.strptime(x,"%Y/%m/%d") for x in main_cnt_df.index]
    start_date = datetime.strptime("2016-12-31","%Y-%m-%d")
    end_date = datetime.strptime("2018-1-25","%Y-%m-%d")
    main_cnt_target = main_cnt_df[(main_cnt_df["date"]>start_date) & (main_cnt_df["date"]<end_date)].copy()
    main_cnt_target.drop("date",axis=1,inplace=True)
    df = OI_Construct(main_cnt_target)
    
    df.to_pickle("OI.tmp")
    #try_df = pd.read_pickle("OI.tmp")
    
    """
    main_cnt_series_list = []    
    for cmt in cmt_list:
        #持仓量矩阵
        cmt_data = w.wset("futurecc","wind_code="+cmt)
        cnt_data = pd.DataFrame(data=cmt_data.Data,index=cmt_data.Fields).T
        if datetime.strptime(start_date,"%Y-%m-%d") < cnt_data["contract_issue_date"].iloc[0]:
            base_date = cnt_data["contract_issue_date"].iloc[0]+timedelta(days=1)
        else:
            base_date = start_date
        effective_cnt = copy.deepcopy(cnt_data)
        effective_cnt.set_index('wind_code',inplace=True)
        
        cnt_list = ",".join(list(effective_cnt.index))
        oi_data = w.wsd(cnt_list, "oi",base_date,end_date,"")
        oi_data = pd.DataFrame(data=oi_data.Data,index=oi_data.Codes,columns=oi_data.Times).T.fillna(0)
        
        #考虑持仓量相同的情况
        oi_data = oi_data[True-(oi_data.max(axis=1)==0)]
        max_count_f = lambda x: x[x==x.max()].count()
        max_oi_count = oi_data.apply(max_count_f,axis=1)
        print cmt+"持仓量相等情况个数%d" % len(max_oi_count[max_oi_count>1])
        
        #找最大持仓量合约
        max_oi_cnt_f = lambda x: x.idxmax()
        max_oi_cnt = oi_data.apply(max_oi_cnt_f,axis=1)
        
        
        main_cnt_list = list(max_oi_cnt)
        original_cnt = main_cnt_list[0]
        sub_cnt = main_cnt_list[0]
        
        decide_flag = False        
        back_cnt_list = []
        filtered_main_cnt_list = copy.deepcopy(main_cnt_list)
        
        for t in range(len(main_cnt_list)):
            if decide_flag==False:
                if main_cnt_list[t]==sub_cnt:
                    filtered_main_cnt_list[t] = sub_cnt
                else:
                    if main_cnt_list[t] in back_cnt_list:
                        filtered_main_cnt_list[t] = sub_cnt
                    else:
                        original_cnt = sub_cnt
                        sub_cnt = main_cnt_list[t]
                        decide_flag = True
                        filtered_main_cnt_list[t] = original_cnt
                        decide_day = 1
            elif decide_flag==True:
                filtered_main_cnt_list[t] = original_cnt
                if main_cnt_list[t]==sub_cnt:
                    decide_day += 1
                    if decide_day>=decide_param:
                        decide_flag = False
                        back_cnt_list.append(original_cnt)
                elif main_cnt_list[t]==original_cnt:
                    decide_flag = False
                    sub_cnt = main_cnt_list[t]
                else:
                    sub_cnt = main_cnt_list[t]        
        filter_main_cnt = pd.Series(filtered_main_cnt_list,index=max_oi_cnt.index)
        filter_main_cnt.name = cmt
        main_cnt_series_list.append(filter_main_cnt)
    main_cnt_df = pd.concat(main_cnt_series_list,axis=1)
    return main_cnt_df
    """
    
    