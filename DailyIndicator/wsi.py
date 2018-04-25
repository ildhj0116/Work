#coding:utf-8
#modified on 2017.8.6
import pandas as pd
import datetime as dt
import numpy as np 
from WindPy import w 
w.start()
'''
functions:
single_bar : to get minutely data for single contracts 
multi_bar: to get minutely data for double contracts 
'''

hourlist=['21:01:00','22:00:00','23:00:00','00:00:00','01:00:00','02:29:00',
            '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']

hourlist2=['21:01:00','22:00:00','23:00:00','23:29:00','00:00:00','01:00:00','02:29:00',
            '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']

def wsi2pandas(wind_data):
    data= np.array(wind_data.Data).T
    fields = [i[:-4] for i in wind_data.Codes]
    #Times=map(to_minutes,wind_data.Times)
    return pd.DataFrame(data, index = wind_data.Times, columns=fields)

def trading_hour(cmt):
    '''
    return trading hours per day according to different commodities 
    parameters: commodity 
    return: hour list 
    '''
    if cmt in ['AU','AG']:
        rn=['21:01:00','22:00:00','23:00:00','00:00:00','01:00:00','02:29:00',
            '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']
    elif cmt in ['NI','PB','CU','SN','ZN','AL']:
        rn=['21:01:00','22:00:00','23:00:00','00:00:00','00:59:00',
            '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']
    elif cmt in ['A','B','M','Y','P','I','JM','J','TA','SR','FG','RM','CF','MA','ZC','OI']:
        rn=['21:01:00','22:00:00','23:00:00','23:29:00',
            '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']
    elif cmt in ['RU','RB','HC','BU']:
        rn=['21:01:00','22:00:00','22:59:00',
            '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']
    elif cmt in ['IF','IH','IC','TF','T']:
        rn=['09:15:00','10:00:00','11:00:00','11:29:00','14:00:00','15:00:00']
    else: 
        rn=['09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00'] # no evening trade 
      
    return rn 

def night_node(cmt):
    if cmt in ['AU','AG']:
        node='02:30:00'
    elif cmt in ['NI','PB','CU','SN','ZN','AL']:
        node='01:00:00'
    elif cmt in ['A','B','M','Y','P','I','JM','J','TA','SR','FG','RM','CF','MA','ZC','OI']:
        node='23:30:00'
    elif cmt in ['RU','RB','HC','BU']:
        node='23:00:00'
    else: 
        node='15:00:00'
    return node 

def commodity(cnt):
    if cnt[1].isdigit():
        cmt=cnt[0]
    else:
        cmt=cnt[:2]
    return cmt 

def _filter(cmt,df):
    '''
    the index must be date time 
    '''
    node=night_node(cmt)
    a=df.index.strftime('%H:%M:%S')<=node
    b=df.index.strftime('%H:%M:%S')>='09:00:00' 
    if node in ['01:00:00','02:30:00']:
        df['valid']=[x or y for x,y in zip(a,b)]
    else:
        df['valid']=[x and y for x,y in zip(a,b)]
    df=df[df['valid']==True].drop('valid',axis=1)
    return df  
    
def _selectlonger(cmt1,cmt2):
    h1=trading_hour(cmt1)
    h2=trading_hour(cmt2)
    if len(h1)>len(h2):
        return cmt2
    else:
        return cmt1  # select the shorter one 

def _single_bar(cnt,cmt,start,end,field='close'):
    #w_data=w.wsi(cnt,field,start,end,"Fill=Previous")
    w_data=w.wsi(cnt,field,start,end)
    df=wsi2pandas(w_data)
    df=_filter(cmt,df)
    df.dropna(inplace=True)
    return df
####### above are tool functions 

###### blew are output functions 
def single_bar(cnt,start,end,field='close'):
    cmt=commodity(cnt)
    #w_data=w.wsi(cnt,field,start,end,"Fill=Previous")
    w_data=w.wsi(cnt,field,start,end)
    df=wsi2pandas(w_data)
    df=_filter(cmt,df)
    df.dropna(inplace=True)
    return df

def multi_bar(cntlist,start,end,mode='ratio',field='close'):
    # double contracts 
    cmt=_selectlonger(commodity(cntlist[0]),commodity(cntlist[1]))
    for i in range(2):
        df=_single_bar(cntlist[i],cmt,start,end)
        if i==0:
            temp=df 
        else:
            df=temp.join(df)
    if mode=='spread':
        df['spread']=df.iloc[:,0]-df.iloc[:,1]
    else:
        df['ratio']=df.iloc[:,0]/df.iloc[:,1]
    return df 

def hourly_ma(cnt,testday,wd=None,sp='ratio'):
    if wd==None:
        wd=[5,60]
    end=testday.strftime('%Y-%m-%d %H:%M:%S') 
    start=(testday-dt.timedelta(days=25)).strftime('%Y-%m-%d %H:%M:%S') 
    if isinstance(cnt,str):
        i=cnt[:-4]
        cmt=commodity(cnt)
        if cmt in ['A','B','M','Y','P','I','JM','J','TA','SR','FG','RM','CF','MA','ZC','OI']:
            hlist=hourlist2
        else:
            hlist=hourlist
        bar=single_bar(cnt,start,end)
        bar_1=bar.copy()
        bar=bar[bar.index.map(lambda x:(x.strftime('%H:%M:%S') in hlist)).tolist()]
        
        bar.loc[bar_1.index[-1]] = bar_1.iloc[-1]
        for m in wd:
            bar['HM'+str(m)]=bar[i].rolling(m).mean()
        
    else:
        bar=multi_bar(cnt,start,end,sp)
        bar_1=bar.copy()
        bar=bar[bar.index.map(lambda x:x.strftime('%H:%M:%S') in hourlist).tolist()]
        bar.loc[bar_1.index[-1]]=bar_1.iloc[-1]
        for m in wd:
            bar['HM'+str(m)]=bar[sp].rolling(m).mean()
    bar.dropna(inplace=True)
    return bar


if __name__ == "__main__":
    start='2017-09-28 21:00:00'
    t='2017-10-09 15:00:00'
    tt=dt.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    kk=hourly_ma('I1801.DCE',tt)
    #kk.columns=['close','h5','h60']
    #kkk=multi_bar(['M1709.DCE','L1709.DCE'],'2017-7-31 09:00:00','2017-8-1 02:00:00')
    #kk.to_csv('E:\\test.csv')
    print kk