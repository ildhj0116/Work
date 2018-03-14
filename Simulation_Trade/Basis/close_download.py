# -*- coding: utf-8 -*-
"""
Created on Thu Mar 08 08:42:01 2018

@author: Administrator

"""

from WindPy import w
import pandas as pd
w.start()

position = "ZC805.CZC,C1805.DCE,RU1805.SHF,TA805.CZC,BU1806.SHF,P1805.DCE,RM805.CZC,RB1805.SHF,J1805.DCE,Y1805.DCE"

date = "2018-03-13"

close = w.wsd(position, "close", date, date, "")
close = pd.DataFrame(close.Data,index=close.Fields,columns=close.Codes).T



