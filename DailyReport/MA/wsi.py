#coding:utf-8
# updated on 2016-10-21
import pandas as pd
import datetime as dt
import numpy as np 
from WindPy import w 
from hour_cross import *
from contracts import contracts
'''
functions:
single_bar : to get minutely data for single contracts 
multi_bar: to get minutely data for double contracts 

'''
hourlist=['21:01:00','22:00:00','23:00:00','00:00:00','01:00:00','02:29:00',
            '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']

hourlist = ['21:01:00','22:00:00','23:00:00','00:00:00','01:00:00','02:29:00',
            '09:01:00','10:00:00','11:00:00','13:29:00','14:00:00','14:59:00']

def wsi2pandas(wind_data):
    data= np.array(wind_data.Data).T
    fields = [i[:-4] for i in wind_data.Codes]
    #Times=map(to_minutes,wind_data.Times)
    index = map(lambda x:x.replace(microsecond=0),wind_data.Times)
    return pd.DataFrame(data, index = list(index), columns=fields)


def trading_hour(cmt):
    '''
    return trading hours per day according to different commodities 
    parameters: commodity 
    return: hour list 
    '''
    if cmt in ['AU','AG']:
        rn=['21:01:00','22:00:00','23:00:00','00:00:00','00:59:00','02:29:00',
            '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']
    elif cmt in ['NI','PB','CU','SN','ZN','AL']:
        rn=['21:01:00','22:00:00','23:00:00','00:00:00','00:59:00',
            '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']
    elif cmt in ['A','B','M','Y','P','I','JM','J','TA','SR','FG','RM','CF','MA','ZC','OI']:
        rn=['21:01:00','22:00:00','23:00:00','23:29:00',
            '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']
    elif cmt in ['IF','IH','IC','TF','T']:
        rn=['09:15:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']
    elif cmt in ['BU','RB','HC','RU']:
        rn = ['21:01:00','22:00:00','22:59:00',
              '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']
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
    elif cmt in ['BU','RB','HC','RU']:
        node = '23:00:00'
    else: 
        node='15:00:00'
    return node 


def commodity(cnt):
    if cnt[1].isdigit():
        cmt=cnt[0]
    else:
        cmt=cnt[:2]
    return cmt 

####### above are tool functions 

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
        return cmt1
    else:
        return cmt2


def single_bar(cnt,start,end,field='close'):
    cmt=commodity(cnt)
    w_data=w.wsi(cnt,field,start,end,"Fill=Previous")
    df=wsi2pandas(w_data)
    df=_filter(cmt,df)
    return df

def _single_bar(cnt,cmt,start,end,field='close'):
    w_data=w.wsi(cnt,field,start,end,"Fill=Previous")
    df=wsi2pandas(w_data)
    df=_filter(cmt,df)
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
    if wd is None:
        wd = [5,60]
    end=testday.strftime('%Y-%m-%d %H:%M:%S') 
    start=(testday-dt.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S') 
    if isinstance(cnt,str):
        i=cnt[:-4]
        bar=single_bar(cnt,start,end)
        bar_1 = bar.copy()
        bar=bar[bar.index.map(lambda x:x.strftime('%H:%M:%S') in hourlist,)]
        bar.loc[bar_1.index[-1]] = bar_1.iloc[-1]
#        bar.loc[]
        for m in wd:
            bar['hma'+str(m)]=bar[i].rolling(m).mean()
    else:
        bar=multi_bar(cnt,start,end,sp)
        bar=bar[bar.index.map(lambda x:x.strftime('%H:%M:%S') in hourlist)]
        for m in wd:
            bar['hma'+str(m)]=bar[sp].rolling(m).mean()
    bar.dropna(inplace=True)
#    print(bar)
    return bar 
CROSSUP = u'上穿'
CROSSDOWN = u'下穿'

def add_date(time1,yesterday,day_before_yesterday):
    if 9<=int(time1[:2])<= 23:
        return yesterday[-5:] + ' ' + time1
    else:
        return day_before_yesterday[-5:] + ' ' + time1

if __name__ == "__main__":
    import os
    w.start()
    TEST = 0
    
    t='2017-11-16 15:01:00'
    yesterday = pd.to_datetime('2017-11-15 20:00:00')
    day_before_yesterday = '2017-11-14'
    
    today = t[:10]
    tt=dt.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')    
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    
#    hours = ['21:01:00','22:00:00','23:00:00','00:00:00','00:59:00',
#            '09:01:00','10:00:00','11:00:00','11:29:00','14:00:00','14:59:00']
#    kk=hourly_ma(['RU1709.SHF','PP1709.DCE'],tt)
#    kkk=multi_bar(['M1709.DCE','L1709.DCE'],'2017-7-31 09:00:00','2017-8-1 02:00:00')


#    contract_ = pd.read_csv(os.path.join('E:\\Python3\\option\\code\\tamarket','listed_contract.csv')).values.T[0].tolist()
    dd_ = contracts()
    dd = dd_.main_contracts(yesterday_str)
    contract_hy = [x for l in dd.values() for x in l if x[-3:] != 'CFE' and x[-7:-4] != '709']
    data_dict = {}
    hour_df = pd.DataFrame()
    
    for ticker in contract_hy:
#    for ticker in ['Y1801.DCE']:
        if ticker == 'CU1708.SHF':
            continue
        print(ticker)
        hourly=hourly_ma(ticker,tt)
#        if ticker == 'RU1801.SHF' and TEST:
#            print(hourly)
#            break
        data_dict[ticker] = hourly
        
        hourly = hourly[yesterday:].copy()
        if hourly.shape[0] == 0:
            continue
        first_row_flag = 1
        result=[np.nan]
        for index,row in hourly.iterrows():
            if first_row_flag:
                last_ma5 = row['hma5']
                last_ma60 = row['hma60']
                first_row_flag = False
                continue
                
            ma5 = row['hma5']
            ma60 = row['hma60']
            close = row[0]
            if last_ma5 > last_ma60 and ma5 < ma60 and close < ma5 :
                result.append(CROSSDOWN)
            elif last_ma5 < last_ma60 and ma5 > ma60 and close > ma5:
                result.append(CROSSUP)
            else:
                result.append(np.nan)
#            print('ma5={0}, ma60={1}, close={2}'.format(ma5,ma60,close))
#            print('last_ma5={0}, ma60={1}'.format(last_ma5, last_ma60))
            last_ma5 = ma5
            last_ma60 = ma60

        hourly[ticker[:-4]] = result
        hour_df = pd.concat([hour_df,hourly.loc[:,[ticker[:-4]]]],axis=1,join='outer')
    
    final_df =hour_df.loc[:,hour_df.isnull().sum()<hour_df.shape[0]]  
    final_df2 = final_df.copy()
    final_df.index = final_df.index.map(lambda x:x.strftime('%H:%M'))
    final_df = final_df.T
    final_df = final_df.loc[:,final_df.isnull().sum() < final_df.shape[0]]
    
    filename = os.path.join('hourly',t.replace(':','-') + '.xlsx')
    writer = pd.ExcelWriter(filename,engine='xlsxwriter')
    final_df.to_excel(writer, index=True,sheet_name='report')
    worksheet = writer.sheets['report']
    workbook = writer.book
    
    fmt = workbook.add_format()
    fmt.set_align('center')
    fmt.set_align('vcenter')
    
    worksheet.set_column('A:Z',13,fmt)
#    worksheet.set_column('B:G',8,fmt)
#    worksheet.set_column('C:C',20,fmt)
#    worksheet.set_column('D:D',15,fmt)
#    worksheet.set_column('F:H',20,fmt)
#    worksheet.set_column('G:G',8,fmt)
#    worksheet.set_column('H:H',20,fmt)
    

    worksheet.write('A1',today)
    if not TEST:
        writer.save()
    print()
    print(final_df)
    final_df2.index = final_df2.index.map(lambda x:x.strftime('%m-%d %H:%M'))
    final_df2 = final_df2.T
    final_df2 = final_df2.loc[:,final_df2.isnull().sum() < final_df2.shape[0]]
    
#    if tt.hour == 15:
    if 1:
        

        yesterday_hourcross = pd.read_excel(os.path.join('hourly',yesterday_str + ' ' + '15-01-00.xlsx'))
        yesterday_hourcross = yesterday_hourcross.set_index(yesterday_str)
        yesterday_hourcross.columns = list(map(lambda x:add_date(x,yesterday_str,day_before_yesterday),yesterday_hourcross.columns))
        if final_df2.shape[0] > 0:
            final_df2.drop_duplicates(inplace=True)
        if yesterday_hourcross.shape[0] >0:
            yesterday_hourcross.drop_duplicates(inplace=True)
        twodays_hour = pd.concat([yesterday_hourcross,final_df2],axis=1)
        filename2 = os.path.join('hourly','two_day','n'+ t.replace(':','-') + '.xlsx')
        writer = pd.ExcelWriter(filename2,engine='xlsxwriter')
        twodays_hour.to_excel(writer, index=True,sheet_name='report')
        worksheet = writer.sheets['report']
        workbook = writer.book
    
        fmt = workbook.add_format()
        fmt.set_align('center')
        fmt.set_align('vcenter')
    
        worksheet.set_column('A:Z',13,fmt)
#     worksheet.set_column('B:G',8,fmt)
#    worksheet.set_column('C:C',20,fmt)
#    worksheet.set_column('D:D',15,fmt)
#    worksheet.set_column('F:H',20,fmt)
#    worksheet.set_column('G:G',8,fmt)
#    worksheet.set_column('H:H',20,fmt)

        writer.save()

        
