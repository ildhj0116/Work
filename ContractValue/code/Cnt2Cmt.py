# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 14:01:52 2018

@author: LHYM
"""

def Cnt2Cmt(contract):
    return ''.join([letter for letter in contract[:2] if letter.isalpha()])

