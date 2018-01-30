#coding:utf-8
# updated on 2017-8-28

def kdj(df,params=None):
    # 1st parameter is pandas data frame
    if params==None:
        params=[9,3,3]
    low=df['low'].rolling(params[0]).min()
    low.fillna(df['low'].expanding().min(),inplace=True)
    high=df['high'].rolling(params[0]).max()
    high.fillna(df['high'].expanding().max(),inplace=True)
    rsv=(df['close']-low)*100.0/(high-low) # Raw Stochastic Value
    df['kdj_k']=rsv.ewm(com=params[1]-1).mean()  # center of mass = 2, decay =1/(2+1) 
    df['kdj_d']=df['kdj_k'].ewm(com=params[2]-1).mean()
    df['kdj_j']=3*df['kdj_k']-2*df['kdj_d']
    df['position']=df['kdj_k']>df['kdj_d']
    df.ix[(df['position']>df['position'].shift(1)),'symbol']='GC'  # gold cross 
    df.ix[(df['position']<df['position'].shift(1)),'symbol']='DC'  # death cross 
    
    return df 
