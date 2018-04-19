# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 09:10:02 2018

@author: lihongyimeng

For handling Wind API download Errors 
"""



def WindCheck(wind_object):
    if wind_object.ErrorCode != 0:
        raise WindError(wind_object.ErrorCode)
    elif len(wind_object.Data) == 0:
        raise EmptyError()

class WindError(Exception):
    error_dict = {
                -40520001:"unknown error",
                -40520002:"inside error",
                -40520003:"system error",
                -40520004:"login failed",
                -40520005:"no authority",
                -40520006:"user cancelled",
                -40520007:"no data",
                -40520008:"timeout error", 
                -40520009:"local WBOX error",
                -40520010:"non-existed contents",
                -40520011:"non-existed server",
                -40520012:"non-existed reference",
                -40520013:"other place login error",
                -40520014:"login without WIM tool",
                -40520015:"too many failing logins",
                -40521001:"IO error",
                -40521002:"backend server unavailable",
                -40521003:"web connecting failed",
                -40521004:"requests sending failed",
                -40521005:"data receiving failed",
                -40521006:"web error",
                -40521007:"server rejected request",
                -40521008:"wrong response",
                -40521009:"data decoding error",
                -40521010:"web timeout",
                -40521011:"accept too frequently", 
                -40522001:"no legal response",
                -40522002:"illegal data service",
                -40522003:"illegal request",
                -40522004:"Wind grammar error", 
                -40522005:"unsupported Wind code",
                -40522006:"indicator grammar error",
                -40522007:"unsupported indicator",
                -40522008:"indicator param grammar error", 
                -40522009:"unsupported indicator param",
                -40522010:"date grammar error",
                -40522011:"unsupported date",
                -40522012:"unsupported request param",
                -40522013:"array index exceed",
                -40522014:"duplicate WQID",
                -40522015:"no authority for the requests",
                -40522016:"unsupported data type",
                -40522017:"quote exceed"                                     
            }
    def __init__(self,error_code):
        super(WindError,self).__init__()
        self.errorinfo = WindError.error_dict[error_code]
    
    def __str__(self):
        return self.errorinfo


class EmptyError(Exception):
    def __init__(self,err="empty data"):
        super(EmptyError,self).__init__()
        self.errorinfo = err
    
    def __str__(self):
        return self.errorinfo
    
    
    
    
if __name__ == "__main__":
#    raise WindError(-40522017)
#    print a1
#    a2 = a(0)
#    print a2.d
    print "Error"
    
    