#coding:utf-8
# updated on 2016-10-21
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import datetime as dt
import numpy as np
#from conversion import wind_time_transfer as wtr
from WindPy import w
w.start()

# get contracts' trade cycle
def get_cycle(x):
    code=x
    tdy=dt.date.today()
    field=['ipo_date','lasttrade_date']
    oneyear_stocks=['AG','AL','B','BB','C','CF','CS','CU','FB','FG',
                    'FU','HC','I','J','JD','JM','JR','L','LR','M',
                    'MA','NI','OI','P','PB','PM','PP','RB','RI','RM',
                    'RS','RU','SF','SM','SN','TA','V','WH','WR','Y',
                    'ZC','ZN']
    if code[1].isdigit():
        stock=code[0]
    else:
        stock=code[:2]
    if stock in oneyear_stocks:
        cycle=12
    else:
        y=w.wsd(code,field,tdy,tdy)
        cycle=round((y.Data[1][0]-y.Data[0][0]).days/30.0)  # roughly count months
    return cycle                                             # return a string
def get_continue_contr(x):
    cycle=get_cycle(x)
    if x[1].isdigit():
        stock=x[0]
    else:
        stock=x[:2]

    if cycle>12:
        if x[-3:]=='CZC':
            yr=int(x[-7:-6])
            y=stock+str(1)+str(yr-2)+x[-6:]

            
        else:
            yr=int(x[-8:-6])
            y=stock +str(yr-2)+x[-6:]
        
    else:
        y=stock+x[-6:-4]+'M'+x[-4:]
    #print('get_continue_contr():{0}----->{1}. cycle:{2}'.format(x,y,cycle))
    return y

def weekly_price(x,y):
# x means the contract and y means the test date
    index_futs=['000016.SH','000300.SH','000905.SH',
                'TF00.CFE','T00.CFE']
    if x in index_futs:
        cycle=12
        lstock=x
    else:
        cycle=get_cycle(x)
        lstock=get_continue_contr(x)

    if cycle>12:
        cipo=w.wsd(x,'ipo_date',y,y).Data[0][0]
        lipo=w.wsd(lstock,'ipo_date',y,y).Data[0][0]
        ltrade=w.wsd(lstock,'lasttrade_date',y,y).Data[0][0]
        z0=w.wsd(x,'close',cipo,y,'Per=W')
        z1=w.wsd(lstock,'close',lipo,ltrade,'Per=W')
        t=z1.Times+z0.Times
        d=z1.Data[0]+z0.Data[0]
        dat=pd.DataFrame(d)
        dat.index=t
        dat.dropna(inplace=True)
    else:
        z0=w.wsd(lstock,'close','-800D',y,'Per=W')
        z1=w.wsd(x,'close',y,y)
        t=z0.Times
        z0.Data[0][-1]=z1.Data[0][-1]
        #print(np.isnan(z0.Data[0]).sum()/len(z0.Data[0]),'  :79')
        d=z0.Data[0]
        dat=pd.DataFrame(d)
        dat.index=t
        dat = dat.dropna()
    return dat

def daily_price(x,y):
    index_futs=['000016.SH','000300.SH','000905.SH',
                'TF00.CFE','T00.CFE']

    if x in index_futs:
        cycle=12
        lstock=x
    else:
        cycle=get_cycle(x)
        lstock=get_continue_contr(x)

    if cycle>12:
        cipo=w.wsd(x,'ipo_date',y,y).Data[0][0]
        lipo=w.wsd(lstock,'ipo_date',y,y).Data[0][0]
        ltrade=w.wsd(lstock,'lasttrade_date',y,y).Data[0][0]
        z0=w.wsd(x,'close',cipo,y,'Per=D')
        z1=w.wsd(lstock,'close',lipo,ltrade,'Per=D')
        t=z1.Times+z0.Times
        d=z1.Data[0]+z0.Data[0]
        dat=pd.DataFrame(d)
        dat.index=t
        dat.dropna(inplace=True)
    else:
        z0=w.wsd(lstock,'close','-100D',y,'Per=D')
        z1=w.wsd(x,'close',y,y)
        t=z0.Times
        z0.Data[0][-1]=z1.Data[0][-1]
        d=z0.Data[0]
        dat=pd.DataFrame(d)
        dat.index=t
        
    return dat.dropna()
'''
def hourly_price(x,y):
# x means the contract and y means the test date,the format of y is date-time
    todate=y.strftime('%Y-%m-%d %H:%M:%S')
    fromdate=(y-dt.timedelta(days=15)).strftime('%Y-%m-%d %H:%M:%S')
    data=w.wsi(x,'close',fromdate,todate)
    d=data.Data[0]
    dat=pd.DataFrame(d,columns=['close'])
    dat.index=wtr(data.Times,0)
    dat['minute']=wtr(data.Times,1)
    select_minute=['21:00:00','22:00:00','23:00:00','09:00:00','10:00:00','11:00:00','11:29:00','14:00:00','15:00:00']
    dat=dat[dat['minute'].isin(select_minute)]
    dat=dat.dropna(axis=0)
    return dat
'''

def weekly_ma(x,y,z):
# x means contract , y means test day , z means the rolling window
    dat=weekly_price(x,y)
    ma=pd.rolling_mean(dat,z, min_periods=1)
    return ma

def daily_ma(x,y,z):
    dat=daily_price(x,y)
    ma=pd.rolling_mean(dat,z, min_periods=1)
    return ma

def w_ma(x,y):
    dat=weekly_price(x,y)
    dat.columns=['close']
    dat['5w']=pd.rolling_mean(dat['close'],5)
    dat['10w']=pd.rolling_mean(dat['close'],10)
    dat['20w']=pd.rolling_mean(dat['close'],20)
    dat['30w']=pd.rolling_mean(dat['close'],30)
    dat['60w']=pd.rolling_mean(dat['close'],60)
    dat = dat.dropna()
#    print(dat.tail())
    return dat.tail(2)

def d_ma(x,y,n=2):
    dat=daily_price(x,y)
    dat.columns=['close']
    dat['5d']=pd.rolling_mean(dat['close'],5)
    dat['10d']=pd.rolling_mean(dat['close'],10)
    dat['20d']=pd.rolling_mean(dat['close'],20)
    dat['30d']=pd.rolling_mean(dat['close'],30)
    dat['60d']=pd.rolling_mean(dat['close'],60)
    dat.dropna(inplace=True)
    return dat.tail(n)

def h_ma(x,y,n=1):       # this will be combined with Rt_price to get the true MA
    dat=hourly_price(x,y)
    dat['5h']=pd.rolling_mean(dat['close'],4)
    dat['10h']=pd.rolling_mean(dat['close'],9)
    dat['20h']=pd.rolling_mean(dat['close'],19)
    dat['30h']=pd.rolling_mean(dat['close'],29)
    dat['60h']=pd.rolling_mean(dat['close'],59)
    return dat.tail(n)

if __name__ == "__main__":
    pass
    today = '2017-03-16'
    dai_ma = d_ma('M1705.DCE',today)
    week_ma = w_ma('M1705.DCE',today)
    yesterday = '2017-03-15'
    dai_ma2 = d_ma('M1705.DCE',yesterday)
    week_ma2 = w_ma('M1705.DCE',yesterday)
    
