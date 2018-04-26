# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 08:40:38 2018

@author: Administrator
"""

import pandas as pd
from WindPy import w
from datetime import datetime,timedelta
import copy

w.start()

def Main_Contract(cmt_list, start_date, end_date, decide_param = 2):

    main_cnt_series_list = []    
    for cmt in cmt_list:
        #持仓量矩阵
        cmt_data = w.wset("futurecc","startdate="+start_date+";enddate="+end_date+";wind_code="+cmt)
        cnt_data = pd.DataFrame(data=cmt_data.Data,index=cmt_data.Fields).T
        if len(cnt_data) == 0:
             main_cnt_series_list.append(pd.Series([],name=cmt))
             continue
        else:
            if datetime.strptime(start_date,"%Y-%m-%d") < cnt_data["contract_issue_date"].iloc[0]:
                base_date = cnt_data["contract_issue_date"].iloc[0]+timedelta(days=1)
            else:
                base_date = start_date
            effective_cnt = copy.deepcopy(cnt_data)
            effective_cnt.set_index('wind_code',inplace=True)
            cnt_all_list = list(effective_cnt.index)
            cnt_list = ",".join(cnt_all_list)
            oi_data = w.wsd(cnt_list, "oi",base_date,end_date,"")
            oi_data = pd.DataFrame(data=oi_data.Data,index=oi_data.Codes,columns=oi_data.Times).T.fillna(0)
            
            
            #考虑持仓量相同的情况
            oi_data = oi_data[~(oi_data.max(axis=1)==0)]
            max_count_f = lambda x: x[x==x.max()].count()
            max_oi_count = oi_data.apply(max_count_f,axis=1)
            print cmt+"持仓量相等情况个数%d" % len(max_oi_count[max_oi_count>1])
            
            #处理数据
            #万得下载的持仓量数据有时在合约未上市或退市后仍有数据，导致之后横向比较出现错误，因此需要过滤掉无效数据
            for cnt in cnt_all_list:
                last_trade_date = effective_cnt.loc[cnt,"last_trade_date"].date()
                if last_trade_date in oi_data.index:
                    oi_data.loc[oi_data.index>last_trade_date,cnt] = 0
                first_trade_date = effective_cnt.loc[cnt,"contract_issue_date"].date()
                if first_trade_date in oi_data.index:
                    oi_data.loc[oi_data.index<first_trade_date,cnt] = 0
            
            
            
            
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
                today = max_oi_cnt.index[t]
                if effective_cnt.loc[original_cnt,"last_trade_date"].date() >= today:
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
                                original_cnt = sub_cnt
                                back_cnt_list = cnt_all_list[:(cnt_all_list.index(sub_cnt))]
                        elif main_cnt_list[t]==original_cnt:
                            decide_flag = False
                            sub_cnt = main_cnt_list[t]
                        else:
                            sub_cnt = main_cnt_list[t]  
                else:
                    filtered_main_cnt_list[t] = main_cnt_list[t]
                    original_cnt = main_cnt_list[t]
                    sub_cnt = main_cnt_list[t]
                    back_cnt_list = cnt_all_list[:(cnt_all_list.index(sub_cnt))]
                    decide_flag = False 
            filter_main_cnt = pd.Series(filtered_main_cnt_list,index=max_oi_cnt.index)
            filter_main_cnt.name = cmt
            main_cnt_series_list.append(filter_main_cnt)
    main_cnt_df = pd.concat(main_cnt_series_list,axis=1)
    return main_cnt_df
    
commodities={
'DCE':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I'],
'CZC':['CF','SR','RM','TA','FG','MA','ZC','AP'],
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
    base_date = "2017-12-20"
    end_date = "2018-04-25"    
    cmt_list = [exchange(x) for x in cnt_list]
    cmt_list = ["AP.CZC"]
    main_cnt_df = Main_Contract(cmt_list,base_date,end_date)
    main = pd.read_csv("../../data/main_cnt_total.csv",index_col=0,parse_dates=[0])
    main1 = pd.concat([main,main_cnt_df],axis=1)
    
    #main_cnt_df.to_csv("main_cnt_MA.csv")





















    
   