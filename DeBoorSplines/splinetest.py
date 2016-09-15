import CSplines as CS
from numpy import *
"""
    Testing environment for the Cubic Spline algorithm
"""

class dtest:
    def __init__(self):
        self.y = CS.CSplines(CS.spline()[1],CS.spline()[0])()[1]
        self.x = CS.CSplines(CS.spline()[1],CS.spline()[0])()[0]        
    
    def deriv(self):
        if len(self.x) == len(self.y):
            for i in range(0,len(self.x),8):
                left = polyfit(self.x[i:i+4],self.y[i:i+4],3)
                right = polyfit(self.x[i+4:i+8],self.y[i+4:i+8],3)
  
        else:
            return "x and y coordinates don't match"
        return False
            



class unittest:
    def __init__(self):
        return #
        
class nosetest:
    def __init__(self):
        return #     