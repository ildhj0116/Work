# -*- coding: utf-8 -*-
"""
Created on Thu Mar 08 14:31:41 2018

@author: Administrator
"""
import pandas as pd
import numpy as np

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

def Performance_Main(equity_series,ret_series):      #绩效评价main函数
    annual_ret = Annual_Ret(equity_series)
    sharpe = Sharpe(ret_series)
    _,drawdown = Drawdown(equity_series)
    max_drawdown = drawdown.max()
    calmar = Calmar(annual_ret,max_drawdown)
    performance = pd.Series([annual_ret,sharpe,max_drawdown,calmar],index=\
                            ["annual_ret","sharpe","max_drawdown","calmar"])
    return performance