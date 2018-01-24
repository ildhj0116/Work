# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 12:33:12 2017
主函数
@author: LHYM
"""
import sys
sys.path.append("./utils")
from contract_oi_compute import generate_contract_table
from variety_oi_compute import generate_variety_table
from generate_company_oi import company_oi_analysis
import pandas as pd


if __name__ == "__main__":
    # 本文件用于计算date当天指定期货公司在所有品种上的持仓情况
    
    ## 设置参数
    date = "2017-12-18" # 日期，不能是非交易日（可以设置异常处理）
    company_name = '永安期货' #会员名称（可以设置异常处理）
    variety = 0 # 0表示具体到近月远月合约， 1表示只计算每个品种总的持仓情况
    
    #生成date当天所有公司所有品种或合约的持仓情况列表
    if variety==0:
        oi_filename = generate_contract_table(date,date) #这里两个参数表示起始和终止日，但设为只下载一天
    else:
        oi_filename = generate_variety_table(date,date)
        
    
    # 根据上一步得到的table，提取某一指定公司持仓情况，生成统计图及表格
    company_oi = company_oi_analysis(oi_filename, company_name, date, variety) 
    output_filename = '../output/' + company_name + "品种持仓(" + date + ")" + '.csv'
    # 特定公司持仓品种情况公司保存
    company_oi.to_csv(output_filename.decode("utf-8") , encoding = 'gbk')
    
    

