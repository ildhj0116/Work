# encoding: UTF-8

'''
该程序用于实时提示均线趋势策略信号 当前版本v1.0

运行前，配置testday参数, testday表示交易日日期

夜盘时testday需更新为第二天的日期

作者:王文科 当前版本v1.0 日期 20171021
'''
import pickle 
from prettytable import PrettyTable 
import wsi 
import datetime as dt 
import os 
import xlrd
import tech 
import contracts 
from datetime import date
import pandas as pd 
import numpy as np
from WindPy import w 
w.start()

# 参数设置

testday='2017-11-27'  #夜盘用下个交易日时间
spotscd='Basis.xlsm' 
dailyinformationcd='dailyinfo.csv'
trendcd='data\\'
intrade=False   #是否用实时数据计算

#####################################################################################
# 跑程序时间
# [21:01,21:55,22:55,23:20,9:01,9:55,10:55,1:31,14:01,14:50]
ineffective_cmt=['AG','AU','SR','OI','A','C','CF','Y']

# 金属的季节性用国外数据
indexcode={'IC':['000905.SH'],'IH':['000016.SH'],'IF':['000300.SH'],'T':['T.CFE'],'TF':['TF.CFE']}
indexcode1={'000905.SH':'IC','000016.SH':'IH','000300.SH':'IF','T.CFE':'T','TF.CFE':'TF'}

dicmental={
'CU':'CA03M.LME',
'AL':'AH03M.LME',
'ZN':'ZS03M.LME',
'NI':'NI03M.LME',
'SN':'SN03M.LME',
'AU':'SPTAUUSDOZ.IDC',
'AG':'SPTAGUSDOZ.IDC'}

# 计算历史交易日区间, 用于计算季节性胜率
def historytradeday(today_):
    today=pd.to_datetime(today_).date()
    data=list(w.tdays("2000-01-01",today_, "").Data[0])
    def to_date(dt):
        return pd.to_datetime(dt).date()
    def changemonth(mo):
        if mo==12:
            return 1
        else:
            return mo+1
    data=map(to_date,data)
    y=today.year
    m=today.month
    d=today.day
    historyday=[]
    while y>2000:
        y=y-1
        n=date(y,m,d)
        dd=d
        while n not in data:
            if dd==30 or dd==31:
                dd=1
                mm=changemonth(m)
                n=date(y,mm,dd)
            else:
                dd=dd+1
                n=date(y,m,dd) 
        historyday.append(n)
    return historyday

def cnt_to_cmt(cnt):
    if cnt in indexcode1.keys():
        cmt=indexcode1[cnt]
    else:
        if cnt[1].isdigit():
            cmt=cnt[0]
        else:
            cmt=cnt[:2]
    return cmt

def cnt_to_cmt2(cnt):
    try:
        if cnt[1].isdigit():
            cmt=cnt[0]
        else:
            cmt=cnt[:2]
    except:
        cmt=cnt
    return cmt 

# 读取部门每日现货数据
def get_spot():
    cd=spotscd
    book=xlrd.open_workbook(cd)    
    sheet=book.sheet_by_name('Spot')
    dic={}
    for i in range(2):
        col_data=sheet.col_values(i) 
        if i==0:
            key=col_data[0]
        else:
            #key=xlrd.xldate.xldate_as_datetime(col_data[0],0).strftime('%Y-%m-%d')
            key='spot'
        values=col_data[1:]
        dic[key]=values
        df=pd.DataFrame(dic)
    return df

# 计算品种升贴水,跟基差表统一,用中午的盘面数据
def get_basis(cnt,spots,end):
    cmt=cnt_to_cmt(cnt)
    noontime1=end+' 11:29:00'
    noontime2=end+' 11:30:00'
    if cmt in list(spots['Code']):
        spot=spots[spots['Code']==cmt]['spot']
        cl=w.wsi(cnt,'close',noontime1,noontime2,"Fill=Previous").Data[0][0]
        ratio=str(round((cl-spot)*100.0/spot,1))+'%'
    else:
        ratio='null'
    return ratio

# 历史同月合约
def month_contract(x):
    if x in ['000016.SH','000300.SH','000905.SH','T.CFE','TF.CFE']:
        y=x
    else:
        cmt=cnt_to_cmt(x)
        if cmt in ['CU','ZN','AL','NI','SN','AU','AG']:
            y=dicmental[cmt]
        else:
            y=cmt+x[-6:-4]+'M'+x[-4:]
    return y

def wsd2pandas(x):
    return pd.DataFrame(np.array(x.Data).T,index=x.Times,columns=x.Codes) 

# 计算季节性胜率
def win_rate(x,today,duration=None):
    # x must be contract form like M1801.DCE 
    if duration==None:
        duration=historytradeday(today)
    month_ticker=month_contract(x)
    df=w.wsd(month_ticker,'close','2000-03-01',today)

    df=wsd2pandas(df) 
    df['back']=df.rolling(30).mean()
    df['forward']=df['back'].shift(-29)
    df.dropna(inplace=True)
    #df.index=df.index.map(lambda x:x.date())
    def to_date(dt):
    # return date time
        return pd.to_datetime(dt).date()
    df.index=map(to_date,df.index)
    df=df[df.index.isin(duration)]
    df['win']=df['forward']>df['back']
    try:
        rate=df.win.sum()*1.0/df.shape[0]
    except:
    	print x 
    	rate=0
    return round(rate,2)
    
   
# 提取活跃合约代码.国债和股指用主力和指数
def contract(tdy,top):
    dic=contracts.main_contracts(tdy,top)
    
    for key in ['IC','IH','IF','T','TF']:
        dic[key]=indexcode[key]

    for key in ineffective_cmt:  #删除效果不好的品种
        del(dic[key])  

    return dic 


# 季节性和基差等数据每日只需要跑一次并保存，实时数据只需提取相应数据
def dailyinfo(preday):
    duration=historytradeday(preday)
    cnts=contract(preday,1)
    spots=get_spot()
    winr=[]
    basis=[]
    cnt_list=[]
    for key in cnts:
        cnt=cnts[key][0]
        cn=cnt[:-4]
        w=str(int(win_rate(cnt,preday,duration)*100))+'%'
        winr.append(w)
        b=get_basis(cnt,spots,preday)
        basis.append(b)
        cnt_list.append(cnt)
    df=pd.DataFrame(winr,index=cnt_list,columns=['seasonal']) 
    df['contango']=basis
    return df 
####################################################################################

# 提取日线数据
def get_data(cnt,start,end,end2):
    if intrade==True:
        w_data=w.wsd(cnt,'close,low,high',start,end) 
        data=np.array(w_data.Data).T
        fields=list(map(lambda x:x.lower(),w_data.Fields))
        df=pd.DataFrame(data,index=w_data.Times,columns=fields)
        df.dropna(inplace=True)
    
        w_data=w.wsq(cnt,'rt_latest,rt_low,rt_high')
        ti=dt.datetime.now()
    
        if ti.hour>20:
            Times=pd.to_datetime(w_data.Times[0]).date()+dt.timedelta(days=1)
        else:
            Times=pd.to_datetime(w_data.Times[0]).date()
        Data=w_data.Data
        rn=pd.DataFrame(Data,columns=[Times])
        rn=rn.T
        rn.columns=df.columns
        df=df.append(rn)
        # u'模拟下交易日数据'
        nextday=pd.to_datetime(Times).date()+dt.timedelta(days=1)
        nextdata=pd.DataFrame(list(df.iloc[-1]),index=df.columns,columns=[nextday]).T
        df=df.append(nextdata)
    else:
        w_data=w.wsd(cnt,'close,low,high',start,end2) 
        data=np.array(w_data.Data).T
        fields=list(map(lambda x:x.lower(),w_data.Fields))
        df=pd.DataFrame(data,index=w_data.Times,columns=fields)
        df.dropna(inplace=True)
        nextday=pd.to_datetime(end2).date()+dt.timedelta(days=1)
        nextdata=pd.DataFrame(list(df.iloc[-1]),index=df.columns,columns=[nextday]).T
        df=df.append(nextdata)
    return df 

def dailyma(data,ma=None):
    if ma==None:
        ma=[5,10,20,30,60,120]
    for wk in ma:
        data['DM'+str(wk)]=data['close'].rolling(wk).mean()
    data.dropna(inplace=True)
    return data

def wsi_data(cnt,end):
    df=wsi.hourly_ma(cnt,end,[5,60])
    return df 

def hr_cross(cnt,end,preday):
    t=end+' 14:58:00'
    tt=preday+' 21:00:00'
    ttt=dt.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    df=wsi_data(cnt,ttt)
    df.columns=['close','h5','h60']
    df.ix[df['h5']>df['h60'],'up']=1
    df.ix[df['h5']<df['h60'],'down']=1
    df.ix[df['close']>df['h60'],'over']=1
    df.fillna(0,inplace=True)
    df.ix[(df['up']==1) &(df['over']==1),'is_up']=1
    df.ix[(df['down']==1) &(df['over']==0),'is_down']=1
    df.fillna(0,inplace=True)
    df.ix[(df['is_up'].shift(1)==0) & (df['is_up']==1) & (df['down'].shift()==1),'cross_up']=1
    df.ix[(df['is_down'].shift(1)==0) & (df['is_down']==1) & (df['up'].shift()==1),'cross_down']=1
    df.fillna(0,inplace=True)
    a=df.index.strftime('%Y-%m-%d %H:%M:%S')>tt
    b=df.index.strftime('%Y-%m-%d %H:%M:%S')<t
    df['one']=[x and y for x,y in zip(a,b)]
    df=df[df['one']==True].drop('one',axis=1)
    return [int(df['cross_up'].sum()),int(df['cross_down'].sum()),int(df['is_up'][-1]),int(df['is_down'][-1])]
    

def seek(preday):
    '''查找过去进入过入场的数据'''
    num=3
    start=w.tdaysoffset(-num, "2017-10-18", "").Data[0][0].strftime('%Y-%m-%d')
    end=preday
    data=w.tdays(start,end).Data[0]
    longlist=[]
    shortlist=[]
    for i in data:
        dd=i.strftime('%Y-%m-%d')
        cd=trendcd 
        open_path=os.path.join(cd,'{}.csv'.format(dd))
        df=pd.read_csv(open_path,index_col=0)
        for i in df.index:
            a=df.loc[i]['Level']
            b=df.loc[i]['hm_up']
            if a.find('long')==0 and b=='h5>h60|today' and i not in longlist:
                longlist.append(i)
            if a.find('short')==0 and b=='h5<h60|today' and i not in shortlist:
                shortlist.append(i) 
    return longlist,shortlist
    

def anti_trend(data,ms,ml):
    df=data.copy()
    df.drop(df.index[-1],axis=0,inplace=True)
    df['ms']=df['close'].rolling(ms).mean()
    df['ml']=df['close'].rolling(ml).mean()
    for i in [5,10,30,60]:
        df['m'+str(i)]=df['close'].rolling(i).mean()
        df['c'+str(i)]=(df['m'+str(i)]-df['close'])/df['close']
    df.dropna(inplace=True)
    df.ix[df['ms']>=df['ml'],'pos']=1
    df.ix[df['ms']<df['ml'],'pos']=-1
    df.ix[(df['pos']==1)&(df['pos'].shift()==-1),'break']=1
    df.ix[(df['pos']==-1)&(df['pos'].shift()==1),'break']=-1
    df.fillna(0,inplace=True)
    df['id']=range(len(df))
    
    def select(a, b, c, d, pos):
        vlist = [-1*pos*i for i in [a, b, c, d]]
        threshold = 0.005
        temp = 1
        for i in vlist:
            if i > 0 and i < threshold:
                if i<temp:
                    temp=i 
        try:
            return vlist.index(temp)
        except:
            return -1

    def entry_price(df,i):
        data=df.copy()
        data=data[:i+1]
        temp=i
        for j in reversed(range(i+1)):
            if data.iloc[j]['break']!=0:
                temp=j
                break 
            else:
                temp=j
        data=data[temp:]
        position=data['pos'][0]
        close=data['close'][-1]
        if position==1:
            peak=max(data['close'])
        else:
            peak=min(data['close'])
        drawdown=position*(peak-close)/peak    
        return drawdown

    df['dd']=df['id'].map(lambda x:entry_price(df,x))  
    df['dist']=map(lambda a,b,c,d,e:select(a,b,c,d,e),df['c5'],df['c10'],df['c30'],df['c60'],df['pos'])
    dd=df.iloc[-1]['dd']
    ll=int(df.iloc[-1]['dist'])
    indicator=['m5','m10','m30','m60']
    if dd<0.02:
        rtn='null'
    elif ll==-1:
        rtn='null'
    else:
        rtn=indicator[ll]
    return rtn 
     
def indicator(cnt,start,preday,end,ma_paras):
    cmt=cnt_to_cmt(cnt)

    try:
        ma_s=ma_paras.loc[cmt]['ma_short']
        ma_m=ma_paras.loc[cmt]['ma_middle']
        ma_l=ma_paras.loc[cmt]['ma_long']
        mas='DM'+str(ma_s)
        mam='DM'+str(ma_m)
        mal='DM'+str(ma_l)
    except:
        ma_s=5
        ma_m=10
        ma_l=60
        mas='DM5'
        mam='DM10'
        mal='DM60' 
        print cmt+' uses general MA Parasmeters'
    '''
    if cmt in ['AG','AU','AL','BU','CS','FG','HC','I','J','NI','RB','RM','TA','ZC','ZN']:
        longma='DM30'
        ml=30
    else:
        longma='DM60'
        ml=60
    '''

    dailydf=get_data(cnt,start,preday,end)
    #att=round(anti_trend(dailydf,5,ml)*100,2)
    try:
        att=anti_trend(dailydf,5,ma_l)
    except:
        print cmt+' anti_trend error'

    dm=dailyma(dailydf,[5,10,20,30,60,120]).iloc[-1]
    kdj=tech.kdj(dailydf).iloc[-1]
    level=['A','AA','B','UP','AT']
    values=['null']*5
    dic=dict(zip(level,values))
    ti=dt.datetime.now()
    
    
    if ti.hour>20 or ti.hour<9:
        if cmt in ['AU','AG','NI','PB','CU','SN','ZN','AL','A','B','M','Y','P',
                   'I','JM','J','TA','SR','FG','RM','CF','MA','ZC','OI','RU','RB','HC','BU']:
            cross=hr_cross(cnt,end,preday)
        else:
            cross=[0,0,0,0]
    else:
        cross=hr_cross(cnt,end,preday)
        
   
    if cross[2]==1:
        if cross[0]>0: 
            dic['UP']='h5>h60'+'|today'
        else:
            dic['UP']='h5>h60'
    if cross[3]==1:
        if cross[1]>0:
            dic['UP']='h5<h60'+'|today'
        else:
            dic['UP']='h5<h60'
            
    
    if dm[mas]>dm[mal] and dm['close']>dm[mal]:  #and wm['WM5']>wm['WM60'] 
        dic['A']=1
        if dm[mas]>dm[mam] and dm['close']>dm[mam]:
            dic['AA']='long_1'
        elif dm[mas]<dm[mam] and dm['close']>dm[mas]:
            dic['AA']='long_2'
        #elif dm['DM5']<dm['DM10'] and dm['close']<dm['DM5']:
            #dic['AA']='long_3'
    if dm[mas]<dm[mal] and dm['close']<dm[mal]:   # and wm['WM5']<wm['WM60']:
        dic['A']=-1
        if dm[mas]<dm[mam] and dm['close']<dm[mam]:
            dic['AA']='short_1'
        elif dm[mas]>dm[mam] and dm['close']<dm[mas]:
            dic['AA']='short_2'
        #elif dm['DM5']>dm['DM10'] and dm['close']>dm['DM5']:
            #dic['AA']='short_3'
    if dailydf['close'][-1]>dailydf['close'][-2] and kdj['position']==False:
        dic['B']='top deviate'
    elif dailydf['close'][-1]<dailydf['close'][-2] and kdj['position']==True:
        dic['B']='bottom deviate'
    if kdj['symbol']=='GC':
        dic['B']='gold cross'
    elif kdj['symbol']=='DC':
        dic['B']='death cross'
    dic['AT']=att
    return dic 

def overview(dailyinfor,start,preday,end):
    df=dailyinfor
    ma_paras=pd.read_csv('parmt.csv',index_col=0)
    rn={}
    for cnt in df.index:
        if cnt in ['000016.SH','000300.SH','000905.SH','T.CFE','TF.CFE']:
            cn=indexcode1[cnt]
        else:
            cn=cnt[:-4]
        
        try:
            ind=indicator(cnt,start,preday,end,ma_paras)
        except:
            # pass 
            print cnt+' indicator error'

        try:
            ind['W']=df.loc[cnt]['seasonal']
            ind['C']=df.loc[cnt]['contango']
        except:
        	ind['W']='null'
        	ind['C']='null'
        if ind['AA']!='null':
            rn[cn]=ind 
    return rn 
        

def output(dailyinfor,start,preday,end):
    data=overview(dailyinfor,start,preday,end)
    df=pd.DataFrame(data).T
    del df['A']
    # df.sort_values(by=['W'],ascending=[0],inplace=True)
    df.sort_values(by=['AA','W'],ascending=[1,0],inplace=True)
    
    cd=trendcd
    open_path=os.path.join(cd,'{}.csv'.format(preday))
    df0=pd.read_csv(open_path,index_col=0)
    df0.index=map(cnt_to_cmt2,df0.index)  #对index做一个处理,使得合约代码换成商品代码,纠正换月代码不一样的bug
    (AA0,B0)=([],[])
    for i in df.index:
        try:
            c=cnt_to_cmt(i)
            row=df0.loc[c]
            AA0.append(row['Level'])
            B0.append(row['KDJ'])
        except:
            AA0.append('null')
            B0.append('null')
    df['LastLevel']=AA0
    
    df.rename(columns = {'AA':'Level','B':'KDJ','W':'Seasonal',
                         'C':'Contango','UP':'hm_up','AT':'FC'},inplace=True)
    hmup=[]   #修正小时线上穿的定义
    for index, row in df.iterrows():
        l = row['Level']
        last = row['LastLevel']
        hp = row['hm_up']
        if l.find('long')==0 and last=='null': #and hp.find('h5>h60')==0: 日线级别新进的，强制认为是小时线也进入
            hmup.append('h5>h60|today')
        elif l.find('short')==0 and last=='null': # and hp.find('h5<h60')==0: 日线级别新进的，强制认为是小时线也进入
            hmup.append('h5<h60|today')
        else:
            hmup.append(hp)
    df['hm_up']=hmup


    save_path=os.path.join(cd,'{}.csv'.format(end))
    df.to_csv(save_path)
    
    # 趋势信号变动分析 
    ytyindex= [i for i in df0.index if i not in df.index ]
    ytydic={}
    chgdic={}
    try:
        for i in ytyindex:
            ytydic[i]=df0.loc[i]['Level']
    except:
        pass 
    
    for i in df.index:
        a=df.loc[i]['Level']
        b=df.loc[i]['LastLevel']
        if a == b :
            continue
        else:
            chgdic[i]=[b,a]
    
    # 小时线信号分析
    l_e=''
    l_s=''
    s_e=''
    s_s=''

    # 将有过入场信号的合约存于固定list 
    f=file('position.pkl','rb')
    pos=pickle.load(f) 
    long_pos=pos['long']
    short_pos=pos['short']
    f.close()
     
    # 读取入场合约，并更新到position.pkl 数据中
    for i in df.index:
        a=df.loc[i]['Level']
        b=df.loc[i]['hm_up']
        c=df.loc[i]['LastLevel']
        if a.find('long')==0 and b=='h5>h60|today':  #当日小时线上穿且在日线多头的,买入
            l_e=l_e+'|'+i
            if i not in long_pos:
                long_pos.append(i)
        '''
        elif a.find('long')==0 and c.find('long')==-1: #日线多头新进入的,买入
            l_e=l_e+'|'+i
            if i not in long_pos:
                long_pos.append(i)
        '''

        if a.find('short')==0 and b=='h5<h60|today':  #当日小时线下穿且在日线空头的,卖出
            s_e=s_e+'|'+i
            if i not in short_pos:
                short_pos.append(i)
        
        '''
        elif a.find('short')==0 and c.find('short')==-1:  #日线空头新进的,卖出
            l_e=l_e+'|'+i
            if i not in short_pos:
                short_pos.append(i)
        '''

    # 遍历读取需要止损的合约
    for i in long_pos:
        if i not in df.index:
            l_s=l_s+'|'+i
            long_pos.remove(i)
        elif df.loc[i]['Level'].find('short')==0:
            l_s=l_s+'|'+i
            long_pos.remove(i)
        elif df.loc[i]['hm_up'].find('h5<h60')==0:
            l_s=l_s+'|'+i
            long_pos.remove(i)

    for i in short_pos:
        if i not in df.index:
            s_s=s_s+'|'+i
            short_pos.remove(i)
        elif df.loc[i]['Level'].find('long')==0:
            s_s=s_s+'|'+i
            short_pos.remove(i)
        elif df.loc[i]['hm_up'].find('h5>h60')==0:
            s_s=s_s+'|'+i
            short_pos.remove(i)

    # save 到 pkl 
    pos={'long':long_pos,'short':short_pos}
    f1 = file('position.pkl','wb')  
    pickle.dump(pos, f1, True)  
    f1.close() 
    



    once=seek(preday)
    str1=u'做多'
    str2=u'做空'
    
    
    for i in once[0]:
        if i not in df.index:
            str1=str1+','+i+'('+u'消失'+')'
        elif df.loc[i]['Level'].find('short')==0:
            str1=str1+','+i+'('+u'反转'+')'
        elif df.loc[i]['hm_up']=='h5<h60':
            str1=str1+','+i+'('+u'做多'+')'
        else:
            str1=str1+','+i+'('+u'趋势'+')'
            
            
    for i in once[1]:
        if i not in df.index:
            str2=str2+','+i+'('+u'消失'+')'
        elif df.loc[i]['Level'].find('long')==0:
            str2=str2+','+i+'('+u'反转'+')'
        elif df.loc[i]['hm_up']=='h5>h60':
            str2=str2+','+i+'('+u'做空'+')'
        else:
            str2=str2+','+i+'('+u'趋势'+')'
    

    long_str=''
    short_str=''
    for i in long_pos:
        long_str=long_str+'|'+i
    for i in short_pos:
        short_str=short_str+'|'+i

    return df,ytydic,chgdic,l_e,l_s,s_e,s_s,str1,str2,long_str,short_str


if __name__ == "__main__":
    
    runmode='TEST'
    if runmode=='real':
        start='2017-01-01'
        d=w.tdaysoffset(-1,testday,"")
        preday=d.Data[0][0].strftime('%Y-%m-%d')  # notice the string format 
        ti=dt.datetime.now()
        # 有些比如季节性和贴水的数据每天收盘后跑一次,不需要盘中再跑
        if ti.hour>15 and ti.hour<21:       # 15:00 - 21:00 
            dailyifo=dailyinfo(preday)
            dailyifo.to_csv(dailyinformationcd)
        else:
            dailyifo=pd.read_csv(dailyinformationcd,index_col=0)

        data=output(dailyifo,start,preday,testday)
        df=data[0]
        ti=dt.datetime.now()
        print ti.strftime('%Y-%m-%d %H:%M')+'|'+u'均线趋势(long:表示多头;short:表示空头)'
        x=PrettyTable([u'合约',u'趋势级别',u'昨日趋势','KDJ',u'季节性上涨',u'升水现货',u'小时线趋势',u'反抽'])  
        for i in range(len(df)):
            z=df.iloc[i]
            y=[z['Level'],z['LastLevel'],z['KDJ'],z['Seasonal'],z['Contango'],z['hm_up'],z['FC']]
            y.insert(0,df.index[i])
            x.add_row(y)
        print x 
        # output summary information

        print u'信号消失品种:'
        quitlist=''
        try:
            for i in data[1].keys():
                quitlist=quitlist+'|'+i+'('+data[1][i]+')'
        except:
            print u'无'
        print quitlist
        print u'信号变化品种(含新增):'
        changelist=''
        try:
            for i in data[2].keys():
                changelist=changelist+'|'+i+'('+data[2][i][0]+'-'+data[2][i][1]+')'
        except:
            print u'无'
        print changelist 
        print '-------------------------'
        print u'多头持有: '+data[9]
        print u'多头入场: '+data[3]
        print u'多头止损: '+data[4]
        print u'空头持有: '+data[10] 
        print u'空头入场: '+data[5] 
        print u'空头止损: '+data[6]
    
        print '-------------------------'
        print u'过去5日入场品种：'
        
    
        if len(data[7])>60:
            print data[7][:60]
            print data[7][60:]
        else:
            print data[7]
    
        if len(data[8])>60:
            print data[8][:60]
            print data[8][60:]
        else:
            print data[8]

    else:
        
        dd=get_data('HC1805.SHF','2017-1-1','2017-11-24','2017-11-27')
        ddd=dailyma(dd)
        #rnt=anti_trend(dd,5,30)
        ddd.to_csv('test01.csv')
        print ddd  
