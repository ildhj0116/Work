#coding:utf-8
# updated by VIC on 2017.9.5
# updated by LHYM on 2017.12.15

import time
import math  
import pandas as pd
import numpy as np
from WindPy import w 
w.start()

mstock=[[1,2,3,6],[2,3,6,9],[3,4,6,9],[4,5,6,9],[5,6,9,12],[6,7,9,12],
        [7,8,9,12],[3,8,9,12],[3,9,10,12],[3,10,11,12],[3,6,11,12],[1,3,6,12]]
commodities={
'DCE':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I'],
'CZC':['CF','SR','OI','RM','TA','FG','MA','ZC'],
'SHF':['CU','ZN','AL','NI','AU','AG','BU','RU','HC','RB'],
'CFE':['IC','IH','IF','T','TF'],
'ALL':['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I',
       'CF','SR','OI','RM','TA','FG','MA','ZC','CU','ZN','AL',
       'NI','AU','AG','BU','RU','HC','RB','IC','IH','IF','T','TF']}
# total 37 commodities, ignore commodities which are small turnover 
month159=['A','C','CS','M','Y','P','JD','L','PP','V','J','JM','I',
            'CF','SR','OI','RM','TA','FG','MA','ZC','NI','RU']
month1510=['RB','HC']
month6912=['BU']
month612=['AG','AU']
nfmental=['CU','ZN','AL','SN']
stockindex=['IH','IF','IC']
month36912=['T','TF']
def m159(c,m,y,e):
    if e=='CZC':
        y=y%10
        rn=map(lambda x:c+str(y+1)+'0'+str(x)+'.'+e if x<=m 
               else c+str(y)+'0'+str(x)+'.'+e,[1,5,9])
    else:
        rn=map(lambda x:c+str(y+1)+'0'+str(x)+'.'+e if x<=m 
               else c+str(y)+'0'+str(x)+'.'+e,[1,5,9])
    return rn 

def m1510(c,m,y,e):
        rn1=map(lambda x:c+str(y+1)+'0'+str(x)+'.'+e if x<=m 
               else c+str(y)+'0'+str(x)+'.'+e,[1,5])
        rn2=map(lambda x:c+str(y+1)+str(x)+'.'+e if x<=m 
               else c+str(y)+str(x)+'.'+e,[10])
        return rn1+rn2
    
def m6912(c,m,y,e):
        rn1=map(lambda x:c+str(y+1)+'0'+str(x)+'.'+e if x<=m 
               else c+str(y)+'0'+str(x)+'.'+e,[6,9])
        rn2=map(lambda x:c+str(y+1)+str(x)+'.'+e if x<=m 
               else c+str(y)+str(x)+'.'+e,[12])
        return rn1+rn2

def m612(c,m,y,e):
        rn1=map(lambda x:c+str(y+1)+'0'+str(x)+'.'+e if x<=m 
               else c+str(y)+'0'+str(x)+'.'+e,[6])
        rn2=map(lambda x:c+str(y+1)+str(x)+'.'+e if x<=m 
               else c+str(y)+str(x)+'.'+e,[12])
        return rn1+rn2
    
def m36912(c,m,y,e):  #u'暂时过段时间需要人为调整，无法自动去掉第四季度合约
        rn1=map(lambda x:c+str(y+1)+'0'+str(x)+'.'+e if x<=m 
               else c+str(y)+'0'+str(x)+'.'+e,[3,9])
        rn2=map(lambda x:c+str(y+1)+str(x)+'.'+e if x<=m 
               else c+str(y)+str(x)+'.'+e,[12])
        return rn1+rn2
    
def mnfmental(c,m,y,e):
        if m==11:
            (n1,y1,n2,y2)=(12,y,1,y+1)
        elif m==12:
            (n1,y1,n2,y2)=(1,y+1,2,y+1)
        else:
            (n1,y1,n2,y2)=(m+1,y,m+2,y)
        rn1=map(lambda x:c+str(y1)+'0'+str(x)+'.'+e if x<10
               else c+str(y1)+str(x)+'.'+e,[n1])
        rn2=map(lambda x:c+str(y2)+'0'+str(x)+'.'+e if x<10
               else c+str(y2)+str(x)+'.'+e,[n2])
        return rn1+rn2

def mstockindex(c,m,y,e):
        l=mstock[m-1]
        rn=[]
        for i in l:
            if i<m:
                if i<10:
                    rn.append(c+str(y+1)+'0'+str(i)+'.'+e)
                else:
                    rn.append(c+str(y+1)+str(i)+'.'+e)
            else:
                if i<10:
                    rn.append(c+str(y)+'0'+str(i)+'.'+e)
                else:
                    rn.append(c+str(y)+str(i)+'.'+e)
        return rn 
    
## classification 
agri_cmt=['A','C','CS','M','Y','P','JD','CF','SR','OI','RM']
chem_cmt=['L','PP','V','TA','MA','BU','RU']
fmt_cmt=['RB','I','HC','J','JM','ZC','FG']
nfmt_cmt=['CU','NI','AL','ZN','SN']
gld_cmt=['AU','AG']
index_cmt=['IC','IH','IF','T','TF']


def exchange_cmt(exchange='ALL'):
        return commodities[exchange]
    
def exchange(cmt):
        if cmt in commodities['DCE']:
            return 'DCE'
        elif cmt in commodities['CZC']:
            return 'CZC'
        elif cmt in commodities['SHF']:
            return 'SHF'
        else:
            return 'CFE'
        
def generate_cnt(month_,year_):
    _exchange=['DCE','CZC','SHF','CFE']
    dic={}
    for i in _exchange:
        for j in commodities[i]:
            if j in month159:
                dic[j]=m159(j,month_,year_,i)
            elif j in month1510:
                dic[j]=m1510(j,month_,year_,i)
            elif j in month6912:
                dic[j]=m6912(j,month_,year_,i)
            elif j in month612:
                dic[j]=m612(j,month_,year_,i)
            elif j in month36912:
                dic[j]=m36912(j,month_,year_,i)
            elif j in nfmental:
                dic[j]=mnfmental(j,month_,year_,i)
            else:
                dic[j]=mstockindex(j,month_,year_,i)
    return dic
                  
def main_contracts(testday,top=2):
    '''
    select main contracts according to daily volume 
    top:if top=1, choose contract whose volume is largest ...
    '''
    tdy=time.strptime(testday,"%Y-%m-%d")
    sets=generate_cnt(tdy[1],tdy[0]-2000)
    x={}
    result={}
    for key in sets:
        cntlist=sets[key]
        vol=w.wsd(cntlist,'volume',testday,testday).Data[0]
        vol=[0 if math.isnan(i) else i for i in vol] # assume only one NAN at most 
        x[key]=dict(zip(cntlist,vol)) 
        
    for key in x:
        _sort=sorted(x[key].values(),reverse=True)
        rn=[]
        for i in range(top):
            if _sort[i]!=0:
                rn.append(list(x[key].keys())[list(x[key].values()).index(_sort[i])])
            else:
                rn.append(np.NaN)
        result[key]=rn
    return result
        

    
    
    
    
    
    
    
    
    
    
    
    
    