# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 14:14:56 2018

@author: Administrator
"""
import pandas as pd
agri_cmt=['A','C','CS','M','Y','P','JD','CF','SR','OI','RM']
chem_cmt=['L','PP','V','TA','MA','BU','RU']
fmt_cmt=['RB','I','HC','J','JM','ZC','FG']
nfmt_cmt=['CU','NI','AL','ZN','SN','SF']
gld_cmt=['AU','AG']
index_cmt=['IC','IH','IF','T','TF']

def Cnt2Cmt(contract):
    return ''.join([letter for letter in contract[:2] if letter.isalpha()])
def cmtclass(cmt):
    if cmt in agri_cmt:
        return u"农产品"
    elif cmt in chem_cmt:
        return u"化工"
    elif cmt in fmt_cmt:
        return u"黑色"
    elif cmt in nfmt_cmt:
        return u"有色"    
    elif cmt in gld_cmt:
        return u"贵金属"    
    elif cmt in index_cmt:
        return u"金融"    
    
    
    
code_df = pd.read_excel('SimulationTrading_test.xlsx',sheetname='stat',encoding = 'gb2312')
cmt = code_df[u"合约"].apply(Cnt2Cmt)
classification = cmt.apply(cmtclass)
classification.name = u"板块"
code_df = pd.concat([code_df,classification],axis=1).fillna(0)
code_df['total_PNF'] = code_df[u'盈亏'] + code_df[u'持仓盈亏']
code_df.sort_index(by=[u'板块', u'合约', u'盈亏', u'开仓日'],inplace=True)
code_df = code_df[[u'板块',u'合约',u'开仓',u'开仓日',u'开仓价',u'平仓日',u'平仓价',u'乘数',
                   u'盈亏',u'收盘价',u'持仓盈亏', u'total_PNF']]
pnf_by_cnt = code_df['total_PNF'].groupby([code_df[u'板块'],code_df[u'合约']]).sum()

#code_df.to_excel("result.xlsx")




