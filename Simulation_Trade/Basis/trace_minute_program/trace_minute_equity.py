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
margin_rate = 0.15



today_trade["Contract"] = [Add_Exchange_For_Cnt(x) for x in today_trade["Contract"]]
trade_cnt_list = today_trade["Contract"].tolist()
trade_cnt_list_str = ",".join(trade_cnt_list)
trade_cnt_data = w.wss(trade_cnt_list_str, "contractmultiplier")
trade_cnt_data = pd.Series(trade_cnt_data.Data[0],name=trade_cnt_data.Fields[0])
today_trade["multiplier"] = trade_cnt_data
today_trade["margin"] = today_trade["Position"] * today_trade["Price"] * today_trade["multiplier"] * margin_rate
today_trade["margin"] = today_trade["margin"]


usable_equity = original_equity
last_position = pd.read_excel("Current_Position.xlsx")
current_position = last_position.copy()
if len(today_trade)!=0:
    for i in range(len(today_trade)):
        entry_trade = today_trade.iloc[i]
        cnt_name = entry_trade["Contract"]
        if  cnt_name in current_position["Contract"]:
            entry_current = current_position.loc[current_position["Contract"]==cnt_name]
            #开仓
            if entry_trade["Position"] * entry_current["Position"] > 0:
                delta_equity = -abs(entry_trade["margin"])
                entry_current["Price"] = (entry_current["Price"]*entry_current["Position"] + entry_trade["Price"] * entry_current["Position"]) \
                                            /(entry_current["Position"] + entry_current["Position"])
                entry_current["Margin"] += entry_trade["margin"]
            #平仓
            else:
                delta_equity = (entry_trade["Position"] * (entry_trade["Price"] - entry_current["Price"]) * entry_trade["multiplier"] + \
                                abs(entry_trade["Position"] * entry_current["Price"]) * entry_trade["multiplier"]) * margin_rate
                entry_current["Margin"] -= abs(entry_trade["Position"] * entry_current["Price"] * entry_trade["multiplier"]) * margin_rate
            entry_current["Position"] = entry_current["Position"] + entry_trade["Position"]
            if entry_current["Position"] == 0:
                current_position = current_position[(True-(current_position["Contract"]==cnt_name))].copy()
        else:
            len_current = len(current_position)
            current_position.loc[len_current,"Contract"] = cnt_name
            current_position.loc[len_current,"Position"] = entry_trade["Position"]
            current_position.loc[len_current,"Price"] = entry_trade["Price"]
            current_position.loc[len_current,"Margin"] = entry_trade["margin"]
            delta_equity = -abs(entry_trade["margin"])
        usable_equity += delta_equity
        
                
                                

current_position.set_index("Contract",inplace=True)
#设置多空合约以及手数、乘数
cnt_list = current_position.index.tolist()
cnt_list_str = ",".join(cnt_list)
cnt_list = cnt_list_str.split(',')
#long_list = "ZC805.CZC,C1805.DCE,RU1805.SHF,TA805.CZC,CU1804.SHF".split(",")
#short_list = "P1805.DCE,I1805.DCE,RB1805.SHF,J1805.DCE,JM1805.DCE".split(",")
#cnt_size = [31,55,4,69,8,-47,-22,-31,-5,-14]
cnt_multiplier = w.wss(cnt_list_str, "contractmultiplier")
cnt_multiplier = pd.Series(cnt_multiplier.Data[0],index=cnt_multiplier.Codes,name=cnt_multiplier.Fields[0]).T
if "CONTRACTMULTIPLIER" in current_position.columns:
    current_position.drop("CONTRACTMULTIPLIER",inplace=True)
current_position = pd.concat([current_position,cnt_multiplier],axis=1)


#设置起止时间

start_time = "2018-02-26 9:00:00"
end_time = "2018-02-27 8:59:00"

#提取分钟数据
minute_data = w.wsi(cnt_list_str, "close", start_time, end_time, "")
minute_data = pd.DataFrame(minute_data.Data,index=minute_data.Fields).T
minute_data["windcode"] = minute_data["windcode"].apply(str)
minute_data.set_index(["time","windcode"],inplace=True)
minute_data = minute_data.unstack()
minute_data.columns = minute_data.columns.levels[1]
minute_data = minute_data.reindex(columns=current_position.index)

#处理nan:全部无值的时间跳过；有的合约有值时，无值的合约使用前值作为其最新报价
minute_data.dropna(how="all",inplace=True)
minute_data.fillna(method="ffill",inplace=True)
 
#计算合约价值
minute_value = minute_data * current_position["Position"] * current_position["CONTRACTMULTIPLIER"]
float_pnl = minute_value - current_position["Margin"]/0.15
total_pnl = float_pnl.sum(axis=1)
usable_equity_series = pd.Series(usable_equity,index=total_pnl.index)
total_margin = current_position["Margin"].abs().sum()
equity = usable_equity + total_pnl + total_margin

"""
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