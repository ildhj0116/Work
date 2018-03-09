# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 13:34:00 2018

@author: 李弘一萌
"""
import pandas as pd
from WindPy import w
from Performance import Performance_Main
from Signal_Index_Generation import Signal_Index_Generation_Main
from Signal_Generation import Signal_Generation_Main
from Backtest import OI_Strat_Bktest
w.start() 





################################################################################################
#                                                                                              #
#                                                主函数                                         #
#                                                                                              #
################################################################################################    

###############################################################################
#设置回测参数
   
#ITS大于lambda时视为买入信号
para_lambda_optimize = False
if para_lambda_optimize==True:
    para_lambda_list = [x/100.0 for x in range(-100,100)]
else:
    para_lambda_list = [0]

#是否测单独合约
para_cmt_single = True
para_cmt = ["IF.CFE"]   #单独测试的品种
print "部分测试模式，品种为:" + ",".join(para_cmt) if para_cmt_single == True else "全部测试"

#手续费
para_fee = True
para_fee_rate = 2.0/10000 if para_fee == True else 0

#策略名称
#para_strat_name = "ITS"
para_strat_name = ("oi_factor",1)

#持仓因子回测窗口
para_r = 1

#持仓因子排名前N位
para_n = 5

###############################################################################
###############################################################################
###############################################################################
        
if __name__ =="__main__":

    #导入主力合约时间序列
    main_cnt_df = pd.read_csv("../../Futures_Data/main_cnt/data/main_cnt_total.csv",parse_dates=[0],index_col=0)
    main_cnt_open_df = pd.read_csv("../../Futures_Data/main_cnt/data/main_cnt_open.csv",parse_dates=[0],index_col=0)
    main_cnt_close_df = pd.read_csv("../../Futures_Data/main_cnt/data/main_cnt_close.csv",parse_dates=[0],index_col=0)
    if para_cmt_single == True:
        cmt_list = para_cmt
    else:
        cmt_list = main_cnt_df.columns.tolist()
      
    ###########################################################################
    #逐品种回测

    for cmt in cmt_list:
        #######################################################################
        #开始回测
        equity_series_list = []
        performance_series_list = []
        equity_withfee_series_list = []
        performance_withfee_series_list = []
        try:
            #导入指定品种主力合约会员持仓数据列表
            cmt_oi = pd.read_pickle("../OI_Data/OI_" + cmt[:-4] + ".tmp")
            #导入指定品种主力合约日总持仓量数据
            total_vol_oi_df = pd.read_csv("../OI_Data/OI_total_"+ cmt[:-4] +".csv",parse_dates=[0],index_col=0)
        except IOError as e:
            #处理不存在该品种持仓数据的情况
            print cmt + "持仓数据导入失败: " + e.strerror
        else:            
            #导入开平仓价格
            open_cmt = main_cnt_open_df[cmt]
            close_cmt = main_cnt_close_df[cmt]
            price_table = pd.concat([open_cmt,close_cmt],axis=1)
            price_table.columns = ["open","close"]
            price_table.dropna(inplace=True)
            print "开平仓价格导入完毕"
                        
            #生成指标            
            index = Signal_Index_Generation_Main(para_strat_name,cmt_oi,total_vol_oi_df,para_r,para_n)
            print "指标生成完毕"
            
            #参数优化
            for para_lambda in para_lambda_list:
                ###################################################################
                #产生信号                
                signal = Signal_Generation_Main(para_strat_name,index,para_lambda)
                #######################################################################    
                #根据信号进行回测                
                bktest_result = OI_Strat_Bktest(signal,main_cnt_df[cmt],price_table)
                bktest_result_withfee = OI_Strat_Bktest(signal,main_cnt_df[cmt],price_table,para_fee_rate)
                equity = bktest_result["equity"].copy()
                ret = bktest_result["ret"].copy()
                performance = Performance_Main(equity,ret)
                
                equity_withfee = bktest_result_withfee["equity"].copy()
                ret_withfee = bktest_result_withfee["ret"].copy()
                performance_withfee = Performance_Main(equity_withfee,ret_withfee)
                #print cmt[:-11] + "净值计算完毕"
                
                equity_series_list.append(equity)
                performance_series_list.append(performance)
                
                equity_withfee_series_list.append(equity)
                performance_withfee_series_list.append(performance)                
                print cmt + ": lambda=" + str(para_lambda) 
                
            equity_df = pd.concat(equity_series_list,axis=1)
            performance_df = pd.concat(performance_series_list,axis=1)
            equity_withfee_df = pd.concat(equity_series_list,axis=1)
            performance_withfee_df = pd.concat(performance_series_list,axis=1)
            equity_df.columns = para_lambda_list
            performance_df.columns = para_lambda_list
            performance_df = performance_df.T
            equity_withfee_df.columns = para_lambda_list
            performance_withfee_df.columns = para_lambda_list
            performance_withfee_df = performance_withfee_df.T














