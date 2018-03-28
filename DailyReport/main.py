# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 14:05:04 2018

@author: Administrator
"""
import sys
sys.path.append("./sector_code/Strength")
sys.path.append("./sector_code/Volatility")
sys.path.append("./sector_code/OI_Vol")
sys.path.append("./sector_code/Money_Flow/code")
sys.path.append("./sector_code/Total_Fund/code")
import os
from NanHua import NanHua
from cmt_ret import cmt_ret_rank
from volatility import amplitude
from oi_indicator import vol_oi_indicator
from fund_main import fund_main
from money_flow_main import money_flow_main

from WindPy import w
import pandas as pd
from datetime import datetime
w.start()



if __name__ == "__main__":
    
    cmt_list = pd.read_csv("../Futures_Data/cmt_list/cmt_daily_list.csv").loc[:,"cmt"].tolist()
    main_cnt_df = pd.read_csv("../Futures_Data/main_cnt/data/main_cnt_total.csv",parse_dates=[0],index_col=0)
    report_date = "2018-03-28"
    relative_data_path = "../Futures_Data"
    
    #判断数据更新情况
    report_date_time = datetime.strptime(report_date,"%Y-%m-%d")
    try:
        main_cnt_list_today = main_cnt_df.loc[report_date_time,:].copy()
    except:
        print "主力合约列表无更新日期数据，不能进行计算"
    else:
        del main_cnt_df
        # 1、品种强弱
        #   (1)半年内南华商品指数价格折线图
        #   (2)半年内南华商品指数收益率折线图
        start_date_NanHua = "2017-09-24"
        NanHua(start_date_NanHua,report_date)
        #   (3)各品种日、月、周收益率排名
        cmt_ret_rank(main_cnt_list_today,cmt_list,relative_data_path)
        #   (4)新高新低
        
        # 2、波动率提示：品种日振幅
        amplitude(main_cnt_list_today,cmt_list,report_date)
        # 3、持仓、成交提示
        vol_oi_indicator(main_cnt_list_today,cmt_list,report_date,relative_data_path)
        # 4、资金提示
        #   (1)沉淀资金
        start_date_fund = "2017-09-01"
        fund_main(start_date_fund,report_date)
        #   (2)资金流向
        top_N = 2
        money_flow_main(report_date,top_N)
        
        #输出
        if os.path.exists("output/" + report_date):
            print report_date + "已更新过，文件夹重复"
        else:
            os.makedirs("output/" + report_date)
        
        
        
        
        
        
