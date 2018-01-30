# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 10:09:16 2018

@author: 李弘一萌
"""
from WindPy import w
w.start()
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime 

#不加这个中文标题可能乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


#设置多空合约以及手数、乘数
cnt_list_str = "MA805.CZC,CS1805.DCE,ZC805.CZC,TA805.CZC,RU1805.SHF,J1805.DCE,RB1805.SHF,Y1805.DCE,BU1806.SHF,JM1805.DCE"
cnt_list = cnt_list_str.split(',')
long_list = "MA805.CZC,CS1805.DCE,ZC805.CZC,TA805.CZC,RU1805.SHF".split(",")
short_list = "J1805.DCE,RB1805.SHF,Y1805.DCE,BU1806.SHF,JM1805.DCE".split(",")
cnt_size = [13,18,6,13,3,-2,-9,-6,-13,-5]
cnt_data = w.wss(cnt_list_str, "contractmultiplier")
cnt_data = pd.DataFrame(cnt_data.Data,columns=cnt_data.Codes,index=cnt_data.Fields).T
cnt_data["size"] = cnt_size


#设置起止时间
start_time = "2018-01-30 9:00:00"
end_time = "2018-01-30 15:01:00"

#提取分钟数据
minute_data = w.wsi(cnt_list_str, "close", start_time, end_time, "")
minute_data = pd.DataFrame(minute_data.Data,index=minute_data.Fields).T
minute_data["windcode"] = minute_data["windcode"].apply(str)
minute_data.set_index(["time","windcode"],inplace=True)
minute_data = minute_data.unstack()
minute_data.columns = minute_data.columns.levels[1]
#处理nan:全部无值的时间跳过；有的合约有值时，无值的合约使用前值作为其最新报价
minute_data.dropna(how="all",inplace=True)
minute_data.fillna(method="ffill",inplace=True) 
#计算合约价值
minute_value = minute_data*cnt_data["size"]*cnt_data["CONTRACTMULTIPLIER"]
minute_value["long_value"] = minute_value.loc[:,long_list].sum(axis=1)
minute_value["short_value"] = minute_value.loc[:,short_list].sum(axis=1)
minute_value["ratio"] = minute_value["long_value"]/(-minute_value["short_value"])
minute_value["diff"] = minute_value["long_value"]+minute_value["short_value"]



###############################################################################
#画图
fig = plt.figure(1)
ax1=fig.add_subplot(1,1,1)
#minute_value["ratio"].plot(ax=ax1,title=u"多头总合约价值/空头总合约价值("+datetime.now().date().strftime("%Y-%m-%d")+")")
x = minute_value.index
#将DatetimeIndex转为字符串
x = x.to_pydatetime()
x = np.vectorize(lambda s: s.strftime('%m-%d %H:%M'))(x)
y = minute_value["ratio"].tolist()
#设置横坐标显示
xticks = range(0,len(x),10)
xlabels = [x[index] for index in xticks]
xticks.append(len(x))
xlabels.append(x[-1])
ax1.set_xticks(xticks)
ax1.set_xticklabels(xlabels,rotation=30)
ax1.set_xlim(xticks[0],xticks[-1])
ax1.set_title(u"多头总合约价值/空头总合约价值("+datetime.now().date().strftime("%Y-%m-%d")+")",fontsize=20)
ax1.plot(x,y)
fig.set_dpi(100)
fig.set_figheight(10.8)
fig.set_figwidth(19.2)
plt.savefig("ratio.jpg")
#from matplotlib.dates import DateFormatter  
#yearsFmt = DateFormatter('%m-%d %H:%M')  
#fig.autofmt_xdate()        #设置x轴时间外观  
#ax1.xaxis.set_major_formatter(yearsFmt)      #设置时间显示格式


