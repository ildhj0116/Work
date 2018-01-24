# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 15:39:28 2018

@author: LHYM
"""
import matplotlib.pyplot as plt
import pandas as pd
#不加这个中文标题可能乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def plotCV(filename):
    Contract_Value = pd.read_csv('../output/'+filename, encoding = 'gb2312',index_col = 0)
    fig, axes = plt.subplots(nrows=2, ncols=3)
    fig.set_dpi(100)
    fig.set_figheight(10.8)
    fig.set_figwidth(19.2)
    mtitle = [[u"总合约价值",u"化工合约价值",u"农产品合约价值"],[u"黑色合约价值",u"有色合约价值",u"贵金属合约价值"]]
    cmt = [["total_CV","chem_CV","agri_CV"],["fmt_CV","nfmt_CV","gld_CV"]]
    for r in range(2):
        for c in range(3):
            Contract_Value[cmt[r][c]].plot(ax=axes[r,c],title=mtitle[r][c])
            for tick in axes[r,c].xaxis.get_major_ticks():
                        tick.label.set_fontsize(10) 
    plt.suptitle(u"合约价值（亿元）",fontsize=20)
    plt.savefig("../output/CV.jpg")
