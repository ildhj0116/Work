# encoding: UTF-8
'''
编制猪饲料成本指数
作者:王文科 当前版本v1.0 日期 20180117
'''
import os 
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="white")
from datetime import date
import pandas as pd 
import numpy as np
from WindPy import w 
w.start()

class feedcost_index:
    def __init__(self):
        #指数成分: 玉米&豆粕
        self.c=['C01M.DCE','C05M.DCE','C09M.DCE']
        self.m=['M01M.DCE','M05M.DCE','M09M.DCE']
        #权重比例
        self.wt=0.68/0.88
        #展期判断期
        self.x=2
        #展期移仓天数
        self.p=5
        #指数基期和基点
        self.index_begin='2016-01-01'
        self.base=1000
        #数据回溯周期
        self.start='2016-01-01'
        self.end='2017-12-29'


    def oi_bar(self,cnt):
        '''获取合约持仓数据'''
        wdat=w.wsd(cnt,'oi',self.start,self.end)
        data=np.array(wdat.Data).T
        df=pd.DataFrame(data,index=wdat.Times,columns=[i[1:-5] for i in wdat.Codes])
        df['mm']=map(lambda x,y,z:'eq' if (x==y or x==z or y==z) else '0'+str([x,y,z].index(max([x,y,z]))*4+1),df['01'],df['05'],df['09'])
        return df 






if __name__ == "__main__":
    cls=feedcost_index()
    df=cls.oi_bar(cls.c)
    df.to_csv('test.csv')