# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 08:44:30 2017

对指定期货公司，根据之前的持仓情况总表计算该公司的持仓情况，并画图

@author: LHYM
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

def plot_oi_contract(company_openinterest, company_name,date,col_name, ylabel,variety=1,fig_num=1):
    # 根据输入内容画持仓情况图
    
    # 处理数据
    if variety==0:  # 若需要分合约处理
        position=pd.DataFrame(company_openinterest,columns=[col_name, 'variety', 'contract', 'month'])
        position.set_index([position['variety'],position['month']],inplace=True)
        position_plot=position[col_name].unstack().fillna(0)
        position_plot1=position['contract'].sort_index().unstack().fillna('0')
        position_plot = position_plot.loc[:, ['near', 'far']]
        cnt_list = position_plot1['near'].tolist()
        cnt_list.extend(position_plot1['far'].tolist())
    else:   #画品种总图
        position_plot = pd.DataFrame(company_openinterest,columns=[col_name])
    
    # 画图模块
    fig = plt.figure(fig_num)
    ax1 = fig.add_subplot(1,1,1)
    position_plot.plot(kind='bar',ax=ax1,rot=0)
    # 设置标题等内容
    mytitle = company_name + ylabel + '(' + date + ')'
    ax1.set_title(mytitle.decode("utf-8"))
    ax1.set_xlabel(u'品种')
    ax1.set_ylabel(ylabel.decode("utf-8"))
    # 标注合约名称(只有在画合约图时需要)
    if variety==0:
        cnt = 0
        tmp_label = []
        for p in ax1.patches:        
            if p.get_height() == 0:
                cnt+=1
                continue;
            else:
                ax1.annotate(cnt_list[cnt], (p.get_x() * 1.005, p.get_height() * 1.005))
                cnt+=1
                tmp_label.append(ax1.get_xticklabels())
    return
    


def company_oi_analysis(filename,company_name,date, variety=1):
    # 导入数据
    df = pd.read_csv('../output/'+filename, encoding = 'gbk',index_col=0)
    # 整理数据表格格式
    company = company_name.decode("utf-8")
    company_openinterest=df.loc[company]
    company_openinterest.index=company_openinterest[company_openinterest.columns[0]].tolist()
    del company_openinterest[company_openinterest.columns[0]]
    company_openinterest=company_openinterest.T.dropna(axis=0, how='all')
    list_order = range(0,2)+range(5,7)+range(2,5)+range(7,10)
    company_openinterest = company_openinterest.reindex(columns = \
                                                        company_openinterest.columns.values[list_order])
    company_openinterest.fillna(0)
    
    #如果涉及具体合约，需要单独处理：根据成交量选出每个品种最活跃的两个合约，并设为近远月
    if variety == 0:    
        # 将品种名提取出并设为一列
        company_openinterest['variety'] = [c[:2] if c[1].isalpha() else c[0] for c \
                             in company_openinterest.index.values]
        # 将合约简称提取并设为一列
        company_openinterest['contract'] = [c[:2]+c[-6:-4] if c[1].isalpha() else c[0]+c[-6:-4] for c \
                             in company_openinterest.index.values]
        # 在每个品种中，选出成交量最高的两个合约
        company_openinterest['oi_rank'] = np.abs(company_openinterest['net_position']).\
                                    groupby(company_openinterest['variety']).rank(ascending = False)                                
        company_openinterest = company_openinterest[company_openinterest['oi_rank']<=2]
        # 在这两个合约中，分出近月和远月，并列入原dataframe的新设列month中
        tmp_dict = {0:'near',1:'far'}
        for name, group in company_openinterest.groupby(company_openinterest['variety']):
            l=range(len(group))
            for i in l:
                company_openinterest.loc[group.index[i],'month'] = tmp_dict[i]
                
               
        
    ###########################################################################
    # 画图
    ###########################################################################

    plot_col_name_list = ['net_position', 'net_position_increase',
                          'net_position_rate','vol','vol_increase','vol_rate']
    title_name_list = ['净持仓量', '净持仓变化','净持仓占比(%)','成交量','成交量变化','成交量占比(%)']
    for fig_num in range(1,7):
        plot_oi_contract(company_openinterest,company_name,date,plot_col_name_list[fig_num-1],\
                title_name_list[fig_num-1],variety,fig_num)

    
    return company_openinterest



