#coding:utf-8
#import datetime as dt
from WindPy import w 
import pandas as pd
import numpy as np
import datetime as dt



# select common futures with high liquidity 
def filter_lowliqd_futs(x):
    futs=list(x) 
    drp_list=[]
    lowliqd_futs=['B','BB','FB','FU','PB','JR','LR','PM','RI'
                  'SF','SM','SN','WH','WR']        
    # this should be changed according to different cases 
    for stock in futs:
        if stock[1].isdigit():
            x=stock[0]
        else:
            x=stock[:2]
        if x in lowliqd_futs:
            drp_list.append(stock)
    for stock in drp_list:
        futs.remove(stock)
    return futs

def filter_untraded_contrs(x):
    contrs=list(x)
    drp_list=[]
    un_contrs=['000016.SH','000300.SH','000905.SH','TF00.CFE','T00.CFE','USDX.FX','SP500.SPI']
    for stock in contrs:
        if stock in un_contrs:
            drp_list.append(stock)
    for stock in drp_list:
        contrs.remove(stock)
    return contrs
    
# select contracts which's daily volume > 40000 lots
def select_hy_contracts(x,y):
    n=len(x)
    hy_list=[]
    date = pd.to_datetime(y)
    start_date = date - dt.timedelta(20)
    start_date = start_date.strftime('%Y-%m-%d')
    
    d=w.wsd(x,'volume',start_date,y)
    for i in range(n):                   #y means test date
        mean_vol = np.nansum(d.Data[i][-5:])/5.0
        #print(mean_vol)
        if mean_vol > 2e4:
            stock=d.Codes[i]
            hy_list.append(stock)
    return hy_list
if __name__ == '__main__':
    w.start()
    today = '2017-08-09'
    x = select_hy_contracts(['SF709.CZC','SM801.CZC'],today)
