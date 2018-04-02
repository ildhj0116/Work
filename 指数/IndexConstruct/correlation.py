# -*- coding: utf-8 -*-
"""
Created on Mon Apr 02 12:30:11 2018

@author: Administrator
"""

import pandas as pd
from datetime import datetime

def season(month):
    if month in [1,2,3]:
        return 1
    elif month in [4,5,6]:
        return 2
    elif month in [7,8,9]:
        return 3
    else:
        return 4


if __name__ == "__main__":
    smoothed_df = pd.read_csv("smoothed_main_cnt.csv", index_col=0, parse_dates=[0])
    corr = smoothed_df.corr()
    smoothed_df["month"] = [x.to_pydatetime().strftime("%Y-%m") for x in smoothed_df.index]
    smoothed_df["year"] = [x.to_pydatetime().year for x in smoothed_df.index]
    smoothed_df["season"] = [str(season(x.to_pydatetime().month)) for x in smoothed_df.index]
    smoothed_df["year_season"] = [str(x.to_pydatetime().year) + "_" + str(season(x.to_pydatetime().month)) for x in smoothed_df.index]
    corr_month = smoothed_df[["C.DCE","M.DCE"]].groupby(smoothed_df["month"]).corr()
    corr_month_new = corr_month.iloc[range(0,len(corr_month),2),1].copy()
    corr_month_new.index = [x[0] for x in corr_month_new.index.tolist()]
    corr_month_new.name = "corr_month"
    
    corr_season = smoothed_df[["C.DCE","M.DCE"]].groupby(smoothed_df["year_season"]).corr()
    corr_season_new = corr_season.iloc[range(0,len(corr_season),2),1].copy()
    corr_season_new.index = [x[0] for x in corr_season_new.index.tolist()]
    corr_season_new.name = "corr_season"
    
    corr_month_list = [x[-2:] for x in corr_month_new.index.tolist()]
    corr_month_list = pd.Series(corr_month_list,index=corr_month_new.index,name="month")
    corr_month_new = pd.concat([corr_month_new,corr_month_list],axis=1)
    month_corr_group = corr_month_new["corr_month"].groupby(corr_month_new["month"])
    month_list = []
    corr_month_list = []
    for name,group in month_corr_group:
        month_list.append(name)
        corr_month_list.append(group.mean())
    monthly_corr_mean = pd.Series(corr_month_list,index=month_list)
    
    corr_season_list = [x[-1] for x in corr_season_new.index.tolist()]
    corr_season_list = pd.Series(corr_season_list,index=corr_season_new.index,name="season")
    corr_season_new = pd.concat([corr_season_new,corr_season_list],axis=1)
    season_corr_group = corr_season_new["corr_season"].groupby(corr_season_new["season"])
    season_list = []
    corr_season_list = []
    for name,group in season_corr_group:
        season_list.append(name)
        corr_season_list.append(group.mean())
    seasonly_corr_mean = pd.Series(corr_season_list,index=season_list)
        
    
    
    
        