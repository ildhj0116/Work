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



 

###############################################################################
#设置回测参数
   
#ITS大于lambda时视为买入信号
para_lambda_optimize = False
if para_lambda_optimize==True:
    para_lambda_list = [x/100.0 for x in range(-100,100)]
else:
    para_lambda_list = [0]

#是否测单独合约
para_cmt_single = False
para_cmt = ["A.DCE"]   #单独测试的品种
print "部分测试模式，品种为:" + ",".join(para_cmt) if para_cmt_single == True else "全部测试"

#手续费
para_fee = False
para_fee_rate = 2.0/10000 if para_fee == True else 0

#策略名称
#para_strat_name = "ITS"
para_strat_name = ("oi_factor",8)

#持仓因子回测窗口
para_r = 1

#持仓因子排名前N位
para_n = 5


###############################################################################
#持仓数据导入
def OI_Data_Import(cmt):
    #导入指定品种主力合约会员持仓数据列表
    cmt_oi = pd.read_pickle("../OI_Data/OI_" + cmt[:-4] + ".tmp")
    cmt_oi_TopN = pd.read_pickle("../OI_TopN_Data/OI_" + cmt[:-4] + ".tmp")
    #导入指定品种主力合约日总持仓量数据
    total_vol_oi_df = pd.read_csv("../OI_Data/OI_total_"+ cmt[:-4] +".csv",parse_dates=[0],index_col=0)
    return cmt_oi,cmt_oi_TopN,total_vol_oi_df


###############################################################################
#回测及优化模块
def Backtest_Main(strat_name,main_cnt,cmt_oi,total_oi,price_table,para_r=1,para_n=5,para_lambda=0,para_fee_rate=0):
    #产生指标
    index = Signal_Index_Generation_Main(strat_name,cmt_oi,total_oi,para_r,para_n)
    #产生信号 
    signal = Signal_Generation_Main(strat_name,index,para_lambda)
    #######################################################################    
    #根据信号进行回测                
    bktest_result = OI_Strat_Bktest(signal,main_cnt,price_table,para_fee_rate)
    return bktest_result



################################################################################################
#                                                                                              #
#                                                主函数                                         #
#                                                                                              #
################################################################################################   
        
if __name__ =="__main__":
    ###########################################################################
    #数据准备
    
    #导入主力合约时间序列
    main_cnt_df = pd.read_csv("../../Futures_Data/main_cnt/data/main_cnt_total.csv",parse_dates=[0],index_col=0)
    main_cnt_open_df = pd.read_csv("../../Futures_Data/main_cnt/data/main_cnt_open.csv",parse_dates=[0],index_col=0)
    main_cnt_close_df = pd.read_csv("../../Futures_Data/main_cnt/data/main_cnt_close.csv",parse_dates=[0],index_col=0)
    if para_cmt_single == True:
        original_cmt_list = para_cmt
    else:
        original_cmt_list = main_cnt_df.columns.tolist()
    
    #导入所有测试品种持仓数据
    effective_cmt_list = []
    cmt_oi_list = []
    total_oi_list = []
    for cmt in original_cmt_list:
        try:
            #导入指定品种主力合约会员持仓数据列表及当日该合约总持仓量列表
            cmt_oi,cmt_oi_TopN,total_vol_oi_df = OI_Data_Import(cmt)
        except IOError as e:
            #处理不存在该品种持仓数据的情况
            print cmt + "持仓数据导入失败: " + e.strerror            
        else:
            if (para_strat_name == "ITS") or (para_strat_name == "UTS"):
                cmt_oi_list.append(cmt_oi)
            elif (type(para_strat_name) == tuple) and (para_strat_name[0]== "oi_factor"):
                cmt_oi_list.append(cmt_oi_TopN)
            effective_cmt_list.append(cmt)
            total_oi_list.append(total_vol_oi_df)
    print "价格及持仓数据导入完毕"
    oi_data = pd.DataFrame([cmt_oi_list,total_oi_list],index=["oi_table","total_oi"],columns=effective_cmt_list)
    
    ###########################################################################
    #逐品种回测
    equity_cmt_list = []
    perf_cmt_list = []
    for cmt in effective_cmt_list:
        #######################################################################
        #初始化各列表
        equity_series_list = []
        performance_series_list = []
        
        annual_ret_list = []
        sharpe_list = []
        MD_list = []
        
        #导入开平仓价格
        open_cmt = main_cnt_open_df[cmt]
        close_cmt = main_cnt_close_df[cmt]
        price_table = pd.concat([open_cmt,close_cmt],axis=1)
        price_table.columns = ["open","close"]
        price_table.dropna(inplace=True)
        #导入持仓数据
        cmt_oi = oi_data.loc["oi_table",cmt]
        total_oi = oi_data.loc["total_oi",cmt]
        
        
        #开始回测
        for para_lambda in para_lambda_list:            
            bk_result = Backtest_Main(para_strat_name,main_cnt_df[cmt],cmt_oi,total_oi,price_table,para_r,para_n,para_lambda)
            equity = bk_result["equity"]
            ret = bk_result["ret"]            
            perf = Performance_Main(equity,ret)
            equity_series_list.append(equity)
            performance_series_list.append(perf)        
            #print cmt + ": lambda=" + str(para_lambda) 
        
        #记录净值及评价结果
        equity_df = pd.concat(equity_series_list,axis=1)
        performance_df = pd.concat(performance_series_list,axis=1)
        equity_df.columns = para_lambda_list
        performance_df.columns = para_lambda_list
        performance_df = performance_df.T
        
        #记录品种表现
        equity.name = cmt
        equity_cmt_list.append(equity)
        perf.name = cmt
        perf_cmt_list.append(perf)
        
        
        
        
        print cmt + "回测完毕"

    equity_strat = pd.concat(equity_cmt_list,axis=1)
    perf_strat = pd.concat(perf_cmt_list,axis=1).T











