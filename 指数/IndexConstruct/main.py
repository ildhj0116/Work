# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 13:16:28 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
from WindPy import w
from datetime import datetime
import copy

w.start()


base_date = "2004-09-22"
end_date = "2018-03-15"



cmt_list = ['C.DCE','M.DCE']
weight = np.array([0.77,0.23])
rolling_date_list = []
price_list = []
base_list = []
df_list = []

for cmt in cmt_list:
    #持仓量矩阵
    cmt_data = w.wset("futurecc","startdate="+base_date+";enddate="+end_date+";wind_code="+cmt)
    cnt_data = pd.DataFrame(data=cmt_data.Data,index=cmt_data.Fields).T
    effective_cnt = cnt_data[(cnt_data["contract_issue_date"]<datetime.strptime(end_date,"%Y-%m-%d"))\
                             & (cnt_data["last_trade_date"]>datetime.strptime(base_date,"%Y-%m-%d"))]
    effective_cnt.set_index('wind_code',inplace=True)

    cnt_list = ",".join(list(effective_cnt.index))
    oi_data = w.wsd(cnt_list, "oi",base_date,end_date,"")
    oi_data = pd.DataFrame(data=oi_data.Data,index=oi_data.Codes,columns=oi_data.Times).T.fillna(0)
    
    #考虑持仓量相同的情况
    max_count_f = lambda x: x[x==x.max()].count()
    max_oi_count = oi_data.apply(max_count_f,axis=1)
    print "持仓量相等情况个数%d" % len(max_oi_count[max_oi_count>1])
    
    #找最大持仓量合约
    max_oi_cnt_f = lambda x: x.idxmax()
    max_oi_cnt = oi_data.apply(max_oi_cnt_f,axis=1)
    
    main_cnt_code = ','.join(list(max_oi_cnt.unique()))
    
    main_cnt_data =  w.wsd(main_cnt_code, "close",base_date,end_date,"")
    main_cnt_settle = pd.DataFrame(data=main_cnt_data.Data,index=main_cnt_data.Codes,\
                                   columns=main_cnt_data.Times).T.fillna(0)
    df_list.append(main_cnt_settle.iloc[:,0:2])
    main_cnt_weight = pd.DataFrame(0,index=main_cnt_data.Codes,\
                                   columns=main_cnt_data.Times).T.fillna(0)
    date_list = main_cnt_data.Times
    main_cnt_list = list(max_oi_cnt)
    original_cnt = main_cnt_list[0]
    sub_cnt = main_cnt_list[0]
    
    decide_flag = False
    rolling_flag = False
    
    back_cnt_list = []
    rolling_date_to_deliver = {}
    filtered_main_cnt_list = copy.deepcopy(main_cnt_list)
    decide_param = 2 #判断周期
    rolling_param = 5 #展期周期
    for t in range(len(main_cnt_list)):
        if decide_flag==False and rolling_flag==False:
            if main_cnt_list[t]==sub_cnt:
                main_cnt_weight.ix[t,sub_cnt] = 1
                filtered_main_cnt_list[t] = sub_cnt
            else:
                if main_cnt_list[t] in back_cnt_list:
                    main_cnt_weight.ix[t,sub_cnt] = 1
                    filtered_main_cnt_list[t] = sub_cnt
                else:
                    original_cnt = sub_cnt
                    sub_cnt = main_cnt_list[t]
                    decide_flag = True
                    main_cnt_weight.ix[t,original_cnt] = 1
                    filtered_main_cnt_list[t] = original_cnt
                    decide_day = 1
        elif decide_flag==True:
            main_cnt_weight.ix[t,original_cnt] = 1
            filtered_main_cnt_list[t] = original_cnt
            if main_cnt_list[t]==sub_cnt:
                decide_day += 1
                if decide_day>=decide_param:
                    decide_flag = False
                    rolling_flag = True
                    rolling_day = 0
                    rolling_date_to_deliver[original_cnt]=date_list[t]
            elif main_cnt_list[t]==original_cnt:
                decide_flag = False
                sub_cnt = main_cnt_list[t]
            else:
                sub_cnt = main_cnt_list[t]
        elif rolling_flag==True:
            rolling_day += 1
            filtered_main_cnt_list[t] = original_cnt + "+" + sub_cnt
            if rolling_day == rolling_param:
                rolling_flag = False
                back_cnt_list.append(original_cnt)
                main_cnt_weight.ix[t,sub_cnt] = 1
            else:
                main_cnt_weight.ix[t,original_cnt] = (rolling_param - rolling_day)/float(rolling_param)
                main_cnt_weight.ix[t,sub_cnt] = rolling_day/float(rolling_param)
    
    trade_rolling_date_main = effective_cnt.loc[rolling_date_to_deliver.keys(),'last_trade_date'].copy()
    trade_rolling_date_main = pd.concat([trade_rolling_date_main,pd.Series(rolling_date_to_deliver,\
                                        name="rolling_date")],axis=1)
    rolling_date_list.append(trade_rolling_date_main)
    filter_main_cnt = pd.Series(filtered_main_cnt_list,index=max_oi_cnt.index)
    main_cnt = pd.DataFrame([max_oi_cnt,filter_main_cnt]).T
    main_cnt.columns = ["original","filtered"]
    weighted_cmt_price = np.diag(np.dot(main_cnt_settle, main_cnt_weight.T))
    weighted_base_price = np.diag(np.dot(main_cnt_settle.iloc[:-1,:], main_cnt_weight.iloc[1:,:].T))
    price_list.append(pd.Series(weighted_cmt_price,index=main_cnt.index))
    base_list.append(pd.Series(weighted_base_price,index=main_cnt.index[1:]))

# 展期日期偏移计算
trade_rolling_date_main = pd.concat(rolling_date_list)


#    
cmt_price = pd.DataFrame(price_list).T
base_price = pd.DataFrame(base_list).T
cmt_price.columns = cmt_list 
base_price.columns = cmt_list    
weighted_price = np.dot(cmt_price,weight.T)
weighted_base = np.dot(base_price,weight.T)
date_num = len(cmt_price.index)
index = np.zeros(date_num)
index[0] = 1000
for i in range(1,date_num):
    index[i] = weighted_price[i]/weighted_base[i-1]*index[i-1]
index_price = pd.Series(index,index=cmt_price.index,name="index")


feedcost_weekly = w.wsd("S5063761", "close",base_date,end_date,"")
feedcost_weekly = pd.Series(feedcost_weekly.Data[0],index=feedcost_weekly.Times,name=feedcost_weekly.Codes[0])
feedcost_monthly = w.wsd("M5464273", "close",base_date,end_date,"")
feedcost_monthly = pd.Series(feedcost_monthly.Data[0],index=feedcost_monthly.Times,name=feedcost_monthly.Codes[0])

    
index_with_cmt = pd.concat([index_price,cmt_price],axis=1)
index_with_feedcost_weekly = pd.concat([feedcost_weekly,index_price],axis=1).dropna()
index_with_feedcost_monthly = pd.concat([feedcost_monthly,index_price],axis=1).dropna()
    
index_price.to_csv('output\index_close.csv')    
index_with_cmt.to_csv('output\index_with_cmt.csv')    
index_with_feedcost_weekly.to_csv('output\index_with_feedcost_weekly.csv')   
index_with_feedcost_monthly.to_csv('output\index_with_feedcost_monthly.csv')












    