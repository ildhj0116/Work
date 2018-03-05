# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 13:34:00 2018

@author: 李弘一萌
"""
import pandas as pd
import numpy as np
from WindPy import w
w.start() 

################################################################################################
#                                                                                              #
#                                          回测模块                                             #
#                                                                                              #
################################################################################################

def SpyderNet_1_Signal_Generation(cmt_ITS_series,cmt_UTS_series,para_lambda):    
    cmt_ITS_signal_series = pd.Series(0,index=cmt_ITS_series.index,name=cmt+"_ITS_signal")
    cmt_ITS_signal_series[cmt_ITS_series>para_lambda]= 1
    cmt_ITS_signal_series[cmt_ITS_series<para_lambda]= -1
    cmt_UTS_signal_series = pd.Series(0,index=cmt_UTS_series.index,name=cmt+"_UTS_signal")
    cmt_UTS_signal_series[cmt_UTS_series>para_lambda]= -1
    cmt_UTS_signal_series[cmt_UTS_series<para_lambda]= 1 
    return cmt_ITS_signal_series, cmt_UTS_signal_series


def SpyderNet_1_ITS_UTS_Generation(cmt_oi_series,total_vol_oi_df):
    cmt_oi_series.dropna(inplace=True)
    cmt_ITS_list = []
    cmt_UTS_list = []
    cmt_IT_B_list = []
    cmt_IT_S_list = []
    cmt_UT_B_list = []
    cmt_UT_S_list = []
    
    for i in range(len(cmt_oi_series)):
        tmp_oi_df = cmt_oi_series[i]
        
        if len(tmp_oi_df)<=2:
            ITS=0
            UTS=0
            IT_B = np.nan
            IT_S = np.nan                
            UT_B = np.nan
            UT_S = np.nan
        else:
            oi_sum = tmp_oi_df.drop("date",axis=1).sum()
            total_oi_vol = total_vol_oi_df.iloc[i,:]
            tmp_oi_df.loc["others","vol"] = total_oi_vol.loc["VOLUME"] - oi_sum["vol"]
            tmp_oi_df.loc["others","long_position"] = total_oi_vol.loc["OI"] - oi_sum["long_position"]
            tmp_oi_df.loc["others","short_position"] = total_oi_vol.loc["OI"] - oi_sum["short_position"]
            tmp_oi_df["Stat"] = (tmp_oi_df["long_position"]+tmp_oi_df["short_position"])/tmp_oi_df["vol"]                        
            total_stat = total_oi_vol.loc["OI"] * 2 / total_oi_vol.loc["VOLUME"]
            informed_trader = tmp_oi_df[tmp_oi_df["Stat"]>=total_stat]
            uninformed_trader = tmp_oi_df[tmp_oi_df["Stat"]<total_stat]
            IT_B = informed_trader["long_position"].sum()
            IT_S = informed_trader["short_position"].sum()                    
            UT_B = uninformed_trader["long_position"].sum()
            UT_S = uninformed_trader["short_position"].sum()
            if ((IT_B+IT_S)==0) or ((UT_B+UT_S)==0):
                ITS = 0
                UTS = 0
            else:
                ITS = (IT_B-IT_S)/(IT_B+IT_S)
                UTS = (UT_B-UT_S)/(UT_B+UT_S)
        cmt_IT_B_list.append(IT_B)
        cmt_IT_S_list.append(IT_S)
        cmt_UT_B_list.append(UT_B)
        cmt_UT_S_list.append(UT_S)
        cmt_ITS_list.append(ITS)
        cmt_UTS_list.append(UTS)
        
    cmt_ITS_series = pd.Series(cmt_ITS_list,index=cmt_oi_series.index,name=cmt)
    cmt_UTS_series = pd.Series(cmt_UTS_list,index=cmt_oi_series.index,name=cmt)    
    return cmt_ITS_series,cmt_UTS_series


###############################################################################

def MainCnt_trade_start_end(cnt_series):
    #返回各主力合约的开始和结束时间
    cnt_unique = cnt_series.dropna().unique()
    start_date_list = []
    end_date_list = []
    for cnt in cnt_unique:
        tmp_date_list = cnt_series[cnt_series==cnt].index.tolist()
        start_date_list.append(tmp_date_list[0])
        end_date_list.append(tmp_date_list[-1])
    df = pd.DataFrame([start_date_list,end_date_list],index=["start_date","end_date"],columns=cnt_unique).T    
    return df

###############################################################################
def Spyder_Bktest(signal,main_cnt_list,price_table):
    signal.name = "signal"
    main_cnt_list.name = "main_cnt"
    signal.dropna(inplace=True)
    main_cnt_list.dropna(inplace=True)
    signal_and_cnt = pd.concat([signal,main_cnt_list],axis=1)
    signal_and_cnt.dropna(inplace=True)
    signal_and_price_table = pd.concat([signal_and_cnt,price_table],axis=1) 
    return Bktest(signal_and_price_table["signal"].shift(1),signal_and_price_table["open"],signal_and_price_table["close"])
    
    
def Bktest(signal,open_price,close_price):
    signal.name = "signal"
    open_price.name = "open"
    close_price.name = "close"
    table = pd.concat([signal,open_price,close_price],axis=1)
    table.dropna(inplace=True)
    original_ret = table["close"] / table["open"] - 1
    strat_ret = original_ret * table["signal"]
    strat_ret.name = "ret"
    equity = strat_ret.apply(lambda x:(x+1)).cumprod()
    equity.name = "equity"    
    ret_equity = pd.concat([strat_ret,equity],axis=1)
    return ret_equity
    
    
###############################################################################    
def SpyderNet_Bktest_Price_Generation(main_cnt_list,start_date,end_date):
    open_list = main_cnt_list.shift(1)
    close_list = main_cnt_list.shift(1)
    open_trade_date_table = MainCnt_trade_start_end(open_list)
    close_trade_date_table = MainCnt_trade_start_end(close_list)
    cnt_unique = open_list.dropna().unique()
    open_price_list = []
    close_price_list = []
    for cnt in cnt_unique:
        tmp_open = w.wsd(cnt,"open",open_trade_date_table.loc[cnt,"start_date"],\
                         open_trade_date_table.loc[cnt,"end_date"],"") 
        tmp_open = pd.DataFrame(tmp_open.Data,index=["open"],columns=tmp_open.Times).T
        tmp_open["open_cnt"] = [cnt]*len(tmp_open.index)
        tmp_close = w.wsd(cnt,"close",close_trade_date_table.loc[cnt,"start_date"],\
                         close_trade_date_table.loc[cnt,"end_date"],"") 
        tmp_close = pd.DataFrame(tmp_close.Data,index=["close"],columns=tmp_close.Times).T
        tmp_close["close_cnt"] = [cnt]*len(tmp_close.index)    
        open_price_list.append(tmp_open)
        close_price_list.append(tmp_close)
    open_price_table = pd.concat(open_price_list)
    close_price_table = pd.concat(close_price_list)
    price_table = pd.concat([open_price_table,close_price_table],axis=1)
   
    return price_table

###############################################################################
def Data_Analysis(cmt_oi_series):
    cmt_oi_series.dropna(inplace=True)
    net_long_num = []
    net_short_num = []
    for i in range(len(cmt_oi_series)):
        tmp_oi_df = cmt_oi_series[i]
        tmp_oi_df["net_position"] = tmp_oi_df["long_position"] - tmp_oi_df["short_position"]
        net_long_num.append(tmp_oi_df["net_position"][tmp_oi_df["net_position"]>0].count())
        net_short_num.append(tmp_oi_df["net_position"][tmp_oi_df["net_position"]<0].count())
    net_position_stat = pd.DataFrame([net_long_num,net_short_num],columns=cmt_oi_series.index,index=["net_long","net_short"]).T
    net_position_sum = net_position_stat.sum()
    net_position_stat["net_count_indicator"] = 0
    net_position_stat["net_count_indicator"][net_position_stat["net_short"]>net_position_stat["net_long"]] = -1
    net_position_stat["net_count_indicator"][net_position_stat["net_short"]<net_position_stat["net_long"]] = 1
    #net_position_stat["net_count_indicator"].plot()
    return  

    
################################################################################################
#                                                                                              # 
#                                            绩效评价模块                                       #
#                                                                                              #
################################################################################################
    
def Sharpe(ret_series):     #夏普比率
    ret_series.dropna(inplace=True)
    return ret_series.mean() / ret_series.std() * np.sqrt(252)
    
def Drawdown(equity_series):    #回撤
    max_list = []
    last_max = -10000000
    for equity in equity_series:
        if equity > last_max:
            max_list.append(equity)
            last_max = equity
        else:
            max_list.append(last_max)
    max_equity = pd.Series(max_list,index=equity_series.index,name="max")
    drawdown = (max_equity - equity_series) / max_equity 
    return max_equity,drawdown
    
def Annual_Ret(equity_series):      #年化收益
    date_num = len(equity_series)
    return (equity_series[-1] / equity_series[0] - 1) / date_num * 252    
    
    
def Calmar(annual_ret,max_drawdown):    #Calmar比率
    return annual_ret / max_drawdown

def Performance(equity_series,ret_series):      #绩效评价main函数
    annual_ret = Annual_Ret(equity_series)
    sharpe = Sharpe(ret_series)
    _,drawdown = Drawdown(equity_series)
    max_drawdown = drawdown.max()
    calmar = Calmar(annual_ret,max_drawdown)
    performance = pd.Series([annual_ret,sharpe,max_drawdown,calmar],index=\
                            ["annual_ret","sharpe","max_drawdown","calmar"])
    return performance
    


################################################################################################
#                                                                                              #
#                                                主函数                                         #
#                                                                                              #
################################################################################################    
        
if __name__ =="__main__":
    ###########################################################################
    #设置回测参数
       
    #ITS大于lambda时视为买入信号
    para_lambda_optimize = True
    if para_lambda_optimize==True:
        para_lambda_list = [x/100.0 for x in range(-100,100)]
    else:
        para_lambda_list = [0]
    
    #是否测单独合约
    para_cmt_single = True
    para_cmt = ["IF.CFE"]
    print "部分测试模式，品种为:" + ",".join(para_cmt) if para_cmt_single == True else "全部测试"

    ###########################################################################
    #导入主力合约df
    main_cnt_df = pd.read_csv("main_cnt_revised.csv",parse_dates=[0],index_col=0)
    if para_cmt_single == True:
        cmt_list = para_cmt
    else:
        cmt_list = main_cnt_df.columns.tolist()
      
    ###########################################################################
    #逐品种回测

    for cmt in cmt_list:
        #######################################################################
        #参数优化
        equity_series_list = []
        performance_series_list = []
        try:
            cmt_oi = pd.read_pickle("OI_Data\OI_" + cmt[:-4] + ".tmp")
            total_vol_oi_df = pd.read_csv("OI_Data\OI_total_"+ cmt[:-4] +".csv",parse_dates=[0],index_col=0)
        except IOError as e:
            print e.strerror
        else:
            ITS,UTS = SpyderNet_1_ITS_UTS_Generation(cmt_oi,total_vol_oi_df)
            price_table = SpyderNet_Bktest_Price_Generation(main_cnt_df[cmt],1,1)
            for para_lambda in para_lambda_list:
                ###################################################################
                #产生信号                
                ITS_signal,UTS_signal = SpyderNet_1_Signal_Generation(ITS,UTS,para_lambda)        
                #######################################################################    
                #根据信号进行回测                
                ITS_bktest_result = Spyder_Bktest(ITS_signal,main_cnt_df[cmt],price_table)
                equity = ITS_bktest_result["equity"].copy()
                ret = ITS_bktest_result["ret"].copy()
                performance = Performance(equity,ret)
                #print cmt[:-11] + "净值计算完毕"
                
                equity_series_list.append(equity)
                performance_series_list.append(performance)
                print cmt + ": lambda=" + str(para_lambda) 
                
            equity_df = pd.concat(equity_series_list,axis=1)
            performance_df = pd.concat(performance_series_list,axis=1)
            equity_df.columns = para_lambda_list
            performance_df.columns = para_lambda_list
            performance_df = performance_df.T















