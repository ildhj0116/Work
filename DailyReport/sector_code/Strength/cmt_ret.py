# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 10:17:19 2018

@author: Administrator
"""
import pandas as pd
import matplotlib.pyplot as plt

def color_setting(ret):
    colors = ['r' if x>0 else 'g' for x in ret]
    return colors
    

def cmt_ret_rank(main_cnt_list_today,cmt_list,relative_data_path):
    cl_series_list = []
    for cmt in cmt_list:
        tmp_cl = pd.read_csv(relative_data_path + "/data_cl/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0) #相对地址有问题
        main_cnt = main_cnt_list_today.loc[cmt]
        main_cnt_cl = tmp_cl[main_cnt].dropna().copy()
        main_cnt_cl.name = cmt
        del tmp_cl
        cl_series_list.append(main_cnt_cl)
    cl_df = pd.concat(cl_series_list,axis=1)
    ret_d = ((cl_df - cl_df.shift(1)) / cl_df.shift(1)).iloc[-1,:]
    ret_d.name = "daily_ret"
    ret_w = ((cl_df - cl_df.shift(5)) / cl_df.shift(5)).iloc[-1,:]
    ret_w.name = "weekly_ret"
    ret_m = ((cl_df - cl_df.shift(20)) / cl_df.shift(20)).iloc[-1,:]
    ret_m.name = "monthly_ret"
    ret_d.sort_values(ascending=False,inplace=True)
    ret_w.sort_values(ascending=False,inplace=True)
    ret_m.sort_values(ascending=False,inplace=True)
    
    #画图
    fig = plt.figure()
    axis = fig.add_subplot(111)
    ret_d.plot.bar(ax=axis,color=[tuple(color_setting(ret_d))])
    axis.axhline(0, color='k')
    fig = plt.figure()
    axis = fig.add_subplot(111)
    ret_w.plot.bar(ax=axis,color=[tuple(color_setting(ret_w))])
    axis.axhline(0, color='k')
    fig = plt.figure()
    axis = fig.add_subplot(111)
    ret_m.plot.bar(ax=axis,color=[tuple(color_setting(ret_m))])
    axis.axhline(0, color='k')
    

if __name__ == "__main__":
    a = 0
    
    
    