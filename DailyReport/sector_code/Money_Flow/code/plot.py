# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

import numpy as np
import matplotlib.pyplot as plt

def PlotMoneyFlow(data,date):    
    fig_num = 3
    fig_xlabel = [u'总资金流量',u'主动资金流量',u'被动资金流量']
    fig_title = [u'期货资金流向图(单位：亿元)',u'期货资金主动流入(单位：亿元)',u'期货资金被动流入(单位：亿元)']
    fig_list = []
    for i in range(fig_num):
        data = data.sort_values(by=data.columns[fig_num - i], ascending=False)
        data = data.dropna()
    
        fig = plt.figure(figsize=(19.2,10.8), dpi=100,edgecolor=None)
        axis = fig.add_subplot(111)
        bar_width = 0.5
        index = np.arange(len(data))
        
        rects = axis.barh(index, data[data.columns[fig_num - i]], bar_width) 
        for rect in rects:
            #height = rect.get_height()
            width = rect.get_width()
            #x = rect.get_x()
            y = rect.get_y()
            if width < 0:
                plt.text(width*1.1 - 0.2  , y-0.1, width, ha = 'center', va = 'bottom',fontsize=15)
                rect.set_color('grey')
            else:
                plt.text(width*1.1 + 0.2 , y-0.1, width, ha = 'center', va = 'bottom',fontsize=15)
                rect.set_color('red')
        	# print rect.get_x() > 0
        
        plt.yticks(index, data['commodity_name'],fontsize=15)
        plt.xticks(fontsize=15)
        plt.xlabel(fig_xlabel[i],fontsize=15)
        plt.ylabel(u'合约品种',fontsize=15)
        plt.title(date+fig_title[i],fontsize=20)
        x_max = max(abs(data[data.columns[fig_num - i]].iloc[-1]),abs(data[data.columns[fig_num - i]].iloc[0]))
        plt.xlim(-x_max*1.4, x_max*1.4)
        plt.ylim(index[0]-bar_width/1.5,index[-1]+bar_width/1.5)
        axis.grid(linestyle='--', axis='y', zorder=0)
        fig_list.append(fig)
    return fig_list