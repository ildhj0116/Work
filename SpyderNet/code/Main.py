# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 13:34:00 2018

@author: 李弘一萌
"""
import pandas as pd
from WindPy import w
from guppy import hpy; hp = hpy()
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
para_single_strat = False
#para_strat = "MTS"
para_strat = ("oi_factor",10)
para_strat_totaol_list = []
para_strat_totaol_list.extend(["ITS","UTS","MTS"])
para_strat_totaol_list.extend(zip(["oi_factor"]*10,range(1,11)))
para_strat_list = [para_strat] if para_single_strat else para_strat_totaol_list
                     


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
def Backtest_Main(strat_name,index,main_cnt,price_table,para_lambda=0,para_fee_rate=0,para_slippage=0):
    #产生指标

    #产生信号 
    signal = Signal_Generation_Main(strat_name,index,para_lambda)
    #######################################################################    
    #根据信号进行回测                
    bktest_result = OI_Strat_Bktest(signal,main_cnt,price_table,para_fee_rate,para_slippage)
    return bktest_result

def Equity2Ret(equity_series):
    equity_open = equity_series.shift(1)
    equity_open[0] = 1
    return (equity - equity_open) / equity_open


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
    cmt_oi_TopN_list = []
    total_oi_list = []
    for cmt in original_cmt_list:
        try:
            #导入指定品种主力合约会员持仓数据列表及当日该合约总持仓量列表
            cmt_oi,cmt_oi_TopN,total_vol_oi_df = OI_Data_Import(cmt)
        except IOError as e:
            #处理不存在该品种持仓数据的情况
            print cmt + "持仓数据导入失败: " + e.strerror            
        else:
            cmt_oi_list.append(cmt_oi)
            cmt_oi_TopN_list.append(cmt_oi_TopN)            
            effective_cmt_list.append(cmt)
            total_oi_list.append(total_vol_oi_df)
    print "价格及持仓数据导入完毕"
    oi_data = pd.DataFrame([cmt_oi_list,cmt_oi_TopN_list,total_oi_list],index=["oi_table","oi_TopN_table","total_oi"],\
                           columns=effective_cmt_list)

    ###########################################################################
    #逐品种回测
    strat_equity_list = []
    strat_perf_list = []
    for para_strat_name in para_strat_list:
        equity_cmt_list = []
        ret_cmt_list = []
        perf_cmt_list = []
        best_lambda_list = []
        
        for cmt in effective_cmt_list:
            #######################################################################
            #初始化各列表
            equity_series_list = []
            performance_series_list = []
            ret_series_list = []
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
            if (para_strat_name == "ITS") or (para_strat_name == "UTS") or (para_strat_name == "MTS"): 
                cmt_oi = oi_data.loc["oi_table",cmt]
            elif (type(para_strat_name) == tuple) and (para_strat_name[0]== "oi_factor"):
                cmt_oi = oi_data.loc["oi_TopN_table",cmt]
               
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
                ret_series_list.append(ret)
                performance_series_list.append(perf)        
                #print cmt + ": lambda=" + str(para_lambda) 

            #记录随lambda变化的净值及评价结果
            equity_df = pd.concat(equity_series_list,axis=1)
            ret_df = pd.concat(ret_series_list,axis=1)
            performance_df = pd.concat(performance_series_list,axis=1)
            equity_df.columns = para_lambda_list
            ret_df.columns = para_lambda_list
            performance_df.columns = para_lambda_list
            performance_df = performance_df.T
            

                
            #记录品种表现
            if para_lambda_optimize == True:
                best_lambda = performance_df["sharpe"].idxmax()
                equity = equity_df[best_lambda]
                ret = ret_df[best_lambda]
                perf = performance_df.loc[best_lambda]
                best_lambda_list.append(best_lambda)
            equity.name = cmt
            equity_cmt_list.append(equity)
            ret.name = cmt
            ret_cmt_list.append(ret)           
            perf.name = cmt
            perf_cmt_list.append(perf)                  
            print cmt + "回测完毕"
            
            h = hp.heap()
            print h
        
        equity_strat = pd.concat(equity_cmt_list,axis=1)
        ret_strat = pd.concat(ret_cmt_list,axis=1)       
        perf_strat = pd.concat(perf_cmt_list,axis=1).T
        best_lambda_series = pd.Series(best_lambda_list,index=effective_cmt_list)
        
        #计算等权配置品种后的策略净值和表现
        filter_cmt = perf_strat[perf_strat["annual_ret"]>0].index.tolist()
        filtered_equity = equity_strat.loc[:,filter_cmt]
        filtered_ret = ret_strat.loc[:,filter_cmt]
        weighted_equity = filtered_equity.apply(lambda x: x.mean(),axis=1)
        weighted_ret = filtered_ret.apply(lambda x: x.mean(),axis=1)
        weighted_perf = Performance_Main(weighted_equity,weighted_ret)
        weighted_equity.name = weighted_ret.name = weighted_perf.name = para_strat_name
        strat_equity_list.append(weighted_equity)
        strat_perf_list.append(weighted_perf)
        
        #
        
        
        #输出
        equity_strat.index = [x.date() for x in equity_strat.index]
        if (para_strat_name == "ITS") or (para_strat_name == "UTS") or (para_strat_name == "MTS"):
            strat_name = para_strat_name
        elif (type(para_strat_name) == tuple) and (para_strat_name[0]== "oi_factor"):
            strat_name = para_strat_name[0] + '_' + str(para_strat_name[1])
        """    
        if para_single_strat == True:
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
        """
        #print para_strat_name + "策略回测完毕"
        
        
        
        
    #生成策略总表
    
    equity_final = pd.concat(strat_equity_list,axis=1)    
    perf_final = pd.concat(strat_perf_list,axis=1)
    perf_final = perf_final.T
    equity_final.index = [x.date() for x in equity_final.index]
    if (para_strat_name == "ITS") or (para_strat_name == "UTS") or (para_strat_name == "MTS"):
        strat_name = para_strat_name
    elif (type(para_strat_name) == tuple) and (para_strat_name[0]== "oi_factor"):
        strat_name = para_strat_name[0] + '_' + str(para_strat_name[1])
    equity_final.name = perf_final.name = strat_name
    output_file_name = '../output/total_' + strat_name + '.xlsx'
    writer = pd.ExcelWriter(output_file_name)
    equity_final.to_excel(writer,'Equity')
    perf_final.to_excel(writer,'Performance')
    writer.save()
    
        
        
        
        
        
        
        




