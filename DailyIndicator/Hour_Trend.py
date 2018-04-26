# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 14:09:08 2018

@author: Administrator
"""

import wsi
import pandas as pd
from datetime import datetime
from WindPy import w
from Cnt2Cmt import Cnt2Cmt
w.start()



def wsi_data(cnt,end):
    '''获取分钟数据,外部函数'''
    df=wsi.hourly_ma(cnt,end,[5,10,20,30,60])
    return df 

def hr_cross(cnt,end,preday):
    '''小时线上下穿计算'''
    t=end+' 14:58:00'
    tt=preday+' 21:00:00'
    ttt=datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    df=wsi_data(cnt,ttt)
    df.columns=['close','h5','h10','h20','h30','h60']
    df.loc[df['h5']>df['h60'],'up']=1
    df.loc[df['h5']<df['h60'],'down']=1
    df.loc[df['close']>df['h60'],'over']=1
    #设置不同品种的小时线出场信号
    cmt=Cnt2Cmt(cnt)
    if cmt in ['TA']:      # 这些品种还是按长一点的小时均线
        df.loc[df['h5']>=df['h60'],'hm_exit']=1
    elif cmt in ['IH','IC','IF']:
        df.loc[df['close']>df['h20'],'hm_exit']=1
    else:
        df.loc[df['h5']>df['h10'],'hm_exit']=1
    
    df.fillna(0,inplace=True)
    df.loc[(df['up']==1) &(df['over']==1),'is_up']=1
    df.loc[(df['down']==1) &(df['over']==0),'is_down']=1
    df.fillna(0,inplace=True)
    df.loc[(df['is_up'].shift(1)==0) & (df['is_up']==1) & (df['down'].shift()==1),'cross_up']=1
    df.loc[(df['is_down'].shift(1)==0) & (df['is_down']==1) & (df['up'].shift()==1),'cross_down']=1
    df.fillna(0,inplace=True)
    a=df.index.strftime('%Y-%m-%d %H:%M:%S')>tt
    b=df.index.strftime('%Y-%m-%d %H:%M:%S')<t
    df['one']=[x and y for x,y in zip(a,b)]
    df=df[df['one']==True].drop('one',axis=1)
    return [int(df['cross_up'].sum()),int(df['cross_down'].sum()),int(df['up'][-1]),int(df['down'][-1]),int(df['hm_exit'][-1])]




def Hour_Trend(tdate,pre_tdate,main_cnt_df):
    ti=datetime.now()
    tdate_dt = datetime.strptime(tdate,"%Y-%m-%d")
    h_trend_list = []
    main_cnt_list = []
    for cmt in main_cnt_df.columns.tolist():    
        #有些没有夜盘的品种不需要计算晚上的小时线
        
        cnt = main_cnt_df.loc[tdate_dt,cmt]
        cmt = cmt[:-4]
        if ti.hour>19:
            if cmt in ['AU','AG','NI','PB','CU','SN','ZN','AL','A','B','M','Y','P',
                       'I','JM','J','TA','SR','FG','RM','CF','MA','ZC','OI','RU','RB','HC','BU']:
                cross=hr_cross(cnt,tdate,pre_tdate)
            else:
                cross=[0,0,0,0,-1]
        else:
            cross=hr_cross(cnt,tdate,pre_tdate)
            
        
        # 小时线指标的录入
        # h5 vs h60 
        if cross[2]==1:
            h_trend ='h5>h60'
        elif cross[3]==1:
            h_trend ='h5<h60'
        else:
            h_trend = "null"
        h_trend_list.append(h_trend)
        main_cnt_list.append(cnt[:-4])
    h_trend_series = pd.Series(h_trend_list,index=main_cnt_list,name=u"小时线趋势")
    return h_trend_series

if __name__ == "__main__":
    main_cnt_df = pd.read_csv("../Futures_data/main_cnt/data/main_cnt_total.csv",index_col=0,parse_dates=[0])
    tdate_series = pd.read_csv("../Futures_data/others/trade_date.csv",index_col=0)
    tdate = "2018-04-26"
    pre_tdate = tdate_series.loc[:tdate].index[-2]    
    h_trend = Hour_Trend(tdate,pre_tdate,main_cnt_df)





