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
    

def plotCV_all(cv):
    cv_today = cv.iloc[-1,:]
    cv_today.sort_values(ascending=False,inplace=True)
    #画图
    fig = plt.figure()
    axis = fig.add_subplot(111)
    cv_today.plot.bar(ax=axis,color=[tuple(color_setting(cv_today))])
    axis.axhline(0, color='k')
