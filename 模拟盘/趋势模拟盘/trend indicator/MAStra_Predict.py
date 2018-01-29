# encoding: UTF-8
'''
该程序用于预测未来进入均线系统信号的相应价格
暂时不考虑分钟线指标
运行前, 配置ytd参数, ytd表示今日交易日
运行时间: 收盘后
作者:王文科 当前版本v1.0 日期 20171225
'''
from prettytable import PrettyTable 
import datetime as dt 
import os 
from datetime import date
import pandas as pd 
import numpy as np
from WindPy import w 
w.start()

#工具函数
indexcode={'000905.SH':'IC','000016.SH':'IH','000300.SH':'IF','T.CFE':'T','TF.CFE':'TF'}
def cnt_to_cmt(cnt):
    if cnt in indexcode.keys():
        cmt=indexcode[cnt]
    else:
        if cnt[1].isdigit():
            cmt=cnt[0]
        else:
            cmt=cnt[:2]
    return cmt

#主类
class Predict:
    def __init__(self,ytd):
        #时间参数
        self.start='2017-01-01'
        self.ytd=ytd
        #外部数据表
        self.ma_paras_table=pd.read_csv('parmt.csv',index_col=0) #品种的均线参数
        self.ytd_trend=pd.read_csv(os.path.join('dataV1.2\\','{}.csv'.format(ytd)),index_col=0) #本交易日的趋势信息
        self.dailyinfo=pd.read_csv('dailyinfo.csv',index_col=0)  #获得活跃合约
        self.cmdt_table=pd.read_csv('cmdt_info.csv',index_col=0) #获得最小变动价位
        #其他参数
        self.min_tick=5
    
    def daily_bar(self,cnt):
        w_data=w.wsd(cnt,'close',self.start,self.ytd) 
        data=np.array(w_data.Data).T
        fields=list(map(lambda x:x.lower(),w_data.Fields))
        df=pd.DataFrame(data,index=w_data.Times,columns=fields)
        df.dropna(inplace=True)
        return df 
    
    def simulate_bar(self,d_bar,price):
        nextday=[pd.to_datetime(self.ytd).date()+dt.timedelta(days=1),pd.to_datetime(self.ytd).date()+dt.timedelta(days=2)]
        nextdata=pd.DataFrame([price,price],index=nextday,columns=d_bar.columns)
        df=d_bar.append(nextdata)
        ma=[5,10,20,30,60,120]
        for wk in ma:
            df['DM'+str(wk)]=df['close'].rolling(wk).mean()
        df.dropna(inplace=True)
        return df 
    
    def ind_trend(self,cnt,d_bar,price):
        '''特定价格下的趋势判断'''
        cmt=cnt_to_cmt(cnt)
        bar=self.simulate_bar(d_bar,price)
        try:
            #读取各品种的均线参数
            ma_para=list(self.ma_paras_table.loc[cmt])
            ma_syb=['DM'+str(i) for i in ma_para]
        except:
            #默认值
            ma_para=[5,10,60]
            ma_syb=['DM'+str(i) for i in ma_para]
            print cmt+' uses general MA Parasmeters'
    
        dm=bar.iloc[-1]

        # 均线判定准则 
        [mas,mam,mal]=ma_syb
        tmp='null'
        if dm[mas]>dm[mal] and dm['close']>dm[mal]:  
            if dm[mas]>dm[mam] and dm['close']>dm[mam]:
                tmp='long'
            elif dm[mas]<dm[mam] and dm['close']>dm[mas]:
                tmp='long'
        if dm[mas]<dm[mal] and dm['close']<dm[mal]:   
            if dm[mas]<dm[mam] and dm['close']<dm[mam]:
                tmp='short'
            elif dm[mas]>dm[mam] and dm['close']<dm[mas]:
                tmp='short'

        return tmp

    def search(self,cnt):
        '''循环找出会出现趋势信号价格,step为5个tick'''
        d_bar=self.daily_bar(cnt)
        w_data=w.wsd(cnt,'close,changelt',self.ytd,self.ytd)
        data=np.array(w_data.Data).T
        fields=list(map(lambda x:x.lower(),w_data.Fields))
        df=pd.DataFrame(data,index=w_data.Times,columns=fields)
        (cl,ltratio)=(w_data.Data[0][0],w_data.Data[1][0])
        lt_up=cl*(1+ltratio*1.0/100)     #涨停价
        lt_down=cl*(1-ltratio*1.0/100)   #跌停价
        tick=float(self.cmdt_table.loc[cnt_to_cmt(cnt)]['ticksize'])*self.min_tick
        (tmp1,tmp2,up_p,down_p)=(float(cl),float(cl),0,0)

        while tmp1 < lt_up:
            tmp1 += tick
            tr=self.ind_trend(cnt,d_bar,tmp1)
            if tr=='long':
                up_p=tmp1
                break 

        while tmp2 > lt_down:
            tmp2 -= tick
            tr=self.ind_trend(cnt,d_bar,tmp2)
            if tr=='short':
                down_p=tmp2
                break 
        
        return up_p,down_p

    def overall(self):
        dic={}
        for i in self.dailyinfo.index:
            cmt=cnt_to_cmt(i)
            ytd_tr=self.ytd_trend.loc[cmt]['Level']
            next_tr=self.search(i)
            if ytd_tr.find('long')==-1 and next_tr[0]>0:
                l_price=next_tr[0]
            else:
                l_price='null'
            if ytd_tr.find('short')==-1 and next_tr[1]>0:
                s_price=next_tr[1]
            else:
                s_price='null'
            dic[cmt]=[l_price,s_price]  
        df=pd.DataFrame(dic,index=[u'buy','sell']).T
        return df



if __name__ == "__main__":
    ytd='2017-12-27'
    p=Predict(ytd)
    df=p.overall()
    print ytd+'|'+u'明日对应趋势价格判断'
    x=PrettyTable([u'品种',u'做多价格',u'做空价格'])  
    for index, row in df.iterrows():
        y=[index,row['buy'],row['sell']]
        x.add_row(y)
    print x 


    '''
    for index, row in df.iterrows():
        if row['buy']=='null' and row['sell']=='null':
            pass
        else:
            print index+':'+str(row[])
    '''