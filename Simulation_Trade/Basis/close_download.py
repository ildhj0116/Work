# -*- coding: utf-8 -*-
"""
Created on Thu Mar 08 08:42:01 2018

@author: Administrator

"""

from WindPy import w
import pandas as pd
w.start()

position = "C1805.DCE,FG805.CZC,RU1805.SHF,TA805.CZC,ZC805.CZC,P1805.DCE,RM805.CZC,RB1805.SHF,SR805.CZC,Y1805.DCE"

date = "2018-03-27"

close = w.wsd(position, "close", date, date, "")
close = pd.DataFrame(close.Data,index=close.Fields,columns=close.Codes).T



