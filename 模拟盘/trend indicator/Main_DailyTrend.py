# encoding: UTF-8
'''
该程序用于实时提示均线缠绕策略信号
运行前，配置testday参数, testday表示交易日日期
夜盘时testday需更新为第二天的日期
作者:王文科 当前版本v1.4 日期 20171227
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
 
testday='2018-01-29'  #夜盘用下个交易日时间
spotscd='Basis.xlsm' 
dailyinformationcd='dailyinfo.csv'
trendcd='dataV1.3\\'
intrade=True     #是否用实时数据计算
wholerun=False    #是否更新合约列表和季节性等数据
threshold=0.005  #判定是否接近均线的一个阈值,用于反弹接近的判断
drawd01=0.01     #回撤的判断,大于drawd01才算是回撤
drawd02=0.01     
## ###################################################################################
# 跑程序时间
# [21:01,21:55,22:55,23:20,9:01,9:55,10:55,1:31,14:01,14:50]
ineffective_cmt=['SR','OI','A','C','CF','Y']  #这些品种不适合该策略
# 股指国债的数据源
indexcode={'IC':['000905.SH'],'IH':['000016.SH'],'IF':['000300.SH'],'T':['T.CFE'],'TF':['TF.CFE']}
indexcode1={'000905.SH':'IC','000016.SH':'IH','000300.SH':'IF','T.CFE':'T','TF.CFE':'TF'}
# 金属的季节性用国外数据
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
#合约转换成品种代码
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
def get_basis(cnt,spots,end,bs_adjust):
    cmt=cnt_to_cmt(cnt)
    mcode=cmt+cnt.split('.')[0][-2:]
    noontime1=end+' 11:29:00'
    noontime2=end+' 11:30:00'
    if cmt in list(spots['Code']):
        try:
            #adj=bs_adjust.loc[mcode]['adjust']
            adj=0
        except:
            adj=0
        spot=spots[spots['Code']==cmt]['spot']
        cl=w.wsi(cnt,'close',noontime1,noontime2,"Fill=Previous").Data[0][0]
        ratio=round((spot-cl-adj)*100.0/cl,0)
    else:
        ratio=0
    return ratio
# 历史同月合约获取
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
#wind数据转成pandas 
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
    return round(rate*100,0)
    

# 提取活跃合约代码.国债和股指用主力和指数
def contract(tdy,top):
    dic=contracts.main_contracts(tdy,top)
    for key in ['IC','IH','IF','T','TF']:
        dic[key]=indexcode[key]
    for key in ineffective_cmt:  #删除效果不好的品种
        del(dic[key])  
    return dic 


# 季节性和基差等数据每日只需要跑一次并保存，实时跑的时候只需提取相应数据
def dailyinfo(preday):
    duration=historytradeday(preday)
    bs_adjust=pd.read_csv('basis_adjust.csv',index_col=0) #基差修正值
    cnts=contract(preday,1)
    spots=get_spot()
    winr=[]
    basis=[]
    cnt_list=[]
    for key in cnts:
        cnt=cnts[key][0]
        cn=cnt[:-4]
        w=int(win_rate(cnt,preday,duration))
        winr.append(w)
        b=round(get_basis(cnt,spots,preday,bs_adjust),1)
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
    '''计算均线'''
    if ma==None:
        ma=[5,10,20,30,60,120]
    for wk in ma:
        data['DM'+str(wk)]=data['close'].rolling(wk).mean()
    data.dropna(inplace=True)
    return data

def wsi_data(cnt,end):
    '''获取分钟数据,外部函数'''
    df=wsi.hourly_ma(cnt,end,[5,10,20,30,60])
    return df 

def hr_cross(cnt,end,preday):
    '''小时线上下穿计算'''
    t=end+' 14:58:00'
    tt=preday+' 21:00:00'
    ttt=dt.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    df=wsi_data(cnt,ttt)
    df.columns=['close','h5','h10','h20','h30','h60']
    df.ix[df['h5']>df['h60'],'up']=1
    df.ix[df['h5']<df['h60'],'down']=1
    df.ix[df['close']>df['h60'],'over']=1
    #设置不同品种的小时线出场信号
    cmt=cnt_to_cmt(cnt)
    if cmt in ['TA']:      # 这些品种还是按长一点的小时均线
        df.ix[df['h5']>df['h60'],'hm_exit']=1
    elif cmt in ['IH','IC','IF']:
        df.ix[df['close']>df['h20'],'hm_exit']=1
    else:
        df.ix[df['h5']>df['h10'],'hm_exit']=1
    
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
    return [int(df['cross_up'].sum()),int(df['cross_down'].sum()),int(df['is_up'][-1]),int(df['is_down'][-1]),int(df['hm_exit'][-1])]
    
'''
def seek(preday):
    #查找过去进入过入场的数据
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
'''

def anti_trend(data,ms,mm,ml):
    '''ms,mm,ml分别为三均线的参数'''
    df=data.copy()
    df.drop(df.index[-1],axis=0,inplace=True) #剔除最后一列预测数据
    col=iter(['ms','mm','ml'])  # 均线标志
    dcol=iter(['ds','dm','dl']) # 收盘价与均线的距离标志
    for i in [ms,mm,ml]:
        c=next(col)
        df[c]=df['close'].rolling(i).mean()
        df[next(dcol)]=(df[c]-df['close'])*1.0/df['close']
    df.dropna(inplace=True)
    #均线突破定义
    df.ix[(df['ms']>df['ml'])&(df['close']>df['ml']),'pos']=1 
    df.ix[(df['ms']<df['ml'])&(df['close']<df['ml']),'pos']=-1
    df.fillna(0,inplace=True)
    #均线突破点
    df.ix[(df['pos']==1)&(df['pos'].shift()==-1),'break']=1  
    df.ix[(df['pos']==-1)&(df['pos'].shift()==1),'break']=-1  
    df.fillna(0,inplace=True)
    
    df['id']=range(len(df))  #辅助标记

    def select(a, b, pos):
        '''判断是否接近均线,以及接近哪一条线'''
        '''目前只需分析是否接近长均线和中均线'''
        vlist = [-1*pos*i for i in [a,b]]
        temp = 1
        for i in vlist:
            if i > 0 and i < threshold:
                if i<temp:
                    temp=i 
        try:
            return vlist.index(temp)
        except:
            return -1

    def draw_down(df,i):
        '''计算均线突破后的回撤情况'''
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
        drawdown=position*(peak-close)*1.0/peak    
        return drawdown

    df['dd']=df['id'].map(lambda x:draw_down(df,x))  
    df['dist']=map(lambda a,b,e:select(a,b,e),df['dm'],df['dl'],df['pos'])
    dd=df.iloc[-1]['dd']
    if df.iloc[-1]['pos']==1:
        ps='long'
    elif df.iloc[-1]['pos']==-1:
        ps='short'
    else:
        ps='null'
    ll=int(df.iloc[-1]['dist'])
    ind=['2','3']
    if dd<drawd01:
        rtn='null'
    elif ll==-1:
        rtn='null'
    else:
        rtn=ind[ll]+'_'+ps 
    return rtn,df['dm'][-1],df['dl'][-1]
     
def indicator(cnt,start,preday,end,ma_paras):
    cmt=cnt_to_cmt(cnt)

    try:
        #设置各类均线参数
        ma_s=ma_paras.loc[cmt]['ma_short']
        ma_m=ma_paras.loc[cmt]['ma_middle']
        ma_l=ma_paras.loc[cmt]['ma_long']
        mas='DM'+str(ma_s)
        mam='DM'+str(ma_m)
        mal='DM'+str(ma_l)
    except:
        #默认值
        ma_s=5
        ma_m=10
        ma_l=60
        mas='DM5'
        mam='DM10'
        mal='DM60' 
        print cmt+' uses general MA Parasmeters'

    dailydf=get_data(cnt,start,preday,end)

    try:
        att=anti_trend(dailydf,ma_s,ma_m,ma_l)
    except:
        print cmt+' anti_trend error'

    dm=dailyma(dailydf,[5,10,20,30,60,120]).iloc[-1]
    kdj=tech.kdj(dailydf).iloc[-1]
    level=['A','B','UP','AT','OV','MC','LC']
    # A:趋势判定准则;B:背离指标;UP:5与60小时线;AT:反抽指标;OV:短频小时线;MC:中均线VS收盘价;LC:长均线VS收盘价
    values=['null']*len(level)
    dic=dict(zip(level,values))
    ti=dt.datetime.now()
    
    
    #有些没有夜盘的品种不需要计算晚上的小时线
    if ti.hour>19:
        if cmt in ['AU','AG','NI','PB','CU','SN','ZN','AL','A','B','M','Y','P',
                   'I','JM','J','TA','SR','FG','RM','CF','MA','ZC','OI','RU','RB','HC','BU']:
            cross=hr_cross(cnt,end,preday)
        else:
            cross=[0,0,0,0,-1]
    else:
        cross=hr_cross(cnt,end,preday)
        
    
    # 小时线指标的录入
    # h5 vs h60 
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
    # h vs h60 
    if cross[4]==1:
        dic['OV']='cl>hm'
    elif cross[4]==0:
        dic['OV']='cl<hm'
    else:
        dic['OV']='null'
    

    # 均线判定准则 
    if dm[mas]>dm[mal] and dm['close']>dm[mal]:  
        if dm[mas]>dm[mam] and dm['close']>dm[mam]:
            dic['A']='long_1'
        elif dm[mas]<dm[mam] and dm['close']>dm[mas]:
            dic['A']='long_2'
    if dm[mas]<dm[mal] and dm['close']<dm[mal]:   
        if dm[mas]<dm[mam] and dm['close']<dm[mam]:
            print cnt,dm[mas],dm['close'],dm[mam]
            dic['A']='short_1'
        elif dm[mas]>dm[mam] and dm['close']<dm[mas]:
            dic['A']='short_2'
    
    #因为加了预测值，所以剔除[-1]末尾的收盘价数据
    if dailydf['close'][-2]>dailydf['close'][-3] and kdj['position']==False:
        dic['B']='top deviate'
    elif dailydf['close'][-2]<dailydf['close'][-3] and kdj['position']==True:
        dic['B']='bottom deviate'
    if kdj['symbol']=='GC':
        dic['B']='gold cross'
    elif kdj['symbol']=='DC':
        dic['B']='death cross'
    dic['AT']=att[0]
    dic['MC']=att[1]
    dic['LC']=att[2]
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
        	ind['W']=0
        	ind['C']=0
        rn[cn]=ind 
    return rn 
        

def output(dailyinfor,start,preday,end):
    data=overview(dailyinfor,start,preday,end)
    df=pd.DataFrame(data).T  #df包含所有的品种,包括目前没有信号的品种
    # df.sort_values(by=['W'],ascending=[0],inplace=True)
    df.sort_values(by=['A','W'],ascending=[1,0],inplace=True)
    open_path=os.path.join(trendcd,'{}.csv'.format(preday))
    df0=pd.read_csv(open_path,index_col=0)
    # df0['idx']=map(cnt_to_cmt2,df0.index)  #对index做一个处理,使得合约代码换成商品代码,纠正换月代码不一样的bug
    #对index做一个处理,使得合约代码换成商品代码,纠正换月代码不一样的问题,都用主力合约
    df.index=map(cnt_to_cmt2,df.index)
    AA0=[]
    for i in df.index:
        try:
            row=df0.loc[i]
            AA0.append(row['Level'])
        except:
            AA0.append('null')
    df['LastLevel']=AA0
    df.rename(columns = {'A':'Level','B':'KDJ','W':'Seasonal',
                         'C':'Contango','UP':'hm_up','OV':'hm_over','AT':'FC','MC':'MC','LC':'LC'},inplace=True)

    #仓位管理
    def pos1(x,ps):
        tmp=ps*x*1.0/10
        if tmp>ps:
            tmp=ps
        elif tmp<-ps:
            tmp=-ps
        else:
            pass 
        return tmp 

    def pos2(x,ps):
        tmp=ps*(x*1.0/50-1)
        if tmp>ps:
            tmp=ps
        elif tmp<-ps:
            tmp=-ps
        else:
            pass 
        return tmp 
    
    def pos3(x,ps,ind):
        '''背离的话，这部分仓位没有'''
        if ind=='l':
            if x=='top deviate' or x=='death cross':
                return 0
            else:
                return ps 
            
        elif ind=='s':
            if x=='bottom deviate' or x=='gold cross':
                return 0
            else:
                return ps 

    def basic_pos(cmt):  
        '''金属和黑色基础仓位为5%,其他为3%'''
        if cmt in ['J','JM','RB','HC','I','ZC','NI','ZN','CU','AL']:
            return 5 
        else:
            return 3 



    df['Pos']=map(lambda a,b,x,y,z,c:round(basic_pos(c)*(0.45+pos1(x,0.2)+pos2(y,0.15)+pos3(z,0.2,'l')),1) if a=='long_1' else 
                    round(basic_pos(c)*(0.45-pos1(x,0.2)-pos2(y,0.15)+pos3(z,0.2,'s')),1) if a=='short_1' else
                    round(basic_pos(c)*(0.35+pos1(x,0.2)+pos2(y,0.15)+pos3(z,0.2,'l')),1) if a=='long_2' else 
                    round(basic_pos(c)*(0.35-pos1(x,0.2)-pos2(y,0.15)+pos3(z,0.2,'s')),1) if a=='short_2' else 0,
                    df['Level'],df['LastLevel'],df['Contango'],df['Seasonal'],df['KDJ'],df.index)


    #保存基础数据
    save_path=os.path.join(trendcd,'{}.csv'.format(end))
    df.to_csv(save_path)
     
    '''
    ddf0=df0[df0['Level']!='null']
    ddf=df[df['Level']!='null']
    #趋势信号变动分析 
    ytyindex= [i for i in ddf0.index if i not in ddf.index ]
    ytydic={}    #日级别信号消失
    chgdic={}    #日级别信号变动
    try:
        for i in ytyindex:
            ytydic[i]=ddf0.loc[i]['Level']
    except:
        pass 
    
    for i in ddf.index:
        a=ddf.loc[i]['Level']
        b=ddf.loc[i]['LastLevel']
        if a == b :
            continue
        else:
            chgdic[i]=[b,a]
    '''
    ## 出入场判断(核心板块)
    # 读取之前持有的储存合约
    f=file('holdlist.pkl','rb')
    pos=pickle.load(f) 
    long_hold=pos['long']
    short_hold=pos['short']
    f.close()
    #初始化信号列表,如果有多种情况,可令列表变长
    long_entry=[[],[],[]]         #多头入场
    short_entry=[[],[],[]]
    long_exit=[[],[],[]]          #多头止损出场
    short_exit=[[],[],[]]
    symb=iter(['_01','_02','_03']*4) 
    ## 第一种入场：首次出现日线级别信号
    #判断入场
    for index, row in df.iterrows():
        l=row['Level']
        last=row['LastLevel']
        h=row['hm_over']
        bigh=row['hm_up']
        if l.find('long')==0 and last.find('long')==-1:    
            long_entry[0].append(index)
        elif l.find('short')==0 and last.find('short')==-1: 
            short_entry[0].append(index)
        elif l.find('long')==0 and index not in long_hold and h=='cl>hm' and bigh.find('h5>h60')==0:
            long_entry[0].append(index)
        elif l.find('short')==0 and index not in short_hold and h=='cl<hm' and bigh.find('h5<h60')==0: 
            short_entry[0].append(index)
    #判断出场
    for i in long_hold:
        if i[-1]=='1':
            j=i[:-3]
            try:
                row=df.loc[j]
                if (row['hm_over']=='cl<hm' and j not in long_entry[0]) or (row['Level'].find('long')==-1) or (row['hm_up'].find('h5<h60')==0) : 
                    long_exit[0].append(j)
            except:
                pass 
    for i in short_hold:
        if i[-1]=='1':
            j=i[:-3]
            try:
                row=df.loc[j]
                if (row['hm_over']=='cl>hm' and j not in short_entry[0]) or (row['Level'].find('short')==-1) or (row['hm_up'].find('h5>h60')==0):
                    short_exit[0].append(j)
            except:
                pass

    ## 第二种入场: 回撤至接近中均线
    #判断入场
    for index, row in df.iterrows():
        i=row['FC']
        if i=='2_long':
            long_entry[1].append(index)
        elif i=='2_short':
            short_entry[1].append(index)   
    #判断出场
    for i in long_hold:
        if i[-1]=='2':
            j=i[:-3]
            try:
                row=df.loc[j]
                if row['MC']>0:
                    long_exit[1].append(j)
            except:
                pass 
    for i in short_hold:
        if i[-1]=='2':
            j=i[:-3]
            try:
                row=df.loc[j]
                if row['MC']<0:
                    short_exit[1].append(j)
            except:
                pass

    ## 第三种入场: 回撤至接近长均线
    #判断入场
    for index, row in df.iterrows():
        i=row['FC']
        if i=='3_long':
            long_entry[2].append(index)
        elif i=='3_short':
            short_entry[2].append(index)   
    #判断出场
    for i in long_hold:
        if i[-1]=='3':
            j=i[:-3]
            try:
                row=df.loc[j]
                if row['LC']>0:
                    long_exit[2].append(j)
            except:
                pass
    for i in short_hold:
        if i[-1]=='3':
            j=i[:-3]
            try:
                row=df.loc[j]
                if row['LC']<0:
                    short_exit[2].append(j)       
            except:
                pass

    #更新hold_long
    # print_long_entry
    print_long_entry=''
    print_short_entry=''
    print_long_exit=''
    print_short_exit=''
    #如果有更多种情况的入场时，需修改这里
    for i in long_entry:
        symbl=next(symb)
        for j in i:
            symbol=j+symbl
            if symbol not in long_hold:
               long_hold.append(symbol)
               print_long_entry=print_long_entry+'|'+symbol
    

    for i in short_entry:
        symbl=next(symb)
        for j in i:
            symbol=j+symbl
            if symbol not in short_hold:
               short_hold.append(symbol)
               print_short_entry=print_short_entry+'|'+symbol   

    for i in long_exit:
        symbl=next(symb)
        for j in i:
            symbol=j+symbl
            if symbol in long_hold:
               long_hold.remove(symbol)
               print_long_exit=print_long_exit+'|'+symbol

    for i in short_exit:
        symbl=next(symb)
        for j in i:
            symbol=j+symbl
            if symbol in short_hold:
               short_hold.remove(symbol)
               print_short_exit=print_short_exit+'|'+symbol

            
    # save 到 pkl 
    pos2={'long':long_hold,'short':short_hold}
    f1 = file('holdlist.pkl','wb')  
    pickle.dump(pos2, f1, True)  
    f1.close() 
    
    ### 处理df,剔除没有信号的品种
    df=df[df['Level']!='null']

    ### list转化成字符段
    print_long_hold=''
    print_short_hold=''
    for i in long_hold:
        print_long_hold=print_long_hold+'|'+i
    for i in short_hold:
        print_short_hold=print_short_hold+'|'+i

    # return df,ytydic,chgdic,print_long_hold,print_short_hold,print_long_entry,print_long_exit,print_short_hold,print_short_entry,print_short_exit,long_entry_01,short_entry_01
    return df,print_long_hold,print_long_entry,print_long_exit,print_short_hold,print_short_entry,print_short_exit,long_hold,short_hold

if __name__ == "__main__":
    
    runmode='real'
    if runmode=='real':
        start='2017-01-01'
        d=w.tdaysoffset(-1,testday,"")
        preday=d.Data[0][0].strftime('%Y-%m-%d')  # notice the string format 
        ti=dt.datetime.now()
        # 有些比如季节性和贴水的数据每天收盘后跑一次,不需要盘中再跑
        if wholerun==True:      
            dailyifo=dailyinfo(preday)
            dailyifo.to_csv(dailyinformationcd)
        else:
            dailyifo=pd.read_csv(dailyinformationcd,index_col=0)
            if ti.hour<10 and ti.minute<30:
                dailyifo=dailyifo[dailyifo.index.map(lambda x: x not in indexcode1)] #9:30之前忽略金融期货


        data=output(dailyifo,start,preday,testday)
        df=data[0]
        ti=dt.datetime.now()

        # 打印综合信号
        print ti.strftime('%Y-%m-%d %H:%M')+'|'+u'均线趋势(long:表示多头;short:表示空头)'
        x=PrettyTable([u'合约',u'趋势级别',u'昨日趋势','KDJ',u'季节性(%)',u'升水(%)',u'小时线趋势',u'反抽',u'仓位(%)'])  
        for i in range(len(df)):
            z=df.iloc[i]
            y=[z['Level'],z['LastLevel'],z['KDJ'],z['Seasonal'],z['Contango'],z['hm_up'],z['FC'],z['Pos']]
            y.insert(0,df.index[i])
            x.add_row(y)
        print x 
         
        # 打印出入场信号
        #信号分类
        l01=''
        l02=''
        s01=''
        s02=''
        for i in data[7]:
            if i[-1]=='1':
                l01=l01+'|'+i
            else:
                l02=l02+'|'+i

        for i in data[8]:
            if i[-1]=='1':
                s01=s01+'|'+i
            else:
                s02=s02+'|'+i
        
        print u'多头持有'+'01:'+l01
        print u'多头持有'+'02:'+l02
        print u'多头入场: '+data[2]
        print u'多头止损: '+data[3]
        print '---------------------------'
        print u'空头持有'+'01:'+s01
        print u'空头持有'+'02:'+s02
        print u'空头入场: '+data[5] 
        print u'空头止损: '+data[6]
        
        ## 存入log.txt文件,追加形式
        fh=open('log\\entrylog.txt','a')
        fh.write('\n')
        fh.write(ti.strftime('%Y-%m-%d %H:%M')+'\n')
        fh.write('long_hold: '+data[1]+'\n')
        fh.write('long_entry: '+data[2]+'\n')
        fh.write('long_exit: '+data[3]+'\n')
        fh.write('short_hold: '+data[4]+'\n')
        fh.write('short_entry: '+data[5]+'\n')
        fh.write('short_exit: '+data[6]+'\n')
        fh.close()
        '''
        # 打印信号变化情况
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
        '''
 
    else:
        '''
        start='2017-1-1'
        preday='2017-12-13'
        end='2017-12-18'
        cnt='SF801.CZC'
        '''
        df=get_data('NI1805.SHF','2017-1-1','2017-12-27','2017-12-27')
        
        dd=dailyma(df)
        dd.to_csv('test1227.csv')
        print dd



