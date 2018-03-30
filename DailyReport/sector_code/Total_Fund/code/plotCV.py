# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 15:39:28 2018

@author: LHYM
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import pandas as pd

#不加这个中文标题可能乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def color_setting(ret):
    colors = ['r' if x>0 else 'g' for x in ret]
    return colors

def plotCV_sector(Contract_Value):
    fig,axes = plt.subplots(nrows=2, ncols=3)
    fig.set_dpi(100)
    fig.set_figheight(10.8)
    fig.set_figwidth(19.2)
    mtitle = [[u"总沉淀资金",u"化工沉淀资金",u"农产品沉淀资金"],[u"黑色沉淀资金",u"有色沉淀资金",u"贵金属沉淀资金"]]
    cmt = [["total_CV","chem_CV","agri_CV"],["fmt_CV","nfmt_CV","gld_CV"]]
    for r in range(2):
        for c in range(3):
            Contract_Value[cmt[r][c]].plot(ax=axes[r,c],title=mtitle[r][c])
            for tick in axes[r,c].xaxis.get_major_ticks():
                tick.label.set_fontsize(10)
                tick.label.set_rotation(15)
            #axes[r,c].xaxis.set_major_formatter(mdate.DateFormatter('%y-%m-%d %H:%M:%S'))
            #plt.xticks(rotation=90)
    plt.suptitle(u"沉淀资金（亿元）",fontsize=20)
    return fig

def plotCV_sector_one_graph(Contract_Value):
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    axis2 = axis.twinx()
    Contract_Value["total_CV"].plot(ax=axis2,label=u"总沉淀资金",linewidth=3,color=['black'])
    Contract_Value["chem_CV"].plot(ax=axis,label=u"化工沉淀资金",color=['orange'])
    Contract_Value["agri_CV"].plot(ax=axis,label=u"农产品沉淀资金",color=['green'])
    Contract_Value["fmt_CV"].plot(ax=axis,label=u"黑色沉淀资金",color=['purple'])
    Contract_Value["nfmt_CV"].plot(ax=axis,label=u"有色沉淀资金",color=['blue'])
    Contract_Value["gld_CV"].plot(ax=axis,label=u"贵金属沉淀资金",color=['red'])
    lines, labels = axis.get_legend_handles_labels()
    lines2, labels2 = axis2.get_legend_handles_labels()
    axis2.legend(lines + lines2, labels + labels2)
    plt.xticks(rotation=0)
    axis.grid(which="both",linestyle='--')
    plt.xlabel(u"品种",fontsize=15)
    axis.set_ylabel(u"各版块沉淀资金(亿元)",fontsize=15)
    axis2.set_ylabel(u"总沉淀资金(亿元)",fontsize=15)
    plt.title(u"沉淀资金",fontsize=20)

    return fig

def plotCV_all(cv):
    cv_today = cv.iloc[-1,:]
    cv_today.sort_values(ascending=False,inplace=True)
    #画图
    fig = plt.figure(figsize=(19.2,10.8), dpi=100)
    axis = fig.add_subplot(111)
    cv_today.plot.bar(ax=axis,color=[tuple(color_setting(cv_today))])
    plt.xticks(rotation=0)
    axis.grid(axis='y',which="both",linestyle='--')
    axis.axhline(0, color='k')
    plt.xlabel(u"品种",fontsize=15)
    plt.ylabel(u"沉淀资金(亿元)",fontsize=15)
    plt.title(u"品种沉淀资金",fontsize=20)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=15)
    return fig