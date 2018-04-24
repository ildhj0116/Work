# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 17:13:10 2018

@author: Administrator
"""
import pandas as pd
from Trend import TriTrend
from Basis import Basis_Rate
from Spread import Spread
from Seasonal import Seasonal_Winning_Rate

dic_cmt_chinese = {
            u"焦炭":"J.DCE",
            u"焦煤":"JM.DCE",
            u"动力煤":"ZC.CZC",
            u"铁矿石":"I.DCE",
            u"螺纹钢":"RB.SHF",
            u"热卷":"HC.SHF",
            u"天胶":"RU.SHF",
            u"玻璃":"FG.CZC",
            u"PVC":"V.DCE",
            u"LLDPE":"L.DCE",
            u"PP":"PP.DCE",
            u"PTA":"TA.CZC",
            u"沥青":"BU.SHF",
            u"甲醇":"MA.CZC",
            u"豆一":"A.DCE",
            u"豆粕":"M.DCE",
            u"菜粕":"RM.CZC",
            u"玉米":"C.DCE",
            u"淀粉":"CS.DCE",
            u"豆油":"Y.DCE",
            u"棕榈油":"P.DCE",
            u"菜油":"OI.CZC",
            u"白糖":"SR.CZC",
            u"棉花":"CF.CZC",
            u"棉纱":"CY.CZC",
            u"铜":"CU.SHF",
            u"铝":"AL.SHF",
            u"锌":"ZN.SHF",
            u"镍":"NI.SHF",
            u"中证500":"IC.CFE",
            u"上证50":"IH.CFE",
            u"沪深300":"IF.CFE"
        }


def standarlize(series):
    std_series = (series * 2 - 1)/5
    return std_series.tolist()
    
    
    
if __name__ == "__main__":
    ma_param_df = pd.read_csv("parmt.csv",index_col=0)
    main_cnt_df = pd.read_csv("../Futures_data/main_cnt/data/main_cnt_total.csv",index_col=0,parse_dates=[0])
    tdate = "2018-04-23"
    trend = TriTrend(tdate,ma_param_df,main_cnt_df).sort_values()

    spot = pd.read_excel("../Simulation_Trade/Basis/Basis_Table/"+tdate+".xlsm",sheetname=u"手动输入表",usecols=[1,3])    
    spot.index = [dic_cmt_chinese[x] for x in spot[u"品种"] if x in dic_cmt_chinese.keys()]
    basis_rate_series = Basis_Rate(spot,tdate,main_cnt_df)
    
    spread_rate_series = Spread(main_cnt_df,tdate)
    
    seasonal_winrate = Seasonal_Winning_Rate(main_cnt_df,tdate)

    df = pd.concat([trend,basis_rate_series,spread_rate_series,seasonal_winrate], axis=1)
    
    
    df["basis"] = df[u"贴水率"].fillna(-10).copy()
    df["spread"] = (-df[u"价差贴水率"]).copy()
    df["std_season"] = standarlize(df[u"季节性胜率"])
    df["point"] = 0.4 * df["basis"] + 0.3 * df[u"价差贴水率"] + 0.3 * df["std_season"]
    df.sort_values(by=[u"日线趋势","point"],ascending=[True,False],inplace=True)
    df_final = df[[u"日线趋势",u"贴水率",u"价差贴水率",u"季节性胜率"]]
    df_final.to_csv("a.csv",encoding="gbk")



