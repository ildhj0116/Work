# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 10:13:42 2018

@author: Administrator
"""

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
import operator
from datetime import datetime
 
#不加这个中文标题可能乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


commodities={
'DCE':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I'],
'CZC':['CF','SR','RM','TA','FG','MA','ZC'],
'SHF':['CU','ZN','AL','NI','AU','AG','BU','RU','HC','RB'],
'CFE':['IC','IH','IF','T','TF'],
'ALL':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I',
       'CF','SR','RM','TA','FG','MA','ZC','CU','ZN','AL',
       'NI','AU','AG','BU','RU','HC','RB','IC','IH','IF','T','TF']}


def Add_Exchange_For_Cnt(cnt):
    cmt = [x for x in cnt if not x.isdigit()]
    cmt = "".join(cmt)
    if cmt in commodities['DCE']:
        return cnt+'.DCE'
    elif cmt in commodities['CZC']:
        return cnt+'.CZC'
    elif cmt in commodities['SHF']:
        return cnt+'.SHF'
    else:
        return cnt+'.CFE'
        
class Trade:
    def __init__(self,contract,price,position,time_stamp):
        self.contract = contract
        self.price = price
        self.position = position
        self.time_stamp = time_stamp

today_trade = pd.read_excel("Trade.xlsx")
    
#cmpfunc = operator.attrgetter("time_stamp")
    
#original_equity = 5499499 + (9400+4200-11910-9550-9170-12100+3400-6050+1620-3400)

original_equity = 5465939

today_trade["Contract"] = [Add_Exchange_For_Cnt(x) for x in today_trade["Contract"]]
trade_cnt_list = today_trade["Contract"].tolist()
trade_cnt_list_str = ",".join(trade_cnt_list)
trade_cnt_data = w.wss(trade_cnt_list_str, "contractmultiplier")
trade_cnt_data = pd.Series(trade_cnt_data.Data[0],name=trade_cnt_data.Fields[0])
today_trade["multiplier"] = trade_cnt_data
today_trade["margin"] = today_trade["Position"] * today_trade["Price"] * today_trade["multiplier"] * 0.15
usable_equity = original_equity - today_trade["margin"].abs().sum()

current_position = pd.read_excel("Current_Position.xlsx")
#if len(today_trade)!=0:
#    for i in range(len):
#        cnt_name = today_trade["Contract"].iloc[i]
#        if  cnt_name in current_position["Contract"]:
#            if today_trade["Position"].loc * current_position[]

"""
#设置多空合约以及手数、乘数
cnt_list_str = "ZC805.CZC,C1805.DCE,RU1805.SHF,TA805.CZC,CU1804.SHF,P1805.DCE,I1805.DCE,RB1805.SHF,J1805.DCE,JM1805.DCE"
cnt_list = cnt_list_str.split(',')
long_list = "ZC805.CZC,C1805.DCE,RU1805.SHF,TA805.CZC,CU1804.SHF".split(",")
short_list = "P1805.DCE,I1805.DCE,RB1805.SHF,J1805.DCE,JM1805.DCE".split(",")
cnt_size = [31,55,4,69,8,-47,-22,-31,-5,-14]
cnt_data = w.wss(cnt_list_str, "contractmultiplier")
cnt_data = pd.DataFrame(cnt_data.Data,columns=cnt_data.Codes,index=cnt_data.Fields).T
cnt_data["size"] = cnt_size


#设置起止时间

start_time = "2018-02-12 14:59:00"
end_time = "2018-02-13 8:00:00"

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


#导入前数据
ratio = pd.read_csv("ratio.csv",index_col=0,names=["time","ratio"])
ratio.dropna(inplace=True)
ratio_TimeStamp = [datetime.strptime(str(x),"%Y-%m-%d %H:%M:%S") for x in ratio.index]
ratio_TimeStamp = [np.datetime64(x) for x in ratio_TimeStamp]
ratio.index = ratio_TimeStamp
intersection = ratio.index.intersection(minute_value.index)
new_ratio = minute_value["ratio"].drop(intersection)
all_ratio = pd.concat([ratio["ratio"],new_ratio])
all_ratio.to_csv("ratio.csv")


###############################################################################
#画图
fig = plt.figure(1)
ax1=fig.add_subplot(1,1,1)
#minute_value["ratio"].plot(ax=ax1,title=u"多头总合约价值/空头总合约价值("+datetime.now().date().strftime("%Y-%m-%d")+")")
x = all_ratio.index
#将DatetimeIndex转为字符串
x = x.to_pydatetime()
x = np.vectorize(lambda s: s.strftime('%m-%d %H:%M'))(x)
y = all_ratio.tolist()
#设置横坐标显示和标题
xticks = range(0,len(x),100)
xlabels = [x[index] for index in xticks]
xticks.append(len(x))
xlabels.append(x[-1])
ax1.set_xticks(xticks)
ax1.set_xticklabels(xlabels,rotation=30)
ax1.set_xlim(xticks[0],xticks[-1])
ax1.set_title(u"基差持仓多头总合约价值/空头总合约价值",fontsize=20)
#画图，设置图片大小及分辨率、保存
ax1.plot(x,y)
fig.set_dpi(100)
fig.set_figheight(10.8)
fig.set_figwidth(19.2)
plt.savefig("ratio.jpg")

"""