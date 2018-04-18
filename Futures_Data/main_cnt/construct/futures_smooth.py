# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 10:35:30 2018

@author: Administrator
"""

import pandas as pd
import numpy as np




if __name__ == "__main__":
    main_cnt_df = pd.read_csv("../data/main_cnt_total.csv",parse_dates=[0],index_col=0)
#    cmt_list = ["IC.CFE"]
    cmt_list = main_cnt_df.columns.tolist()
    smoothed_series = []
    for cmt in cmt_list:
        cnt_df = pd.read_csv("../../data_cl/" + cmt[:-4]+".csv",parse_dates=[0],index_col=0)
        main_cnt_series = main_cnt_df[cmt].dropna()
        cnt_ret_df = cnt_df.pct_change()
        main_ret_series = pd.Series(np.zeros(len(main_cnt_series)),index=main_cnt_series.index)
        for date in main_cnt_series.index:
            main_ret_series.loc[date] = cnt_ret_df.loc[date,main_cnt_series.loc[date]]
        main_ret_series += 1
        main_ret_series.iloc[0] = cnt_df.loc[main_ret_series.index[0],main_cnt_series.iloc[0]]
        main_price = main_ret_series.cumprod()
        main_price.name = cmt
        smoothed_series.append(main_price)
    smoothed_df = pd.concat(smoothed_series,axis=1)
#    smoothed_df.dropna(inplace=True)
    smoothed_df.to_csv("../data/smoothed_main_cnt_cl.csv")