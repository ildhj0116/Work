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
para_lambda_optimize = True
para_lambda_best = False
if para_lambda_optimize == True:
    para_lambda_list = [x/100.0 for x in range(-100,100)]
else:
    if para_lambda_best == False:
        para_lambda_list = [0]
    else:
        para_lambda_list = [0]

#是否测单独合约
para_cmt_single = False
para_cmt = ["MA.CZC"]   #单独测试的品种
print "部分测试模式，品种为:" + ",".join(para_cmt) if para_cmt_single == True else "全部测试"

#手续费
para_fee = False
para_fee_rate = 2.0/10000 if para_fee == True else 0

#滑点
para_index_cost = False
para_slippage = 1


#策略名称
#para_strat_name = "UTS"
para_strat_name = ("oi_factor",10)

#持仓因子回测窗口
para_r = 1

#持仓因子排名前N位
para_n = 5


###############################################################################
#持仓数据导入
def OI_Data_Import(strat_name,cmt):
    #导入指定品种主力合约会员持仓数据列表
    if (strat_name == "ITS") or (strat_name == "UTS") or (strat_name == "MTS"):
        cmt_oi = pd.read_pickle("../OI_Data/OI_" + cmt[:-4] + ".tmp")
    elif (type(strat_name) == tuple) and (strat_name[0]== "oi_factor"):
        cmt_oi = pd.read_pickle("../OI_TopN_Data/OI_" + cmt[:-4] + ".tmp")
    
    #导入指定品种主力合约日总持仓量数据
    total_vol_oi_df = pd.read_csv("../OI_Data/OI_total_"+ cmt[:-4] +".csv",parse_dates=[0],index_col=0)
    return cmt_oi,total_vol_oi_df


###############################################################################
#回测及优化模块
def Backtest_Main(strat_name,index,main_cnt,price_table,para_lambda=0,para_fee_rate=0,para_slippage=0):
    #产生指标

    #产生信号 
    signal = Signal_Generation_Main(strat_name,index,para_lambda)
    #######################################################################    
    #根据信号进行回测                
    bktest_result = OI_Strat_Bktest(signal,main_cnt,price_table,para_fee_rate,para_slippage)
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
            cmt_oi,total_vol_oi_df = OI_Data_Import(para_strat_name,cmt)
        except IOError as e:
            #处理不存在该品种持仓数据的情况
            print cmt + "持仓数据导入失败: " + e.strerror            
        else:
            cmt_oi_list.append(cmt_oi)
            effective_cmt_list.append(cmt)
            total_oi_list.append(total_vol_oi_df)
    print "价格及持仓数据导入完毕"
    oi_data = pd.DataFrame([cmt_oi_list,total_oi_list],index=["oi_table","total_oi"],columns=effective_cmt_list)
    
    ###########################################################################
    #逐品种回测
    equity_cmt_list = []
    perf_cmt_list = []
    best_lambda_list = []
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
        
        #产生信号
        index = Signal_Index_Generation_Main(para_strat_name,cmt_oi,total_oi,para_r,para_n)
        #开始回测
        for para_lambda in para_lambda_list:            
            bk_result = Backtest_Main(para_strat_name,index,main_cnt_df[cmt],price_table,para_lambda,para_fee_rate,para_slippage)
            equity = bk_result["equity"]
            ret = bk_result["ret"]            
            perf = Performance_Main(equity,ret)
            equity_series_list.append(equity)
            performance_series_list.append(perf)        
            print cmt + ": lambda=" + str(para_lambda) 
        
        #记录随lambda变化的净值及评价结果
        equity_df = pd.concat(equity_series_list,axis=1)
        performance_df = pd.concat(performance_series_list,axis=1)
        equity_df.columns = para_lambda_list
        performance_df.columns = para_lambda_list
        performance_df = performance_df.T
                        
        #记录品种表现
        if para_lambda_optimize == True:
            best_lambda = performance_df["sharpe"].idxmax()
            equity = equity_df[best_lambda]
            perf = performance_df.loc[best_lambda]
            best_lambda_list.append(best_lambda)
        equity.name = cmt
        equity_cmt_list.append(equity)
        perf.name = cmt
        perf_cmt_list.append(perf)    
        print cmt + "回测完毕"
    
    
    equity_strat = pd.concat(equity_cmt_list,axis=1)
    perf_strat = pd.concat(perf_cmt_list,axis=1).T
    best_lambda_series = pd.Series(best_lambda_list,index=effective_cmt_list)
    
    #输出
    equity_strat.index = [x.date() for x in equity_strat.index]
    if (para_strat_name == "ITS") or (para_strat_name == "UTS") or (para_strat_name == "MTS"):
        strat_name = para_strat_name
    elif (type(para_strat_name) == tuple) and (para_strat_name[0]== "oi_factor"):
        strat_name = para_strat_name[0] + '_' + str(para_strat_name[1])
    
    if para_lambda_optimize == False:
        output_file_name = '../output/' + strat_name + '(lambda=' + str(para_lambda) + ').xlsx'
    else:
        output_file_name = '../output/' + strat_name + '_optimized(lambda).xlsx'

    writer = pd.ExcelWriter(output_file_name)
    equity_strat.to_excel(writer,'Equity')
    perf_strat.to_excel(writer,'Performance')
    if para_lambda_optimize == True:    
        best_lambda_series.to_excel(writer,'Lambda') 
    writer.save()









