# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 13:44:01 2018

@author: Administrator
"""

import pandas as pd
from datetime import datetime,timedelta
from all_cnt_update import quotes_data_update
from Main_Contract_Update import main_cnt_update
from position_rank_download import position_rank_update
from trade_date_update import trade_date_update
from cnt_list_update import cnt_list_download

if __name__ == "__main__":
    trade_date_list = pd.read_csv("../others/trade_date.csv",index_col=0,parse_dates=[0]).index.tolist()
    today = datetime.today()
    if today.hour < 15:
        today -= timedelta(days=1)
    #若今天的日期小于等于已存在的日期，则一定是日期出现问题或不需要更新
    if today <= trade_date_list[-1]:
        print "更新日期错误"
    else:
        today_str = today.strftime("%Y-%m-%d")        
        trade_date_update(today_str)
        cnt_list_download(today_str)
        quotes_data_update(today_str)
        main_cnt_update(today)
        position_rank_update(today_str,today_str)

    
