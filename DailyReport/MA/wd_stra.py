# -*- coding: utf-8 -*-

from select_hy import *
from continue_price import *
import datetime as dt
import pandas as pd
import talib as ta
import numpy as np
import os
import pickle
from enum import Enum, unique
from wsi import *
class wama():
    L1 = 1
    L2 = 2
    L3 = 3
    S1 = -1
    S2 = -2
    S3 = -3

#mawa = Enum('mawa', ('L1','L2','L3','S1','S2','S3'))


GOLD = u'金叉'
DEATH = u'死叉'
wd = 'wd_stra' 

  
today = '2018-03-23'
yesterday = '2018-03-22'
TEST_MODE = 0

LONG = u'多头'
SHORT = u'空头'
NO = u'无信号'
long_or_short = '多空分类'
class123 = '均线分类'
contra = '合约'
YES = 'YES'  


def kdj(contract, end_date):
#    result_list = ['','','']
    data = w.wsd(contract,"high,low,close",'2017-01-01', end_date, "")
    data = wind2pandas(data)
    #print(data)
    high = data.HIGH.values
    low = data.LOW.values
    close = data.CLOSE.values
#    print(contract,data.tail(3))
    macd, macdsignal, macdhist = ta.MACD(close)
    k, d = ta.STOCH(high, low, close, fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    if d[-1] > k[-1]:
        return DEATH,k,d
    else:
        return GOLD,k,d
DING = u'顶背离'
DI = u'底背离' 
def beili(k,d,close):
    result = 'NO'
    if k[-2] > d[-2] and k[-1] < d[-1]:
        # SICHA
        if close[-1] > close[-2]:
            result = DING
    if k[-2] < d[-2] and k[-1] > d[-1]:        
        # JINCHA
        if close[-1] < close[-2]:
            result = DI
    return result
        

def wind2pandas(wind_data):
    data = np.array(wind_data.Data).T
    return pd.DataFrame(data, wind_data.Times, columns=wind_data.Fields)





colname = ['long_or_short','class', 'KDJ','dark_horse','beili']
rename_dict = {'long_or_short':'多空分类','class':'均线分类',
               'contract':'合约','dark_horse':'黑马','beili':'背离',
               'ma_warning':'日线提示'}

yesterday_pos = pd.read_excel(os.path.join(wd,'{}.xlsx'.format(yesterday))).set_index(contra).iloc[:,:2]
yesterday_pos[contra] = yesterday_pos.index
yesterday_pos.columns =  [long_or_short,class123, contra]


long_yesterday = set(yesterday_pos[yesterday_pos[long_or_short] == LONG][contra].values)
short_yesterday = set(yesterday_pos[yesterday_pos[long_or_short] == SHORT][contra].values)



def wd_stra(contract,today):
    result = [None] * len(colname)
    weekly = w_ma(contract,today)
    daily = d_ma(contract,today)
    close = daily['close'][-1]
    close_all = daily['close']
    
    if weekly.shape[0] == 0:
        print('{} wind data unavailable'.format(contract))
        return None
    
    w5 = weekly['5w'][-1]
    w10 = weekly['10w'][-1]
    w60 = weekly['60w'][-1]
    d5 = daily['5d'][-1]
    d10 = daily['10d'][-1]
    d60 = daily['60d'][-1]
    d5_1 = daily['5d'][-2]
    d60_1 = daily['60d'][-2]
    
    # if contract not in long_yesterday:
    #     cw = close >= w5
    #     wd = close >= d5
    # else:
    cw = close >= w5*0.995
    cd = close >= d5*0.995
    
    A = w5 > w60
    B = w5 > w10
    
    a = d5 > d60
    b = d5 > d10

    na,nb,nA,nB = map(lambda x:not x, [a,b,A,B])
    
    ncw =  close < w5*1.005
    ncd = close < d5*1.005
    result[colname.index('dark_horse')] = 'NO'
    KDJ,k,d = kdj(contract,today)
#    print(contract,k[-1],d[-1])
    result[colname.index('KDJ')] = KDJ
    result[colname.index('beili')] = beili(k,d,close_all)
    if A  and cw and a:
        #多头信号        
        result[colname.index('long_or_short')] = LONG
        
        if d5_1 < d60_1 and d5>d60 and close > d5 and d5>d10:
            result[colname.index('dark_horse')] = YES
                
        if B and b and cd:
            result[colname.index('class')] = wama.L1
        elif b:
             result[colname.index('class')] = wama.L2
        else:
            result[colname.index('class')] = wama.L3
#
#        if b:       
#            if B:
#                
#                result[colname.index('class')] = wama.L1
#            else:
#                result[colname.index('class')] = wama.L2
#        else:
#            result[colname.index('class')] = wama.L3
            
    elif ncw and nA and  na:
        #空头信号
        result[colname.index('long_or_short')] = SHORT

        if d5_1 > d60_1 and d5 < d60 and close < d5 and d5 < d10:
            result[colname.index('dark_horse')] = YES

        if nB and nb and ncd:
            result[colname.index('class')] = wama.S1
        elif nb:
             result[colname.index('class')] = wama.S2
        else:
            result[colname.index('class')] = wama.S3
#
#        if nb:
#            if nB:
#                result[colname.index('class')] = wama.S1
#            else:
#                result[colname.index('class')] = wama.S2
#        else:
#            result[colname.index('class')] = wama.S3
    else:
        #没信号
        result[colname.index('long_or_short')] = NO

    if (not contract in long_yesterday) and result[colname.index('class')] == wama.L1:
        
        if close < d5:
#            print(contract,'L1',close,d5)
            result = [None] * len(colname)
    if (not contract in short_yesterday) and result[colname.index('class')] == wama.S1:
        
        if close > d5:
#            print(contract,'S2',close,d5)
            result = [None] * len(colname)
        
    return result
    
def get_underlying(contract):
    starts = contract[:2]
    if starts.isalpha():
        return starts
    else:
        return starts[0]

    return dat2.loc[:,['close']],dat

if __name__ == '__main__':
    
    filename = os.path.join(wd,'{}.xlsx'.format(today))
    pickle_data = 'pickle_data'
    multi = pickle.load(open('multi.p','rb'))
    contract_list = []
    
    dd_ = contracts()
    dd = dd_.main_contracts(yesterday)
    contract_list = [x for l in dd.values() for x in l if x[-3:] != 'CFE' and x[-7:-4] != '709']
    
#    contract_ = pd.read_csv(os.path.join('E:\\Python3\\option\\code\\tamarket','listed_contract.csv')).values.T[0].tolist()
#    contract_hy = select_hy_contracts(contract_,today)
#    contract_list = list(set(contract_list + contract_hy))
    df_ori_file = os.path.join(pickle_data,'df_ori-{}.p'.format(today))
    if TEST_MODE:
        df_ori = pickle.load(open(df_ori_file,'rb'))
    else:
        df_ori  = pd.DataFrame([],index=[], columns=colname)
        for contract in contract_list:  
#        for contract in ['JM1801.DCE','JM1805.DCE']:
            try:
                print(contract)
                df_ori.loc[contract] = wd_stra(contract,today)
            except:
                pass
        pickle.dump(df_ori,open(df_ori_file,'wb'))
        

    metal = ['CU','AL','ZN','PB','NI','SN','AG','AU']

    df = df_ori[colname].copy()
    df['contract'] = df.index
    dfsorted = df[(~(df['long_or_short'] == NO)) & df['class'].isin([1,2,-1,-2])].sort(columns=['long_or_short','class','KDJ','contract'],ascending=[1,1,0,1]).dropna()
    dfsorted2 = dfsorted.copy()
    dfsorted2['pz'] = dfsorted2['contract'].map(get_underlying)
    dfsorted2['volume'] = 0
    volume = w.wsd(dfsorted2['contract'].values.tolist(), "volume", today, today, "")
    for index,item in enumerate(volume.Codes):
        dfsorted2.loc[item,'volume'] = volume.Data[0][index]

    signal = list(dfsorted2['contract'])
    for pz in set(dfsorted2['pz']):
        d2 = dfsorted2.loc[dfsorted2['pz']==pz, ['volume','contract']].copy()
#        if pz in metal:
        if 1:
            if d2.shape[0] > 2:
                for i in d2.sort(columns='volume', ascending=[0])['contract'].values[2:]:
                    signal.remove(i)
#        else:
#            if d2.shape[0] > 3:
#                for i in d2.sort(columns='volume', ascending=[0]).values[:3]:
#                    signal.remove(i)
      
    dfsorted=dfsorted.rename(columns=rename_dict).loc[signal]
    
####################################################################### 模拟交易
#    capital = 40000000
#    
#    
##    if 1:
#    def youse_unique(contract_list2,youse):
#        result_youse = set(contract_list2)
#        for item in youse:
#            contract = [i for i in contract_list2 if i[:2] == item]
##            print(contract)
#            if len(contract) > 1:     
#                result_youse  = result_youse - set(contract)                    
#                wdf = w.wsd(contract, "volume", today, today, "")
#                volume_data = wdf.Data[0]
#                youse_codes = wdf.Codes
#                result_youse = result_youse | set([youse_codes[volume_data.index(max(volume_data))]])
#        return result_youse
#    go_long = dfsorted.loc[dfsorted[rename_dict['class']].isin([1,2]),  rename_dict['contract']].values
#    go_short = dfsorted.loc[dfsorted[rename_dict['class']].isin([-1,-2]), rename_dict['contract']].values                      
##    go_long = youse_unique(go_long0,youse)      
##    go_short = youse_unique(go_short0,youse)    
#    if len(go_long) > 0:
#        long_amount = capital/2/len(go_long)
#    if len(go_short) > 0:
#        short_amount = capital/2/len(go_short)
#    today_pos =  dict()
#    for item in go_long:
#        close_data = w.wsd(item, "close", today, today, "")
#        current_close = close_data.Data[0][0]
#        if current_close is not None:
#            today_pos[item] = int(long_amount /(current_close * multi[item]))
#    for item in go_short:
#        close_data = w.wsd(item, "close", today, today, "")
#        current_close = close_data.Data[0][0]
#        if current_close is not None:
#            today_pos[item] = -int(short_amount /(current_close * multi[item]))
#    
#    current_pos = os.path.join('pickle_data','current_pos_{}.d'.format(yesterday))
##    'E:\\Python3\\option\\code\\tamarket'
#    if os.path.exists(current_pos):
#        yesterday_position = pickle.load(open(current_pos,'rb'))
#        trade = dict()
#        for ticker,value in today_pos.items():
#            yes_pos = yesterday_position.get(ticker,0)
#            trade[ticker] = (value ,value -  yes_pos)
#        
#    else:
#        trade = today_pos
#    for ticker,value in yesterday_position.items():
#        if ticker not in today_pos:
#            trade[ticker] = (0,-value)
#    daytime,night = pickle.load(open('trading_time.p','rb'))
#    daytime_dict = {k:trade[k] for k in trade if get_underlying(k) in daytime}    
#    night_dict = {k:trade[k] for  k in trade if get_underlying(k) in night}
#    
#    daytime_dict = sorted(daytime_dict.items(),key=lambda x:x[1][0])
#    night_dict =  sorted(night_dict.items(),key=lambda x:x[1][0])
#    if not TEST_MODE:
#        pickle.dump(today_pos,open(os.path.join('pickle_data','current_pos_{}.d'.format(today)), 'wb'))
    
#######################################################################   
    
    writer = pd.ExcelWriter(filename,engine='xlsxwriter')
    workbook = writer.book
    
    fmt = workbook.add_format()
    fmt.set_align('center')
    fmt.set_align('vcenter')
    
    dfsorted.to_excel(writer, index=False,sheet_name='report')
    
    worksheet = writer.sheets['report']
    worksheet.conditional_format('B2:B60',{'type': '3_color_scale'})
    #worksheet.conditional_format('D2:D60',{'type': '3_color_scale'})
    worksheet.set_column('A:A',15,fmt)
#    worksheet.set_column('B:B',8,fmt)
#    worksheet.set_column('C:C',20,fmt)
    worksheet.set_column('D:D',15,fmt)
    worksheet.set_column('F:H',20,fmt)
#    worksheet.set_column('G:G',8,fmt)
#    worksheet.set_column('H:H',20,fmt)
    worksheet.write('A1',today)

#    
    format1 = workbook.add_format({'bg_color':   '#FFC7CE','font_color': '#9C0006'})
    format2 = workbook.add_format({'bg_color':   '#C6EFCE','font_color': '#006100'})
    format3 = workbook.add_format({'bg_color':   '#FFFF00','font_color': '#000000'})
##    
    worksheet.conditional_format('A2:A60', {'type':     'text',
                                       'criteria': 'containing',
                                       'value':    '多头',
                                       'format':   format1})
    worksheet.conditional_format('A2:A60', {'type':     'text',
                                       'criteria': 'containing',
                                       'value':    '空头',
                                       'format':   format2})
    worksheet.conditional_format('A2:H60', {'type':     'text',
                                       'criteria': 'containing',
                                       'value':    GOLD,
                                       'format':   format3})
#    worksheet.conditional_format('D22:D60', {'type':     'text',
#                                       'criteria': 'containing',
#                                       'value':    DEATH,
#                                       'format':   format2})
#    
#    
    yesterday_pos = pd.read_excel(os.path.join(wd,'{}.xlsx'.format(yesterday))).set_index(contra).iloc[:,:2]
    yesterday_pos[contra] = yesterday_pos.index
    yesterday_pos.columns =  [long_or_short,class123, contra]
    
    long_yesterday = set(yesterday_pos[yesterday_pos[long_or_short] == LONG][contra].values)
    long_today = set(dfsorted[dfsorted[long_or_short] == LONG][contra].values)
    
    long_add = long_today - long_yesterday
    long_remove = long_yesterday - long_today
    
    short_yesterday = set(yesterday_pos[yesterday_pos[long_or_short] == SHORT][contra].values)
    short_today = set(dfsorted[dfsorted[long_or_short] == SHORT][contra].values)
    
    short_add = short_today - short_yesterday
    short_remove = short_yesterday - short_today
    
    row = 1
    col = dfsorted.shape[1] 
    worksheet.write(0,col,'增加')
    
    for i,item in enumerate(long_add):
        worksheet.write(row+i,col, item)
    row = 1+len(long_today)
    for i,item in enumerate(short_add):
        worksheet.write(row+i,col, item)
    
    row = 1
    col += 1
    worksheet.write(0,col,'减少')
    for i,item in enumerate(long_remove):
        worksheet.write(row+i,col, item)
    row = 1+len(long_today)
    for i,item in enumerate(short_remove):
        worksheet.write(row+i,col, item)

    if not TEST_MODE:
        writer.save()

