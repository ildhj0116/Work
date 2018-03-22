# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 09:09:30 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from WindPy import w
import copy

def main_cnt_update(main_cnt_df,decide_param=2):
    cmt_list = main_cnt_df.columns.tolist()
    today = datetime.today()
    #若今天的日期小于等于已存在的日期，则一定是日期出现问题或不需要更新
    if today <= main_cnt_df.index[-1]:
        print "更新日期错误"
        return np.nan
    else:
        start_date = main_cnt_df.index[-decide_param].strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        main_cnt_series_list = []    

        for cmt in cmt_list:
            cmt_data = w.wset("futurecc","startdate="+start_date+";enddate="+end_date+";wind_code="+cmt)
            cnt_data = pd.DataFrame(data=cmt_data.Data,index=cmt_data.Fields).T
            if datetime.strptime(start_date,"%Y-%m-%d") < cnt_data["contract_issue_date"].iloc[0]:
                base_date = cnt_data["contract_issue_date"].iloc[0]+timedelta(days=1)
            else:
                base_date = start_date
            effective_cnt = cnt_data.copy()
            effective_cnt.set_index('wind_code',inplace=True)
            cnt_all_list = list(effective_cnt.index)
            cnt_list = ",".join(cnt_all_list)
            oi_data = w.wsd(cnt_list, "oi",base_date,end_date,"")
            oi_data = pd.DataFrame(data=oi_data.Data,index=oi_data.Codes,columns=oi_data.Times).T.fillna(0)
            
            
            #考虑持仓量相同的情况
            oi_data = oi_data[True-(oi_data.max(axis=1)==0)]
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
            
           #
           
            
            
            #找最大持仓量合约
            max_oi_cnt_f = lambda x: x.idxmax()
            max_oi_cnt = oi_data.apply(max_oi_cnt_f,axis=1)
            
            #
            if len(max_oi_cnt) <= decide_param:
                print "无需更新"
                return np.nan
            else:
                main_cnt_list = list(max_oi_cnt)
                original_cnt = main_cnt_list[0]
                sub_cnt = main_cnt_df[cmt][-decide_param]
                
                decide_flag = False        
                back_cnt_list = main_cnt_df[cmt].unique().tolist()
                back_cnt_list.pop()
                filtered_main_cnt_list = copy.deepcopy(main_cnt_list)
                
                for t in range(len(main_cnt_list)):
                    date = max_oi_cnt.index[t]
                    if effective_cnt.loc[original_cnt,"last_trade_date"].date() >= date:
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
                filter_main_cnt = pd.Series(filtered_main_cnt_list[decide_param:],index=max_oi_cnt.index[decide_param:])
                filter_main_cnt.name = cmt
                main_cnt_series_list.append(filter_main_cnt)
        main_cnt_df = pd.concat(main_cnt_series_list,axis=1)
        return main_cnt_df
        
        
        


if __name__ == "__main__":
    main_cnt_df = pd.read_csv("../../data/main_cnt_total.csv",parse_dates=[0],index_col=0)
    update_main_df = main_cnt_update(main_cnt_df)
    if np.isnan(update_main_df):
        print "无更新"
    else:
        update_main_df.to_csv("../../data/main_cnt_total.csv",mode="a",header=None)
    
    
    
    
    