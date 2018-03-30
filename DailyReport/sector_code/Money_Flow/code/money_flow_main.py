# -*- coding: utf-8 -*-
"""

计算每天成交量较大的合约的资金流向并输出

@author: LHYM
"""

from contracts import main_contracts
from get_data import get_data
from plot import PlotMoneyFlow
from water import add_watermark_to_image
#import pprint
from PIL import Image
import pandas as pd
import numpy as np


def money_flow_main(date,top_N,cmt_list):
    d=main_contracts(date,top_N)
    df_TopContractList = pd.DataFrame(d,index=1+np.arange(top_N)).T
   
    ## 计算资金流向
    df = get_data(date,df_TopContractList)
    df_g = df.groupby(df['commodity_name']).sum().reset_index()
    cmt_list.index = [x[:-4] for x in cmt_list.index.tolist()]
    df_g['commodity_name'] = cmt_list.loc[df_g['commodity_name'].tolist(),:]["Chinese"].tolist()
    ## 生成资金流向柱状图
    fig_list = PlotMoneyFlow(df_g,date)
    return fig_list





if __name__ == "__main__":
    ## 制作合约列表
    date = '2018-03-27'
    
    top = 2
    d=main_contracts(date,2)
    #pprint.pprint(d)
    df_TopContractList = pd.DataFrame(d,index=1+np.arange(top)).T
    df_TopContractList.to_csv('../output/TopContractList.csv', encoding = 'gb2312')
    print u"合约列表制作完毕"

    
    ## 计算资金流向
    df = get_data(date)
    df_g = df.groupby(df['commodity_name']).sum().reset_index()
    MoneyFlowFileName = '../output/MoneyFlow.csv'
    df_g.to_csv(MoneyFlowFileName, encoding = 'gb2312')
    print u"资金流向计算完毕"
  

    
    ## 生成资金流向柱状图
    image_name = PlotMoneyFlow(MoneyFlowFileName,date)
    print u"柱状图生成完毕"
    
    ## 加水印
    for image in image_name:
        im_before = Image.open('../output/'+image+".png")
        im_watermark = Image.open("../logo/Logo.jpg")
        im_after = add_watermark_to_image(im_before, im_watermark)
        watered_image_name = '../output/' + image + '(watered)'
        im_after.save(watered_image_name+".jpg")
    print u"水印添加完毕"    