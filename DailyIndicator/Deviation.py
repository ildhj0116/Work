# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 10:09:10 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
from datetime import datetime
from Trend import TriTrend

def KDJ(df,params=None):
    # 1st parameter is pandas data frame
    if params == None:
        params = [9,3,3]
    low = df['low'].rolling(params[0],min_periods=1).min()
#    low.fillna(df['low'].expanding().min(),inplace=True)
    high = df['high'].rolling(params[0],min_periods=1).max()
#    high.fillna(df['high'].expanding().max(),inplace=True)
    rsv = (df['close'] - low) * 100.0 / (high-low) # Raw Stochastic Value
    df['kdj_k'] = rsv.ewm(com=params[1]-1).mean()  # center of mass = 2, decay =1/(2+1) 
    df['kdj_d'] = df['kdj_k'].ewm(com=params[2]-1).mean()
    df['kdj_j'] = 3 * df['kdj_k'] - 2 * df['kdj_d']
    df['kdj_diff'] = df['kdj_k'] > df['kdj_d']
#    df.ix[(df['position']>df['position'].shift(1)),'symbol']='GC'  # gold cross 
#    df.ix[(df['position']<df['position'].shift(1)),'symbol']='DC'  # death cross     
    return df["kdj_diff"] 

def MACD(df,_short=12,_long=26,m=9):
    def get_ema(data,short):
        df = data.copy()
        df["ema"] = [np.nan]*len(df)
        for i in range(len(df)):
            if i == 0: #initial vlaue = price[0]
                df['ema'].iloc[i] = df['close'].iloc[i]
            if i > 0:
                df['ema'].iloc[i] = (2 * df['close'].iloc[i] + (short - 1) * df['ema'].iloc[i-1]) / (short + 1) # ema(0)=2/N * price + (N-1)/(N+1)*ema(-1)
        ema = list(df['ema'])
        return ema 
    df['ema_s'] = get_ema(df,_short)
    df['ema_l'] = get_ema(df,_long)
    df['diff'] = df['ema_s'] - df['ema_l']
    df["dea"] = [np.nan]*len(df)
    for i in range(len(df)):
        if i == 0:  
            df['dea'].iloc[i] = df['diff'].iloc[i] 
        if i > 0:  
            df['dea'].iloc[i] = ( 2 * df['diff'].iloc[i] + (m - 1) * df['dea'].iloc[i-1]) / (m + 1)  
    df['macd'] = 2 * (df['diff'] - df['dea'])         
    return df["macd"]

def TA2Deviation(kdj,macd,trend):
    kdj_dev_list = []
    macd_dev_list = []
    for cnt in trend.index.tolist():
        if trend.loc[cnt].find('Long') == 0 and kdj.loc[cnt] == False:
            kdj_dev = 'top'
        elif trend.loc[cnt].find('Short') == 0 and kdj.loc[cnt] == True:
            kdj_dev = 'bottom'
        else:
            kdj_dev = "null"
        kdj_dev_list.append(kdj_dev)
        # macd背离指标
        #if dailydf['close'][-2]>dailydf['close'][-3] and macd['macd']<0:
        if trend.loc[cnt].find('Long')==0 and macd.loc[cnt] < 0:
            macd_dev = 'top'
        #elif dailydf['close'][-2]<dailydf['close'][-3] and macd['macd']>0:
        elif trend.loc[cnt].find('Short')==0 and macd.loc[cnt] > 0:
            macd_dev = 'bottom'
        else:
            macd_dev = "null"
        macd_dev_list.append(macd_dev)        
    kdj_dev_series = pd.Series(kdj_dev_list,index=trend.index,name=u"KDJ背离")
    macd_dev_series = pd.Series(macd_dev_list,index=trend.index,name=u"MACD背离")
    dev_df = pd.concat([kdj_dev_series,macd_dev_series],axis=1)
    return dev_df

def Deviation(tdate,main_cnt_df,trend):
    cmt_list = main_cnt_df.columns.tolist()
    tdate = datetime.strptime(tdate,"%Y-%m-%d")
    kdj_list = []
    macd_list = []
    main_cnt_list = []
    for cmt in cmt_list:
        tmp_cl = pd.read_csv("../Futures_data/data_cl/"+cmt[:-4]+".csv", index_col=0, parse_dates=[0])
        tmp_high = pd.read_csv("../Futures_data/data_high/"+cmt[:-4]+".csv", index_col=0, parse_dates=[0])
        tmp_low = pd.read_csv("../Futures_data/data_low/"+cmt[:-4]+".csv", index_col=0, parse_dates=[0])
        main_cnt = main_cnt_df.loc[tdate,cmt]
        main_cl = tmp_cl.loc[:tdate,main_cnt].dropna()
        main_high = tmp_high.loc[:tdate,main_cnt].dropna()
        main_low = tmp_low.loc[:tdate,main_cnt].dropna()
        main_price_df = pd.concat([main_cl,main_high,main_low],axis=1)
        main_price_df.columns = ["close","high","low"]
        kdj = KDJ(main_price_df.copy()).iloc[-1]
        macd = MACD(main_price_df.copy()).iloc[-1]
        kdj_list.append(kdj)
        macd_list.append(macd)
        main_cnt_list.append(main_cnt[:-4])
        
    
    kdj_series = pd.Series(kdj_list,index=main_cnt_list,name="kdj")
    macd_series = pd.Series(macd_list,index=main_cnt_list,name="macd")
    dev_df = TA2Deviation(kdj_series,macd_series,trend)
    return dev_df
    
    
    
    
    
if __name__ == "__main__":
    ma_param_df = pd.read_csv("parmt.csv",index_col=0)
    main_cnt_df = pd.read_csv("../Futures_data/main_cnt/data/main_cnt_total.csv",index_col=0,parse_dates=[0])
    tdate = "2018-04-24"
    trend = TriTrend(tdate,ma_param_df,main_cnt_df)
    deviation_df = Deviation(tdate,main_cnt_df,trend)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


