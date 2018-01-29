# encoding: UTF-8

'''
该程序用于实时提示均线趋势策略信号 当前版本v1.0

运行前，配置testday参数, testday表示交易日日期

夜盘时testday需更新为第二天的日期

作者:王文科 当前版本v1.0 日期 20171021
'''
import pickle 
import sys
import pandas as pd 
from PyQt4 import QtGui
import datetime as dt 
ti=dt.datetime.now()
print ti.minute

f=file('holdlist.pkl','rb')
pos=pickle.load(f) 
long_hold=pos['long']
short_hold=pos['short']
f.close()

long_hold.remove('RB_01')
#long_hold.remove('RB_01')
long_hold.append('FG_01')
long_hold.append('JM_01')
long_hold.append('I_01')
long_hold.append('ZN_01')
long_hold.append('AU_1')
long_hold.append('JM_01')
long_hold.append('TA_01')
short_hold.remove('FG_01')
short_hold.remove('JM_01')
short_hold.remove('ZN_01')
short_hold.remove('HC_01')
short_hold.remove('AU_01')
short_hold.remove('I_01')
short_hold.remove('TA_01')
pos2={'long':long_hold,'short':short_hold}
f1 = file('holdlist.pkl','wb')  
pickle.dump(pos2, f1, True)  
f1.close() 
'''
from WindPy import w 
w.start()
dailyinformationcd='info.csv'
df=pd.read_csv(dailyinformationcd,index_col=0)
for index, row in df.iterrows():
    d=w.wsd(index, "mfprice", "2017-12-25", "2017-12-25")
    print index,d.Data[0][0]
'''

