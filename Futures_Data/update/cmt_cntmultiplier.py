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
        multiplier = 
        margin = 
    
    