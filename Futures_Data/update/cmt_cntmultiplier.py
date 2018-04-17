# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:29:37 2018

@author: Administrator
"""

from WindPy import w
w.start()
import pandas as pd

if __name__ == "__main__":
    cmt_list = pd.read_csv("../cmt_list/cmt_list.csv").iloc[:,0].values.tolist()
    for cmt in cmt_list:
        tmp_cl = pd.read_csv("../data_cl/"+cmt[:-4]+".csv",index_col=0)
        tmp_cl = tmp_cl.loc["2018-01-02":,:].copy()
        tmp_margin = pd.DataFrame(index=tmp_cl.index,columns=tmp_cl.columns)
        all_cnt_list = []
        for i in range(len(tmp_cl)):
            cnt_list = tmp_cl.iloc[i,:].dropna().index.tolist()
            all_cnt_list.append(cnt_list)
        effective_cnt_list = list(set(all_cnt_list[0]).union(*all_cnt_list[1:]))
        for cnt in effective_cnt_list:
            margin = w.wsd(cnt,"long_margin",tmp_margin.index[0],tmp_margin.index[-1])
            margin = pd.DataFrame(margin.Data,index=[cnt],columns=margin.Times).T
            tmp_margin[cnt] = margin[cnt].values
        tmp_margin.to_csv("../data_margin/" + cmt[:-4] + ".csv")