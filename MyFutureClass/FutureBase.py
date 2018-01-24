# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 08:12:21 2017

@author: LHYM
"""

from abc import ABCMeta, abstractmethod

class Future(object):
    # 抽象类
    __metaclass__ = ABCMeta
    
    # 构造函数
    def __init__(self, contract_name=''):
        self.__contract_name = contract_name
    
    # getters and setters
    @property
    def Variety(self):
        return  self.__con_variety
    
    @Variety.setter
    def Variety(self,v):
        self.__con_variety = v
        
    @property
    def Term(self):
        return self.__con_term    
    
    @Term.setter 
    def Term(self,t):
        self.__con_term = t
        
    @property
    def Exchange(self):
        return self.__con_exchange
        
    @Exchange.setter
    def Exchange(self,e):
        self.__con_exchange = e
        
    @property
    def Contract(self):
        return self.__contract_name
    
    @Contract.setter
    def Contract(self, c):
        self.__contract_name = c
    
    @property
    def Trade_Month(self):
        return self.__trade_month
    
    @Trade_Month.setter
    def Trade_Month(self, m):
        self.__trade_month = m
    
    @property
    def Active_Month(self):
        return self.__active_month
    
    @Active_Month.setter
    def Active_Month(self, m):
        self.__active_month = m
    
    @property
    def Multiplyer(self):
        return self.__multiplyer
    
    @Multiplyer.setter
    def Multiplyer(self, m):
        self.__multiplyer = m

    @property
    def Margin(self):
        return self.__margin
    
    @Margin.setter
    def Margin(self, m):
        self.__margin = m     

    @property
    def Category(self):
        return self.__category
    
    @Category.setter
    def Category(self, m):
        self.__category = m   

    @property
    def Main(self):
        return self.__main
    
    @Main.setter
    def Main(self, m):
        self.__main = m  

    @property
    def Name(self):
        return self.__name
    
    @Name.setter
    def Name(self, m):
        self.__name = m      
        
    # printer    
    def __str__(self):
        return self.Contract    
    
    @classmethod
    def all_variety(cls):
        aaa = []
        for sub_cls in cls.__subclasses__():
            aaa.append(sub_cls.variety)
        return aaa
        
    @classmethod
    def generate_main_contract(cls, date):
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    