# -*- coding: utf-8 -*-
"""
Created on Thu Mar 08 08:42:01 2018

@author: Administrator

"""

from WindPy import w
import pandas as pd
w.start()

position = "C1805.DCE,FG805.CZC,RU1805.SHF,TA805.CZC,BU1806.SHF,JM1805.DCE,HC1805.SHF,RB1805.SHF,J1805.DCE,I1805.DCE"

date = "2018-04-13"

close = w.wsd(position, "close", date, date, "")
close = pd.DataFrame(close.Data,index=close.Fields,columns=close.Codes).T



