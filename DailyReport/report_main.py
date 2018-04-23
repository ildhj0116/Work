# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 14:05:04 2018

@author: Administrator
"""

import sys
sys.path.append("./sector_code/Strength")
sys.path.append("./sector_code/Volatility")
sys.path.append("./sector_code/OI_Vol")
sys.path.append("./sector_code/Money_Flow/code")
sys.path.append("./sector_code/Total_Fund/code")
sys.path.append("./sector_code/Report_Generation")
import os
import copy
from NanHua import NanHua
from cmt_ret import cmt_ret_rank,cmt_ret_rank_date
from volatility import amplitude
from oi_indicator import vol_oi_indicator
from fund_main import fund_main,fund_main_local,fund_main_weekly,fund_main_date
from money_flow_main import money_flow_main,money_flow_local_main,money_flow_local_date_main
from report_generation import Report_Generation

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def output(mode,report_date,fig_list,title_list,head_df,tail_df):
    if mode == "day":
        if os.path.exists("output/Daily/" + report_date):
            print report_date + "已更新过，文件夹重复"
        else:
            os.makedirs("output/Daily/" + report_date)
            for i in range(len(fig_list)):
                title = title_list[i]
                fig = fig_list[i]
                fig.savefig("output/Daily/" + report_date + '/' + title + ".jpg",bbox_inches='tight')
            head_df.to_csv("output/Daily/" + report_date + '/' + "head.csv",encoding="utf_8_sig")
            tail_df.to_csv("output/Daily/" + report_date + '/' + "tail.csv",encoding="utf_8_sig")
    elif mode == "week":
        if os.path.exists("output/Weekly/" + report_date):
            print report_date + "已更新过，文件夹重复"
        else:
            os.makedirs("output/Weekly/" + report_date)
            for i in range(len(fig_list)):
                title = title_list[i]
                fig = fig_list[i]
                fig.savefig("output/Weekly/" + report_date + '/' + title + ".jpg",bbox_inches='tight')
            head_df.index = range(1,6)
            tail_df.index = range(1,6)                
            head_df = head_df[[u"5日收益",u"5日资金流向",u"5日资金流向变化率",u"20日收益",u"20日资金流向",u"20日资金流向变化率"]].T
            tail_df = tail_df[[u"5日收益",u"5日资金流向",u"5日资金流向变化率",u"20日收益",u"20日资金流向",u"20日资金流向变化率"]].T
            stat_df = pd.concat([head_df.apply(lambda x:",".join(x.tolist()),axis=1),tail_df.apply(lambda x:",".join(x.tolist()),axis=1)],
                                axis=1)
            stat_df.columns = [u"排名前五",u"排名后五"]
            
#            head_5_list = [head_df.loc[u"5日收益",:].tolist(),head_df.loc[u"5日资金流向",:].tolist(),head_df.loc[u"5日资金流向变化率",:].tolist()]
#            tail_5_list = [tail_df.loc[u"5日收益",:].tolist(),tail_df.loc[u"5日资金流向",:].tolist(),tail_df.loc[u"5日资金流向变化率",:].tolist()]
#            head_20_list = [head_df.loc[u"20日收益",:].tolist(),head_df.loc[u"20日资金流向",:].tolist(),head_df.loc[u"20日资金流向变化率",:].tolist()]
#            tail_20_list = [tail_df.loc[u"20日收益",:].tolist(),tail_df.loc[u"20日资金流向",:].tolist(),tail_df.loc[u"20日资金流向变化率",:].tolist()]
#            inter_5_head = list(set(head_5_list[0]).intersection(*head_5_list[1:]))
#            inter_5_tail = list(set(tail_5_list[0]).intersection(*tail_5_list[1:]))
#            inter_20_head = list(set(head_20_list[0]).intersection(*head_20_list[1:]))
#            inter_20_tail = list(set(tail_20_list[0]).intersection(*tail_20_list[1:]))
            stat_df.to_csv("output/Weekly/" + report_date + '/' + "stat.csv",encoding="utf_8_sig")
    elif mode == "one_date":
        if os.path.exists("output/One_Date/" + report_date):
            print report_date + "已更新过，文件夹重复"
        else:
            os.makedirs("output/One_Date/" + report_date)
            for i in range(len(fig_list)):
                title = title_list[i]
                fig = fig_list[i]
                fig.savefig("output/One_Date/" + report_date + '/' + title + ".jpg",bbox_inches='tight')
            head_df.index = range(1,6)
            tail_df.index = range(1,6)                
            head_df = head_df[[u"一季度收益",u"一季度资金流向",u"一季度资金流向变化率"]].T
            tail_df = tail_df[[u"一季度收益",u"一季度资金流向",u"一季度资金流向变化率"]].T
            stat_df = pd.concat([head_df.apply(lambda x:",".join(x.tolist()),axis=1),tail_df.apply(lambda x:",".join(x.tolist()),axis=1)],
                                axis=1)
            stat_df.columns = [u"排名前五",u"排名后五"]
            
           # head_5_list = [head_df.loc[u"一季度收益",:].tolist(),head_df.loc[u"一季度资金流向",:].tolist(),head_df.loc[u"一季度资金流向变化率",:].tolist()]
           # tail_5_list = [tail_df.loc[u"一季度收益",:].tolist(),tail_df.loc[u"一季度资金流向",:].tolist(),tail_df.loc[u"一季度资金流向变化率",:].tolist()]
           # inter_5_head = list(set(head_5_list[0]).intersection(*head_5_list[1:]))
           # inter_5_tail = list(set(tail_5_list[0]).intersection(*tail_5_list[1:]))
  
            stat_df.to_csv("output/One_Date/" + report_date + '/' + "stat.csv",encoding="utf_8_sig")


def delete_fig(figure_list):
    for fig in figure_list:
        plt.close(fig)

if __name__ == "__main__":
    
    cmt_daily_list = pd.read_csv("../Futures_Data/cmt_list/cmt_daily_list.csv")
    cmt_chinese = pd.read_csv("../Futures_Data/cmt_list/cmt_list_with_Chinese.csv",index_col=0,encoding = 'gb2312')
    cmt_list = cmt_chinese.loc[cmt_daily_list.loc[:,"cmt"].tolist(),:].copy()
    cmt_list.drop(["IC.CFE","IF.CFE","IH.CFE","T.CFE","TF.CFE"],inplace=True)
#    cmt_list = pd.DataFrame({"cmt":{"IC.CFE":"IC"}})
    main_cnt_df = pd.read_csv("../Futures_Data/main_cnt/data/main_cnt_total.csv",parse_dates=[0],index_col=0)

    mode = "day"
    # mode = "day"
    relative_data_path = "../Futures_Data"
    if mode == "day":
        title_list = ([u"品种日收益",u"品种周收益",u"品种月收益",u"品种日振幅",u"品种日增仓",u"品种日减仓",u"会员持仓占比",u"多头日占比变动",
                       u"多头周占比变动",u"多头月占比变动",u"空头日占比变动",u"空头周占比变动",u"空头月占比变动",u"板块沉淀资金",u"品种沉淀资金",
                       u"资金流向变动率",u"总资金流向",u"主动资金流向",u"被动资金流向"])
    elif mode == "week":
        title_list = ([u"品种日收益",u"品种周收益",u"品种月收益",u"板块沉淀资金",u"周资金流向变化率", u"周总资金流向",u"周主动资金流向",
                       u"周被动资金流向",u"月资金流向变化率",u"月总资金流向",u"月主动资金流向",u"月被动资金流向"])
    elif mode == "one_date":
        title_list = ([u"品种季度收益",u"板块沉淀资金",u"季度资金流向变化率", u"季度总资金流向",u"季度主动资金流向",u"季度被动资金流向"])

    report_date_list = pd.read_csv("../Futures_Data/others/trade_date.csv",index_col=0).index.tolist()
    report_date_list = report_date_list[-10:-5]
    for report_date in report_date_list:
        # report_date = "2018-04-16"
        report_date_time = datetime.strptime(report_date,"%Y-%m-%d")

        # 判断数据更新情况
        try:
            main_cnt_list_today = main_cnt_df.loc[report_date_time,:].copy()
        except:
            print "主力合约列表无更新日期数据，不能进行计算"
        else:
            fig_list = []

            head_df = pd.DataFrame()
            tail_df = pd.DataFrame()
            # 1、品种强弱
            #   (1)半年内南华商品指数价格折线图
            #   (2)半年内南华商品指数收益率折线图

            #   (3)各品种日、月、周收益率排名
            active_1 = 1
            if active_1 == 1:
                start_date = "2018-01-02"
                end_date = "2018-03-30"
                if mode == "one_date":
                    tmp_fig_list,tmp_head_df,tmp_tail_df = cmt_ret_rank_date(main_cnt_list_today,cmt_list,relative_data_path,
                                                                             start_date,end_date)
                else:
                    tmp_fig_list,tmp_head_df,tmp_tail_df = cmt_ret_rank(main_cnt_list_today,cmt_list,relative_data_path,report_date)
                head_df = pd.concat([head_df,tmp_head_df],axis=1)
                tail_df = pd.concat([tail_df,tmp_tail_df],axis=1)
                fig_list.extend(tmp_fig_list)

            # 2、波动率提示：品种日振幅
            active_2 = 1
            if active_2 == 1:
                if mode == "day":
                    N_list = [1]
                else:
                    N_list = []
                for N_days in N_list:
                    tmp_fig_list,head_df,tail_df = amplitude(main_cnt_list_today,N_days,cmt_list,report_date)
                    head_df = pd.concat([head_df,tmp_head_df],axis=1)
                    tail_df = pd.concat([tail_df,tmp_tail_df],axis=1)
                    fig_list.extend(tmp_fig_list)

            # 3、持仓、成交提示
            active_3 = 1
            if active_3 == 1:
                if mode == "day":
                    tmp_fig_list,tmp_head_df,tmp_tail_df = vol_oi_indicator(main_cnt_list_today,cmt_list,report_date,relative_data_path)
                    head_df = pd.concat([head_df,tmp_head_df],axis=1)
                    tail_df = pd.concat([tail_df,tmp_tail_df],axis=1)
                    fig_list.extend(tmp_fig_list)

            # 4、资金提示
            #   (1)沉淀资金
            active_4 = 1
            if active_4 == 1:
                start_date_fund = "2018-01-01"
                end_date = "2018-03-30"
                date_interval = 20
                if mode == "week":
                    tmp_fig_list = fund_main_weekly(start_date_fund,report_date,copy.deepcopy(cmt_list),date_interval)
                elif mode == "one_date":
                    tmp_fig_list = fund_main_date(start_date_fund,report_date,copy.deepcopy(cmt_list))
                elif mode == "day":
                   # tmp_fig_list = fund_main(start_date_fund,report_date,copy.deepcopy(cmt_list))
                    tmp_fig_list = fund_main_local(start_date_fund,report_date,copy.deepcopy(cmt_list),relative_data_path)
                fig_list.extend(tmp_fig_list)

            #   (2)资金流向
            active_5 = 1
            if active_5 == 1:
                top_N = 2
                start_date = "2018-01-02"
                if mode == "one_date":
                    end_date = "2018-03-30"
                else:
                    end_date = report_date

                if mode == "one_date":
                    tmp_fig_list,tmp_head_fund,tmp_tail_fund,tmp_head_chg,tmp_tail_chg = money_flow_local_date_main(start_date,end_date,
                                                                                                                    cmt_list,relative_data_path)
                    head_df = pd.concat([head_df,tmp_head_fund,tmp_head_chg],axis=1)
                    tail_df = pd.concat([tail_df,tmp_tail_fund,tmp_tail_chg],axis=1)
                else:
                    if mode == "week":
                        interval_list = [5,20]
                    else:
                        interval_list = [1]
                    for interval in interval_list:
                        #start_date_index = main_cnt_df.index.tolist().index(report_date_time) - interval
                        #start_date = main_cnt_df.index[start_date_index].strftime("%Y-%m-%d")

                        tmp_fig_list,tmp_head_fund,tmp_tail_fund,tmp_head_chg,tmp_tail_chg = money_flow_local_main(end_date,cmt_list,
                                                                                                                   interval,relative_data_path)
                        fig_list.extend(tmp_fig_list)
                        head_df = pd.concat([head_df,tmp_head_fund,tmp_head_chg],axis=1)
                        tail_df = pd.concat([tail_df,tmp_tail_fund,tmp_tail_chg],axis=1)


            # 输出
            active_output = 1
            if active_output == 1:
                output(mode,report_date,fig_list,title_list,head_df,tail_df)
                delete_fig(fig_list)

            #报告生成
            active_report = 0
            if active_report == 1:
                head_df = pd.read_csv("output/Daily/" + report_date + '/' + "head.csv",encoding="utf_8_sig",index_col=0)
                tail_df = pd.read_csv("output/Daily/" + report_date + '/' + "tail.csv",encoding="utf_8_sig",index_col=0)
                column_name_list = [u"1日收益",u"5日收益",u"20日收益",u"振幅",u"成交量变化",u"日多头持仓占比变化",u"日空头持仓占比变化",
                                  u"周多头持仓占比变化",u"周空头持仓占比变化",u"月多头持仓占比变化",u"月空头持仓占比变化"]
                head_value_list = head_df[column_name_list].T.values.tolist()
                tail_value_list = tail_df[column_name_list].T.values.tolist()
                path = "sector_code/Report_Generation/"
                Report_Generation(report_date,head_value_list,tail_value_list,title_list,path)
        
        print report_date + "量化日报生成完毕"
        
        
