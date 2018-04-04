# -*- coding: utf-8 -*-
"""

计算每天成交量较大的合约的资金流向并输出

@author: LHYM
"""

from contracts import main_contracts
from get_data import get_data,get_data_local
from plot import PlotMoneyFlow
from water import add_watermark_to_image
#import pprint
from PIL import Image
import pandas as pd
import numpy as np


def money_flow_main(date,top_N,cmt_list,interval=1):
    d=main_contracts(date,top_N)
    df_TopContractList = pd.DataFrame(d,index=1+np.arange(top_N)).T
   
    ## 计算资金流向
    df = get_data(date,df_TopContractList)
    df_g = df.groupby(df['commodity_name']).sum().reset_index()
    cmt_list.index = [x[:-4] for x in cmt_list.index.tolist()]
    df_g['commodity_name'] = cmt_list.loc[df_g['commodity_name'].tolist(),:]["Chinese"].tolist()
    ## 生成资金流向柱状图
    name_of_date = date + str(interval) + u"日"
    fig_list = PlotMoneyFlow(df_g,date,name_of_date)
    return fig_list

def money_flow_local_main(start_date,end_date,cmt_list,interval,relative_data_path):
    
   
#    ## 计算资金流向
#    df = get_data(date,df_TopContractList)
#    df_g = df.groupby(df['commodity_name']).sum().reset_index()
#    cmt_list.index = [x[:-4] for x in cmt_list.index.tolist()]
#    df_g['commodity_name'] = cmt_list.loc[df_g['commodity_name'].tolist(),:]["Chinese"].tolist()
#    ## 生成资金流向柱状图
    fig_list = []
    passive_list = []
    active_list = []
    total_list = []
    pct_chg_list = []
    
    for cmt in cmt_list.index.tolist():
        tmp_cl = pd.read_csv(relative_data_path + "/data_cl/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0) #相对地址有问题
        tmp_oi = pd.read_csv(relative_data_path + "/data_oi/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0) 
        tmp_passive, tmp_active, tmp_total, tmp_pct_chg = get_data_local(start_date,end_date,cmt,tmp_cl,tmp_oi)
        passive_list.append(tmp_passive)
        active_list.append(tmp_active)
        total_list.append(tmp_total)
        pct_chg_list.append(tmp_pct_chg)
        
    fund_df = pd.DataFrame([total_list,active_list,passive_list,pct_chg_list],index=["total_fund","active_fund","passive_fund","fund_chg"],
                            columns=cmt_list.index).T
    fund_df["commodity_name"] = cmt_list.loc[fund_df.index.tolist(),:]["Chinese"].tolist()
    fund_df = fund_df[["commodity_name","passive_fund","active_fund","total_fund","fund_chg"]]
    head_fund_list = fund_df.sort_values(by=["total_fund"],ascending=False).head().loc[:,"commodity_name"].tolist()
    tail_fund_list = fund_df.sort_values(by=["total_fund"],ascending=False).tail().loc[:,"commodity_name"].tolist()
    head_fund_series = pd.Series(head_fund_list,name=str(interval) + u"日资金流向")
    tail_fund_series = pd.Series(tail_fund_list,name=str(interval) + u"日资金流向")
    head_chg_list = fund_df.sort_values(by=["fund_chg"],ascending=False).head().loc[:,"commodity_name"].tolist()
    tail_chg_list = fund_df.sort_values(by=["fund_chg"],ascending=False).tail().loc[:,"commodity_name"].tolist()
    head_chg_series = pd.Series(head_chg_list,name=str(interval) + u"日资金流向变化率")
    tail_chg_series = pd.Series(tail_chg_list,name=str(interval) + u"日资金流向变化率")
    name_of_date = date + str(interval) + u"日"
    fig_list = PlotMoneyFlow(df_g,date,name_of_date)
    return fig_list,head_fund_series,tail_fund_series,head_chg_series,tail_chg_series

def money_flow_local_date_main(start_date,end_date,cmt_list,relative_data_path):
    
   
#    ## 计算资金流向
#    df = get_data(date,df_TopContractList)
#    df_g = df.groupby(df['commodity_name']).sum().reset_index()
#    cmt_list.index = [x[:-4] for x in cmt_list.index.tolist()]
#    df_g['commodity_name'] = cmt_list.loc[df_g['commodity_name'].tolist(),:]["Chinese"].tolist()
#    ## 生成资金流向柱状图
    fig_list = []
    passive_list = []
    active_list = []
    total_list = []
    pct_chg_list = []
    
    for cmt in cmt_list.index.tolist():
        tmp_cl = pd.read_csv(relative_data_path + "/data_cl/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0) #相对地址有问题
        tmp_oi = pd.read_csv(relative_data_path + "/data_oi/"+cmt[:-4]+".csv",parse_dates=[0],index_col=0) 
        tmp_passive, tmp_active, tmp_total, tmp_pct_chg = get_data_local(start_date,end_date,cmt,tmp_cl,tmp_oi)
        passive_list.append(tmp_passive)
        active_list.append(tmp_active)
        total_list.append(tmp_total)
        pct_chg_list.append(tmp_pct_chg)
        
    fund_df = pd.DataFrame([total_list,active_list,passive_list,pct_chg_list],index=["total_fund","active_fund","passive_fund","fund_chg"],
                            columns=cmt_list.index).T
    fund_df["commodity_name"] = cmt_list.loc[fund_df.index.tolist(),:]["Chinese"].tolist()
    fund_df = fund_df[["commodity_name","passive_fund","active_fund","total_fund","fund_chg"]]
    head_fund_list = fund_df.sort_values(by=["total_fund"],ascending=False).head().loc[:,"commodity_name"].tolist()
    tail_fund_list = fund_df.sort_values(by=["total_fund"],ascending=False).tail().loc[:,"commodity_name"].tolist()
    head_fund_series = pd.Series(head_fund_list,name=u"一季度资金流向")
    tail_fund_series = pd.Series(tail_fund_list,name=u"一季度资金流向")
    head_chg_list = fund_df.sort_values(by=["fund_chg"],ascending=False).head().loc[:,"commodity_name"].tolist()
    tail_chg_list = fund_df.sort_values(by=["fund_chg"],ascending=False).tail().loc[:,"commodity_name"].tolist()
    head_chg_series = pd.Series(head_chg_list,name=u"一季度资金流向变化率")
    tail_chg_series = pd.Series(tail_chg_list,name=u"一季度资金流向变化率")
    fig_list = PlotMoneyFlow(fund_df,end_date,u"一季度")
    return fig_list,head_fund_series,tail_fund_series,head_chg_series,tail_chg_series

if __name__ == "__main__":
    ## 制作合约列表
    date = '2018-03-29'
    
    top = 2
#    d=main_contracts(date,2)
#    #pprint.pprint(d)
#    df_TopContractList = pd.DataFrame(d,index=1+np.arange(top)).T
#    df_TopContractList.to_csv('../output/TopContractList.csv', encoding = 'gb2312')
#    print u"合约列表制作完毕"

#    
#    ## 计算资金流向
#    df = get_data(date)
#    df_g = df.groupby(df['commodity_name']).sum().reset_index()
#    MoneyFlowFileName = '../output/MoneyFlow.csv'
#    df_g.to_csv(MoneyFlowFileName, encoding = 'gb2312')
#    print u"资金流向计算完毕"
#  
#
#    
#    ## 生成资金流向柱状图
#    image_name = PlotMoneyFlow(MoneyFlowFileName,date)
#    print u"柱状图生成完毕"
#    
#    ## 加水印
#    for image in image_name:
#        im_before = Image.open('../output/'+image+".png")
#        im_watermark = Image.open("../logo/Logo.jpg")
#        im_after = add_watermark_to_image(im_before, im_watermark)
#        watered_image_name = '../output/' + image + '(watered)'
#        im_after.save(watered_image_name+".jpg")
#    print u"水印添加完毕"   
    
    
    
    