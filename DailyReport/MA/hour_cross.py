# -*- coding: utf-8 :*-
"""
Created on Wed Jul 26 15:35:28 2017

@author: Administrator
"""
import pandas as pd
import numpy as np
from WindPy import *
#from continue_price import *
from select_hy import *
import os
import datetime as dt
def hourly_price(contract,date):
# compute dialy ma5 and ma60 after marktet closed
    todate=date + ' 15:01:00'
    fromdate=(pd.to_datetime(todate)-dt.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    data=w.wsi(contract,'close',fromdate,todate,"Fill=Previous")
    d=data.Data[0]
    dat=pd.DataFrame(d,columns=data.Fields,index = data.Times)
    dat['minute']=list(map(lambda x:x.time().replace(second=0).strftime('%H:%M:%S'),dat.index))
    select_minute=['21:00:00','22:00:00','23:00:00','09:00:00','10:00:00','11:00:00','11:29:00','14:00:00','15:00:00']
    dat2=dat[dat['minute'].isin(select_minute)]
    index = list(map(lambda x:x.replace(microsecond=0),dat2.index))
    dat2.index = index

    return dat2.loc[:,['close']],dat



def ma_cross(close,ma1,ma2):
    
    pass

if __name__ == '__main__':
    w.start()
    today = '2017-08-11'
    contract_ = pd.read_csv(os.path.join('E:\\Python3\\option\\code\\tamarket','listed_contract.csv')).values.T[0].tolist()
    contract_hy = select_hy_contracts(contract_,today)
    hourx_dict = dict()
    dailyx_dict = dict()
    hourx_dict_down = dict()
    dailyx_dict_down = dict()
    wind_daily = w.wsd(contract_hy, 'close','2017-03-01',today,'')
    daily_data = pd.DataFrame(np.array(wind_daily.Data).T, index = wind_daily.Times, columns=wind_daily.Codes) 
#    hour_df = pd.DataFrame([])
    data_dict =  dict()
    hour_df,_ = hourly_price('RB1801.SHF',today)
    hour_df = hour_df[hour_df.index.date == pd.to_datetime(today).date()].copy()
    for ticker in contract_hy[:]:
        break
        print(ticker)
        
        hp,_ = hourly_price(ticker,today)
        hp['ma5'] = hp['close'].rolling(window=5).mean()
        hp['ma60'] = hp['close'].rolling(window=60).mean()
        
        today_quote = hp[hp.index.date == pd.to_datetime(today).date()].copy()
        today_quote['ma5>ma60'] = today_quote['ma5'] > today_quote['ma60']
        today_quote ['hourly'] = None
        
        first_flag = 1
        result = [None]

        for index,row in today_quote.iterrows():            
            if first_flag:
                
                last_ma5 = row['ma5']
                last_ma60 = row['ma60']
                first_flag = False
                continue
                
            ma5 = row['ma5']
            ma60 = row['ma60']
            close = row['close']
            if last_ma5 > last_ma60 and ma5 < ma60 and close < ma5 :
                result.append(CROSSDOWN)
            elif last_ma5 < last_ma60 and ma5 > ma60 and close > ma5:
                result.append(CROSSUP)
            else:
                result.append(None)
            last_ma5 = ma5
            last_ma60 = ma60
        today_quote['hourly'] = result
        data_dict[ticker] = today_quote
        hour_df.loc[today_quote.index,ticker] = result
#    hour_df.index = today_quote.index
#    hour_df = hour_df.loc[:, hour_df.isnull().sum()<6].T
#    hour_df.drop('close',axis=0, inplace=True)
#    hour_df.columns = list(map(lambda x:x.time().strftime('%H:%M:%S'),hour_df.columns))
#    print(hour_df)

    
                       
    for ticker in contract_hy:
        print(ticker +  'day')
        mad = False
        mad_down = False
        close = daily_data[ticker].iat[-1]
        ma5d = daily_data[ticker].rolling(5).mean()
        ma60d = daily_data[ticker].rolling(60).mean()
        if ma5d[-2] > ma60d[-2] and ma5d[-1] < ma60d[-1] and close > ma5d[-1]:
            mad_down = True
        if ma5d[-2] < ma60d[-2] and ma5d[-1] > ma60d[-1] and close < ma5d[-1]:
            mad = True
        
        dailyx_dict[ticker] = mad
        dailyx_dict_down[ticker] = mad_down
        
    
    df = pd.DataFrame.from_dict(data=dailyx_dict,orient='index')
    df.columns = ['daily']


    dfd = pd.DataFrame.from_dict(data=dailyx_dict_down,orient='index')
    dfd.columns = ['daily']

    print()
    print(today)
    print('日线提示')
#    print('小时线 首次 MA5 上穿 MA60：',list(df[df['hourly']==1].index))
    print('日线   首次 MA5 上穿 MA60：',list(df[df['daily']==1].index))
#    
#    print()
#    print('日线小时线提示（下穿）')
#    print('小时线 首次 MA5 下穿 MA60：',list(dfd[dfd['hourly']==1].index))
    print('日线   首次 MA5 下穿 MA60：',list(dfd[dfd['daily']==1].index))
    
#    hourx_df = pd.DataFrame.from_dict(data=hourx_dict,orient='index')
#    hourx_df.columns = ['ma5xma60']
#    hourx_dfsort = hourx_df.sort(columns=['ma5xma60'],ascending=[0])
#    hourx_dfsort.to_excel('ma50xma60.xlsx')




    filename = os.path.join('hourly',today+'.xlsx')
    writer = pd.ExcelWriter(filename,engine='xlsxwriter')
    hour_df.to_excel(writer, index=True,sheet_name='report')
    worksheet = writer.sheets['report']
    workbook = writer.book
    
    fmt = workbook.add_format()
    fmt.set_align('center')
    fmt.set_align('vcenter')
    
    worksheet.set_column('A:G',12,fmt)
#    worksheet.set_column('B:G',8,fmt)
#    worksheet.set_column('C:C',20,fmt)
#    worksheet.set_column('D:D',15,fmt)
#    worksheet.set_column('F:H',20,fmt)
#    worksheet.set_column('G:G',8,fmt)
#    worksheet.set_column('H:H',20,fmt)
    

    worksheet.write('A1',today)
    writer.save()


