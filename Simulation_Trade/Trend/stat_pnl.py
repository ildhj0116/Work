# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 14:03:40 2018

@author: Administrator
"""
import pandas as pd
import re

data_df = pd.read_excel('stat.xlsx')
data_df.dropna(inplace=True)
data_df["cmt"] = data_df["cnt"].apply(lambda x:re.sub("\d","",x)).tolist()
pnl = data_df["pnl"].groupby(data_df["cmt"])
count_total = pnl.count()
count_total.name = u"总交易次数"
p_num = []
n_num = []
p_sum_list = []
n_sum_list = []
cmt_list = []
sum_list = []
for name,group in pnl:
    p = group[group>=0].count()
    n = group[group<0].count()
    sum_num = group.sum()
    p_sum = group[group>=0].sum()
    n_sum = group[group<0].sum()
    p_num.append(p)
    n_num.append(n)
    cmt_list.append(name)
    sum_list.append(sum_num)
    p_sum_list.append(p_sum)
    n_sum_list.append(n_sum)
    
    
stat = pd.DataFrame([p_num,n_num,p_sum_list,n_sum_list,sum_list],index=[u"盈利交易数",u"亏损交易数",u"盈利总额",u"亏损总额",u"总盈亏"],columns=cmt_list).T
total_table = pd.concat([count_total,stat],axis=1)
total_table[u"总盈亏比率"] = total_table[u"总盈亏"] / 10000000
total_table[u"胜率"] = total_table[u"盈利交易数"] / total_table[u"总交易次数"]
total_table[u"盈亏比"] = total_table[u"盈利总额"] / total_table[u"亏损总额"]
total_table.sort_values(u"总盈亏",ascending=False,inplace=True)
total_table.to_excel("total_stat.xlsx")