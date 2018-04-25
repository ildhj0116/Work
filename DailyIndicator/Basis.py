# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 10:58:25 2018

@author: Administrator
"""

import pandas as pd
from datetime import datetime

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

def Basis_Rate(tdate,main_cnt_df):
    spot = pd.read_excel("../Simulation_Trade/Basis/Basis_Table/"+tdate+".xlsm",sheetname=u"手动输入表",usecols=[1,3])    
    spot.index = [dic_cmt_chinese[x] for x in spot[u"品种"] if x in dic_cmt_chinese.keys()]
    cnt_list = []
    basis_rate_list = []
    tdate = datetime.strptime(tdate,"%Y-%m-%d")
    for cmt in spot.index.tolist():
        if cmt not in main_cnt_df.columns.tolist():
            print spot.iloc[:,0].loc[cmt] + u"不在活跃品种内"
            continue
        else:
            tmp_cl = pd.read_csv("../Futures_data/data_cl/"+cmt[:-4]+".csv", index_col=0, parse_dates=[0])
            main_cnt = main_cnt_df.loc[tdate,cmt]
            main_cl = tmp_cl.loc[tdate,main_cnt]
            basis_rate = float(spot.loc[cmt,u"收盘现货"]) / main_cl - 1
            cnt_list.append(main_cnt[:-4])
            basis_rate_list.append(basis_rate)
    basis_rate_series = pd.Series(basis_rate_list,index=cnt_list,name=u"基差贴水率").sort_values()
    return basis_rate_series

if __name__ == "__main__":
    main_cnt_df = pd.read_csv("../Futures_data/main_cnt/data/main_cnt_total.csv",index_col=0,parse_dates=[0])
    tdate = "2018-04-23"
    basis_rate_series = Basis_Rate(tdate,main_cnt_df)
    
    
    
    
    
    
    