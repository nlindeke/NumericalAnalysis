import CSplines as CS
from numpy import *
"""
    Testing environment for the Cubic Spline algorithm
"""

class dtest:
    """
        Test class devised to investigate the relationship of the first and second derivative
        between two adjacent points
    """
    def __init__(self):
        self.y = CS.CSplines(CS.spline()[1],CS.spline()[0])()[1]
        self.x = CS.CSplines(CS.spline()[1],CS.spline()[0])()[0]        
    
    def deriv(self):
        """
            Testing the Cubic Spline property f''i-1(xi) = f''i(xi)
        """
        if len(self.x) == len(self.y):
            for i in range(0,len(self.x)-8,8):
                # Assuming Polyfit Returns  the vector containing [Ax^3 + Bx^2 + Cx + D] as [ A B C D]
                left = polyfit(self.x[i:i+4],self.y[i:i+4],3)
                right = polyfit(self.x[i+4:i+8],self.y[i+4:i+8],3)
                
                first_left = left * [3,2,1,0]
                first_right = right * [3,2,1,0]
                second_left = first_left * [2,1,0,0] 
                second_right = first_right * [2,1,0,0]
                x = self.x[i:i+4]
                
                for j in range(0,len(x),1):
                    # righteval should be equal to lefteval if this prperty holds
                    righteval = x[j]*second_right[0] + second_right[1]*x[j]
                    lefteval = x[j]*second_left[0] + second_left[1]*x[j]
                    if righteval == lefteval:
                        return "Property 2 holds"
                    #print(righteval)
                    #print(lefteval)
            return "Does not seem to hold"
  
        else:
            return "x and y coordinates don't match"

class speed:
    """
        tests the overall speed of __call__, 
        I think would be the easiest to use 
        when testing different versions of functions
    """
    def testAlgoSpeed(self):

        a=array([])
        c=CS.CSplines(CS.spline()[1],CS.spline()[0])
        for i in range(30):
            c.tic()
            c()
            a=append(a,c.toc())
        average=0
        Tsum=0
        for i in range(30):
            Tsum+=a[i]
        average=Tsum/30
        print("Average time over ",str(30)," tries is: ",str(average))  