# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:53:27 2018

@author: Administrator
"""

from WindPy import w
from datetime import datetime, timedelta
import pandas as pd
w.start()

def trade_date_update(today):
    trade_date_list = pd.read_csv("../others/trade_date.csv",index_col=0).index.tolist()
    trade_date_list = [datetime.strptime(x, "%Y-%m-%d") for x in trade_date_list]
    start_date = trade_date_list[-1] + timedelta(days=1)
    end_date = datetime.strptime(today,"%Y-%m-%d")
    if start_date > end_date:
        print "日期更新错误，无法更新日期列表"
    else:
        update_date_list = w.tdays(start_date, end_date, "")
        update_date_list = [x.date() for x in update_date_list.Data[0]]
        trade_date_list.extend(update_date_list)
        trade_date_list = [x.strftime("%Y-%m-%d") for x in trade_date_list]
        trade_date_df = pd.Series(index=trade_date_list)
        trade_date_df.to_csv("../others/trade_date.csv")
        print "交易日列表更新完毕"
#        trade_date
if __name__ == "__main__":
    today = "2018-04-20"
    trade_date_update(today)