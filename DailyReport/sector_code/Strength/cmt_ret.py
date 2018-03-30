# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 10:17:19 2018

@author: Administrator
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def color_setting(ret):
    colors = ['r' if x>0 else 'g' for x in ret]
    return colors
    

def cmt_ret_rank(main_cnt_list_today,cmt_list,relative_data_path):
    cl_series_list = []
    fig_list = []
    for cmt in cmt_list.index.tolist():
        tmp_cl = pd.read_csv(relative_data_path + "/data_cl/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0) #相对地址有问题
        main_cnt = main_cnt_list_today.loc[cmt]
        main_cnt_cl = tmp_cl[main_cnt].dropna().copy()
        main_cnt_cl.name = cmt
        del tmp_cl
        cl_series_list.append(main_cnt_cl)
    cl_df = pd.concat(cl_series_list,axis=1)
    ret_d = ((cl_df - cl_df.shift(1)) / cl_df.shift(1)).iloc[-1,:]
    ret_d.name = "daily_ret"
    ret_d.index = cmt_list.loc[ret_d.index.tolist(),:]["Chinese"].tolist()
    ret_w = ((cl_df - cl_df.shift(5)) / cl_df.shift(5)).iloc[-1,:]
    ret_w.name = "weekly_ret"
    ret_w.index = cmt_list.loc[ret_w.index.tolist(),:]["Chinese"].tolist()
    ret_m = ((cl_df - cl_df.shift(20)) / cl_df.shift(20)).iloc[-1,:]
    ret_m.name = "monthly_ret"
    ret_m.index = cmt_list.loc[ret_m.index.tolist(),:]["Chinese"].tolist()
    ret_d.sort_values(ascending=False,inplace=True)
    ret_w.sort_values(ascending=False,inplace=True)
    ret_m.sort_values(ascending=False,inplace=True)
    
    #画图
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    ret_d.plot.bar(ax=axis,color=[tuple(color_setting(ret_d))])
    plt.xticks(rotation=0)
    axis.grid(which="both",linestyle='--')
    axis.axhline(0, color='k')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"主力合约收益率",fontsize=15)
    plt.title(u"主力合约收益率（1日）",fontsize=20)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    fig_list.append(fig)
    
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    ret_w.plot.bar(ax=axis,color=[tuple(color_setting(ret_w))])
    plt.xticks(rotation=0)
    axis.grid(which="both",linestyle='--')
    axis.axhline(0, color='k')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"主力合约收益率",fontsize=15)
    plt.title(u"主力合约收益率（1周）",fontsize=20)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    fig_list.append(fig)
   
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    ret_m.plot.bar(ax=axis,color=[tuple(color_setting(ret_m))])
    plt.xticks(rotation=0)
    axis.grid(which="both",linestyle='--')
    axis.axhline(0, color='k')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"主力合约收益率",fontsize=15)
    plt.title(u"主力合约收益率（1月）",fontsize=20)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    fig_list.append(fig)
    
    return fig_list


if __name__ == "__main__":
    a = 0
    
    
    