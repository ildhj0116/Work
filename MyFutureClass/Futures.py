# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 09:29:30 2017

@author: LHYM
"""

from FutureBase import Future
from datetime import date, datetime

def str2term(cnt_name):
    digit = ''.join([d for d in cnt_name if d.isdigit()])
    day = 15
    month = int(digit[-2:])
    if len(digit) == 3:
        year = 2010 + int(digit[0])
    elif len(digit) == 4:
        year = 2000 +int(digit[:2])
    return date(year,month,day)

def my_init(m_self,contract_name):
    m_self.Exchange = m_self.exchange
    m_self.Variety = m_self.variety
    m_self.Trade_Month = m_self.month
    m_self.Active_Month = m_self.active
    m_self.Margin = m_self.margin
    m_self.Multiplyer = m_self.multiplyer
    m_self.Category = m_self.category
    m_self.Term = str2term(contract_name)
    m_self.Name = m_self.name

###############################################################################


class CU(Future):
    
    exchange = 'SHF'
    variety = 'CU'
    category = 'mental'
    name = '铜'
    main = True
    multiplyer = 10
    margin = 0.05
    month = range(1,13)
    active = range(1,13)
    
    def __init__(self, contract_name=''):
        super(A,self).__init__(contract_name)
        my_init(self,contract_name)


class AL(Future):
    
    exchange = 'SHF'
    variety = 'AL'
    category = 'mental'
    name = '铝'
    main = True
    multiplyer = 5
    margin = 0.03
    month = range(1,13)
    active = range(1,13)
    
    def __init__(self, contract_name=''):
        super(AL,self).__init__(contract_name)
        my_init(self,contract_name)        


class ZN(Future):
    
    exchange = 'SHF'
    variety = 'ZN'
    category = 'mental'
    name = '锌'
    main = True
    multiplyer = 5
    margin = 0.05
    month = range(1,13)
    active = range(1,13)
    
    def __init__(self, contract_name=''):
        super(ZN,self).__init__(contract_name)
        my_init(self,contract_name)        


class PB(Future):
    
    exchange = 'SHF'
    variety = 'PB'
    category = 'mental'
    name = '铅'
    main = False
    multiplyer = 5
    margin = 0.05
    month = range(1,13)
    active = range(1,13)

    def __init__(self, contract_name=''):
        super(PB,self).__init__(contract_name)
        my_init(self,contract_name)        

class NI(Future):
    
    exchange = 'SHF'
    variety = 'NI'
    category = 'mental'
    name = '镍'
    main = False
    multiplyer = 1
    margin = 0.05
    month = range(1,13)
    active = range(1,13)
    
    def __init__(self, contract_name=''):
        super(NI,self).__init__(contract_name)
        my_init(self,contract_name)        


class SN(Future):
    
    exchange = 'SHF'
    variety = 'SN'
    category = 'mental'
    name = '锡'
    main = False
    multiplyer = 1
    margin = 0.05
    month = range(1,13)
    active = range(1,13)
    
    def __init__(self, contract_name=''):
        super(SN,self).__init__(contract_name)
        my_init(self,contract_name)        


class AU(Future):
    
    exchange = 'SHF'
    variety = 'AU'
    category = 'gold'
    name = '金'
    main = True
    multiplyer = 1000
    margin = 0.04
    month = range(1,13)
    active = [6,12]
    
    def __init__(self, contract_name=''):
        super(AU,self).__init__(contract_name)
        my_init(self,contract_name)        


class AG(Future):
    
    exchange = 'SHF'
    variety = 'AG'
    category = 'gold'
    name = '银'
    main = True
    multiplyer = 15
    margin = 0.04
    month = range(1,13)
    active = [6,12]
    
    def __init__(self, contract_name=''):
        super(AG,self).__init__(contract_name)
        my_init(self,contract_name)        


class RB(Future):
    
    exchange = 'SHF'
    variety = 'RB'
    category = 'mental'
    name = '螺纹'
    main = True
    multiplyer = 10
    margin = 0.05
    month = range(1,13)
    active = [1,5,10]
    
    def __init__(self, contract_name=''):
        super(RB,self).__init__(contract_name)
        my_init(self,contract_name)        


class WR(Future):
    
    exchange = 'SHF'
    variety = 'WR'
    category = 'mental'
    name = '线材'
    main = False
    multiplyer = 10
    margin = 0.07
    month = range(1,13)
    active = []

    def __init__(self, contract_name=''):
        super(WR,self).__init__(contract_name)
        my_init(self,contract_name)        


class HC(Future):
    
    exchange = 'SHF'
    variety = 'HC'
    category = 'mental'
    name = '热卷'
    main = True
    multiplyer = 10
    margin = 0.05
    month = range(1,13)
    active = [1,5,10]

    def __init__(self, contract_name=''):
        super(HC,self).__init__(contract_name)
        my_init(self,contract_name)        


class FU(Future):
    
    exchange = 'SHF'
    variety = 'FU'
    category = 'energy'
    name = '燃油'
    main = False
    multiplyer = 50
    margin = 0.08
    month = range(1,13)
    active = []
    
    def __init__(self, contract_name=''):
        super(FU,self).__init__(contract_name)
        my_init(self,contract_name)        


class BU(Future):
    
    exchange = 'SHF'
    variety = 'BU'
    category = 'energy'
    name = '沥青'
    main = True
    multiplyer = 10
    margin = 0.04
    month = range(1,13)
    active = [6,9,12]

    def __init__(self, contract_name=''):
        super(BU,self).__init__(contract_name)
        my_init(self,contract_name)        


class RU(Future):
    
    exchange = 'SHF'
    variety = 'RU'
    category = 'chem'
    name = '天胶'
    main = True
    multiplyer = 10
    margin = 0.05
    month = [1,3,4,5,6,7,8,9,10,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(RU,self).__init__(contract_name)
        my_init(self,contract_name)        


class WH(Future):
    
    exchange = 'CZC'
    variety = 'WH'
    category = 'agri'
    name = '强麦'
    main = False
    multiplyer = 20
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(WH,self).__init__(contract_name)
        my_init(self,contract_name)        


class PM(Future):
    
    exchange = 'CZC'
    variety = 'PM'
    category = 'agri'
    name = '普麦'
    main = False
    multiplyer = 50
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(PM,self).__init__(contract_name)
        my_init(self,contract_name)        


class CF(Future):
    
    exchange = 'CZC'
    variety = 'CF'
    category = 'agri'
    name = '棉花'
    main = True
    multiplyer = 5
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(CF,self).__init__(contract_name)
        my_init(self,contract_name)        


class SR(Future):
    
    exchange = 'CZC'
    variety = 'SR'
    category = 'agri'
    name = '白糖'
    main = True
    multiplyer = 10
    margin = 0.06
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(SR,self).__init__(contract_name)
        my_init(self,contract_name)        


class OI(Future):
    
    exchange = 'CZC'
    variety = 'OI'
    category = 'agri'
    name = '菜油'
    main = True
    multiplyer = 10
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(OI,self).__init__(contract_name)
        my_init(self,contract_name)        


class RI(Future):
    
    exchange = 'CZC'
    variety = 'RI'
    category = 'agri'
    name = '早稻'
    main = False
    multiplyer = 20
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(RI,self).__init__(contract_name)
        my_init(self,contract_name)        


class RS(Future):
    
    exchange = 'CZC'
    variety = 'RS'
    category = 'agri'
    name = '菜籽'
    main = False
    multiplyer = 10
    margin = 0.05
    month = [7,8,9,11]
    active = []
    
    def __init__(self, contract_name=''):
        super(RS,self).__init__(contract_name)
        my_init(self,contract_name)        


class RM(Future):
    
    exchange = 'CZC'
    variety = 'RM'
    category = 'agri'
    name = '菜粕'
    main = True
    multiplyer = 10
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(RM,self).__init__(contract_name)
        my_init(self,contract_name)        


class JR(Future):
    
    exchange = 'CZC'
    variety = 'JR'
    category = 'agri'
    name = '粳稻'
    main = False
    multiplyer = 20
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(JR,self).__init__(contract_name)
        my_init(self,contract_name)        


class LR(Future):
    
    exchange = 'CZC'
    variety = 'LR'
    category = 'agri'
    name = '晚稻'
    main = False
    multiplyer = 20
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = []
    
    def __init__(self, contract_name=''):
        super(LR,self).__init__(contract_name)
        my_init(self,contract_name)        


class CY(Future):
    
    exchange = 'CZC'
    variety = 'CY'
    category = 'agri'
    name = '棉纱'
    main = False
    multiplyer = 5
    margin = 0.05
    month = range(1,13)
    active = []
    
    def __init__(self, contract_name=''):
        super(CY,self).__init__(contract_name)
        my_init(self,contract_name)        


class TA(Future):
    
    exchange = 'CZC'
    variety = 'TA'
    category = 'chem'
    name = 'PTA'
    main = True
    multiplyer = 5
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(TA,self).__init__(contract_name)
        my_init(self,contract_name)        


class MA(Future):
    
    exchange = 'CZC'
    variety = 'MA'
    category = 'chem'
    name = '甲醇'
    main = True
    multiplyer = 10
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(MA,self).__init__(contract_name)
        my_init(self,contract_name)        


class FG(Future):
    
    exchange = 'CZC'
    variety = 'FG'
    category = 'chem'
    name = '玻璃'
    main = True
    multiplyer = 20
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(FG,self).__init__(contract_name)
        my_init(self,contract_name)        


class ZC(Future):
    
    exchange = 'CZC'
    variety = 'ZC'
    category = 'mental'
    name = '动力煤'
    main = True
    multiplyer = 100
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(ZC,self).__init__(contract_name)
        my_init(self,contract_name)        


class SF(Future):
    
    exchange = 'CZC'
    variety = 'SF'
    category = 'mental'
    name = '硅铁'
    main = True
    multiplyer = 5
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]

    def __init__(self, contract_name=''):
        super(SF,self).__init__(contract_name)
        my_init(self,contract_name)        


class SM(Future):
    
    exchange = 'CZC'
    variety = 'SM'
    category = 'mental'
    name = '锰硅'
    main = True
    multiplyer = 5
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(SM,self).__init__(contract_name)
        my_init(self,contract_name)        


class C(Future):
    
    exchange = 'DCE'
    variety = 'C'
    category = 'agri'
    name = '玉米'
    main = True
    multiplyer = 10
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(C,self).__init__(contract_name)
        my_init(self,contract_name)        

class CS(Future):
    
    exchange = 'DCE'
    variety = 'CS'
    category = 'agri'
    name = '玉米淀粉'
    main = True
    multiplyer = 10
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(CS,self).__init__(contract_name)
        my_init(self,contract_name)   


class A(Future):
    
    exchange = 'DCE'
    variety = 'A'
    name = '豆一'
    category = 'agri'
    main = True
    multiplyer = 10
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(A,self).__init__(contract_name)
        my_init(self,contract_name)

        
class B(Future):
    
    exchange = 'DCE'
    variety = 'B'
    category = 'agri'
    name = '豆二'
    main = False
    multiplyer = 10
    margin = 0.05
    month = [1,3,5,7,9,11]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(B,self).__init__(contract_name)
        my_init(self,contract_name)   
                
class M(Future):
    
    exchange = 'DCE'
    variety = 'M'
    category = 'agri'
    name = '豆粕'
    main = True
    multiplyer = 10
    margin = 0.05
    month = [1,3,5,7,8,9,11,12]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(M,self).__init__(contract_name)
        my_init(self,contract_name)   
        
class Y(Future):
    
    exchange = 'DCE'
    variety = 'Y'
    category = 'agri'
    name = '豆油'
    main = True
    multiplyer = 10
    margin = 0.05
    month = [1,3,5,7,8,9,11,12]
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(Y,self).__init__(contract_name)
        my_init(self,contract_name)   
        
class P(Future):
    
    exchange = 'DCE'
    variety = 'P'
    category = 'agri'
    name = '棕榈油'
    main = True
    multiplyer = 10
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(P,self).__init__(contract_name)
        my_init(self,contract_name)   
        
class FB(Future):
    
    exchange = 'DCE'
    variety = 'FB'
    category = 'agri'
    name = '纤维板'
    main = False
    multiplyer = 500
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(FB,self).__init__(contract_name)
        my_init(self,contract_name)   

class BB(Future):
    
    exchange = 'DCE'
    variety = 'BB'
    category = 'agri'
    name = '胶合板'
    main = False
    multiplyer = 500
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(BB,self).__init__(contract_name)
        my_init(self,contract_name)   
        
class JD(Future):
    
    exchange = 'DCE'
    variety = 'JD'
    category = 'agri'
    name = '鸡蛋'
    main = True
    multiplyer = 10
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(JD,self).__init__(contract_name)
        my_init(self,contract_name)   
        
class L(Future):
    
    exchange = 'DCE'
    variety = 'L'
    category = 'chem'
    name = '聚乙烯'
    main = True
    multiplyer = 5
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(L,self).__init__(contract_name)
        my_init(self,contract_name)   
        
class V(Future):
    
    exchange = 'DCE'
    variety = 'V'
    category = 'chem'
    name = '聚氯乙烯'
    main = True
    multiplyer = 5
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(V,self).__init__(contract_name)
        my_init(self,contract_name)   

class PP(Future):
    
    exchange = 'DCE'
    variety = 'PP'
    category = 'chem'
    name = '聚丙烯'
    main = True
    multiplyer = 5
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(PP,self).__init__(contract_name)
        my_init(self,contract_name)   
        
class J(Future):
    
    exchange = 'DCE'
    variety = 'J'
    category = 'chem'
    name = '焦炭'
    main = True
    multiplyer = 100
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(J,self).__init__(contract_name)
        my_init(self,contract_name)   
        
class JM(Future):
    
    exchange = 'DCE'
    variety = 'JM'
    category = 'chem'
    name = '焦煤'
    main = True
    multiplyer = 60
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(JM,self).__init__(contract_name)
        my_init(self,contract_name)   
        
class I(Future):
    
    exchange = 'DCE'
    variety = 'I'
    category = 'chem'
    name = '铁矿石'
    main = True
    multiplyer = 100
    margin = 0.05
    month = range(1,13)
    active = [1,5,9]
    
    def __init__(self, contract_name=''):
        super(I,self).__init__(contract_name)
        my_init(self,contract_name)   
        
class IF(Future):
    
    exchange = 'CFE'
    variety = 'IF'
    category = 'finance'
    name = '300'
    main = True
    multiplyer = 300
    margin = 0.08
    month = []
    active = []
    
    def __init__(self, contract_name=''):
        super(C,self).__init__(contract_name)
        my_init(self,contract_name)   

class IC(Future):
    
    exchange = 'CFE'
    variety = 'IC'
    category = 'finance'
    name = '50'
    main = True
    multiplyer = 200
    margin = 0.08
    month = []
    active = []
    
    def __init__(self, contract_name=''):
        super(IC,self).__init__(contract_name)
        my_init(self,contract_name)   
                                
class IH(Future):
    
    exchange = 'CFE'
    variety = 'IH'
    category = 'finance'
    name = '500'
    main = True
    multiplyer = 300
    margin = 0.08
    month = []
    active = []
    
    def __init__(self, contract_name=''):
        super(IH,self).__init__(contract_name)
        my_init(self,contract_name)   
                                
class TF(Future):
    
    exchange = 'CFE'
    variety = 'TF'
    category = 'finance'
    name = '5年'
    main = True
    multiplyer = 1
    margin = 0.01
    month = []
    active = []
    
    def __init__(self, contract_name=''):
        super(TF,self).__init__(contract_name)
        my_init(self,contract_name)   
                                
class T(Future):
    
    exchange = 'CFE'
    variety = 'T'
    category = 'finance'
    name = '10年'
    main = True
    multiplyer = 1
    margin = 0.02
    month = []
    active = []
    
    def __init__(self, contract_name=''):
        super(T,self).__init__(contract_name)
        my_init(self,contract_name)   
                                                                