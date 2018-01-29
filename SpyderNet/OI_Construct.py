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

def OI_Construct(main_cnt_df):
    date_list = main_cnt_df.index
    for cmt in main_cnt_df.columns:
        cnt_series = main_cnt_df[cmt]
        unique_cnt_list = cnt_series.unique()
        for cnt in unique_cnt_list:
            part_cnt = cnt_series[cnt_series==cnt]
            start_date = part_cnt.index[0]
            end_date = part_cnt.index[-1]
            tmp_oi_data = w.wset("futureoir","startdate="+start_date+";enddate="+end_date+\
                                 "varity="+cmt+";wind_code="+cnt+";order_by=long;ranks=all;field=date,ranks,"+\
                                 "member_name,long_position,short_position,vol")
            
            tmp_oi_data = pd.DataFrame(tmp_oi_data.Data, index=tmp_oi_data.Fields).T
            
            
    
if __name__ == "__main__":
    main_cnt_df = pd.read_csv("main_cnt.csv",index_col=0)
    OI_Construct(main_cnt_df)

    
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
    
    