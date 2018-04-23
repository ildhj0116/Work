# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:38:12 2018

@author: Administrator
"""

import pandas as pd


if __name__ == "__main__":
    head = pd.read_csv("head_all.csv",index_col=0,encoding="utf_8_sig")
    tail = pd.read_csv("tail_all.csv",index_col=0,encoding="utf_8_sig")
    for name,group in head.groupby(head.index):
        pass
    