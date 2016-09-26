from numpy import *
from scipy import *

class OPC:
    """
    Some stuff
    """
    
    def __init__(self, obj_func, grad=None):
        self.obj_func = obj_func
        self.grad = grad
    
    class QN(OPC):
        def __call__(self):
            return False
    
    class E:
        def __call__(self):
            return False
        
    class IE:
        def __call(self):
            return False
        
    