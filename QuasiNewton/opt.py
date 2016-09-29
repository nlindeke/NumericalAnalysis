from numpy import *
from scipy import *
from itertools import *
import scipy.linalg as lin

def f(x):
    return (2*x[0]**3-10*x[1]**2)/(5-x[2]**2)
def f2(x):
    return 3*x[0][0]**4+2*x[0][1]**5
def f3(x):
    return (5*(x[0][0])**3)-(10*(x[0][1])**2)
def f4(x): #Rosenbrock function
    return (100(x[0][1]-x[0][0]**2)**2)+((1-x[0][0])**2)

    
class OPC:
    """
    Some stuff
    """
    def __init__(self, obj_func, gradis=None):
        self.obj_func = obj_func
        self.gradis = gradis
        self.h_glob = 10**(-3)
        
    def base_newton(self,xzero):
        x=self.listtoarray(xzero)
        termination_criterion=False
        k=0
        try:
            while termination_criterion!=True:
                k+=1
                x[0]=x[0]-self.NewtonDirection(x)
                if sum(x)<=0.0001 and sum(x)>=-0.0001:
                    termination_criterion=True
        except linalg.linalg.LinAlgError:
            return None
        return k
    
    def NewtonDirection(self,x):
        return array(transpose(matrix(self.InvHessian(x))*matrix(transpose(self.Gradient(x)))))
    def NewtonDirection2(self,x): #useless, besthessian should also be inverse, don't use
        return array(transpose(-1*matrix(self.besthessian(x))*matrix(transpose(self.Gradient(x)))))

    def InvHessian(self,x):
        return linalg.inv(self.besthessian(x))
       
    def Gradient(self,x):
        if self.gradis!=None:
            return self.gradis
        else:
            return self.grad(x)
            
    def dimgrid(self,dim,nbvalues=1000,step=1):
        A=zeros((nbvalues,dim))
        for i in range(dim):
            for j in range (nbvalues):
                A[j][i]=j*step
        return A
    def computefunc(self,nbvalues=1000,step=1):
        #We decide the dimension to be 2 for the time being
        f=self.obj_func
        matricevaleurs=zeros((nbvalues,nbvalues))
        for i in range(nbvalues):
            for j in range(nbvalues):
                matricevaleurs[i][j]=f(i*step,j*step)
        return matricevaleurs
    
    def grad(self,x):
        f=self.obj_func
        h=self.h_glob
        dim=len(x[0])
        e=identity(dim)
        arr=zeros((1,dim))
        for i in range(dim):
            arr[0][i]=(f(x+h*e[:][i])-f(x-h*e[:][i]))/(2*h)
        return arr

    def besthessian(self,x):
        f=self.obj_func
        h=self.h_glob
        dim=len(x[0])
        e=identity(dim)
        arr=empty((dim,dim))
        for i in range(dim):
            arr[i][:]=array(((self.grad(x+h*e[:][i])-self.grad(x-h*e[:][i]))/(2*h)))
        return arr

    def listtoarray(self,x):
        dim=len(x)
        matrice=zeros((1,dim))
        for i in range(dim):
            matrice[0][i]=x[i]
        return matrice
        
    def LineSearch(self,x,s):
        alfa_k=f(x+alfa*s)
        return minimize_scalar(alfa_k).x
        
        
    def InexactLineSearch(self,x,s,rho=0.1,sigma=0.7,tau=0.1,X=9):
        #x = self.listtoarray(xx)
        #s = -self.NewtonDirection(x)
        alfa_L=0 #define starting interval a_0 ∈ [a_L,a_U]
        alfa_U=10**9
        alfa_0=1
        d_alfa_0=0
        alfa_hat=0
        def f_a(x_in,s_in,alfa):
            return f3(x_in+alfa*s_in)
            
        def extrapolate(x_in,s_in,a_0,_a_L):
            temp =(f_der(x_in,s_in,_a_L)-f_der(x_in,s_in,a_0))
            if temp == 0:
                temp=0.000001
            return (a_0-_a_L)*(f_der(x_in,s_in,a_0)/temp)
            
        def interpolate(x_in,s_in,a_0,a_L):
            return ((a_0-a_L)**2)*f_der(x_in,s_in,a_L)/(2*(f_a(x_in,s_in,a_L)-f_a(x_in,s_in,a_0)*f_der(x_in,s_in,a_L)))
           
        def f_der(x_in,s_in,a_0):
            h=10**(-3)
            return (f_a(x_in+h,s_in,a_0)-f_a(x_in,s_in,a_0))/h

        LC = f_a(x,s,alfa_0)>=f_a(x,s,alfa_L)+(1-rho)*(alfa_0-alfa_L)*f_der(x,s,alfa_L)       
        RC = f_a(x,s,alfa_0)<=f_a(x,s,alfa_L)+rho*(alfa_0-alfa_L)*f_der(x,s,alfa_L)
        
        print(LC)
        print(RC)
        count=1
        alfa_old=0
        while not (LC and RC):
            if (not LC):
                d_alfa_0=extrapolate(x,s,alfa_0,alfa_L)
                d_alfa_0=max([d_alfa_0,tau*(alfa_0-alfa_L)])
                d_alfa_0=min([d_alfa_0,X*(alfa_0-alfa_L)])
                alfa_L=alfa_0
                alfa_0=alfa_0+d_alfa_0
                if abs(alfa_0-alfa_old)<0.0000001: #the change is fucking small, it drives me crazy, i don't know what's going on
                    break
                alfa_old=alfa_0
                #print("hello from IF ",str(f_a(x,s,alfa_0)))
                #print("LC alfa is: ",alfa_0)
                if count==1 or count ==100:
                    print("wat ",alfa_0)
                count=count+1
            else:
                alfa_U=min([alfa_0,alfa_U])
                alfa_hat=interpolate(x,s,alfa_0,alfa_L)
                alfa_hat=max([alfa_hat,alfa_L+tau*(alfa_U-alfa_L)])
                alfa_hat=min([alfa_hat,alfa_U-tau*(alfa_U-alfa_L)])
                alfa_0=alfa_hat
                print("hello from ELSE")
            LC=f_a(x,s,alfa_0)>=f_a(x,s,alfa_L)+(1-rho)*(alfa_0-alfa_L)*f_der(x,s,alfa_L)
            RC=f_a(x,s,alfa_0)<=f_a(x,s,alfa_L)+rho*(alfa_0-alfa_L)*f_der(x,s,alfa_L)
        return alfa_0,f_a(x,s,alfa_0)


class E(OPC):
    def __call__(self):
        return False
    
class IE(OPC):
    def __call(self):
        return False

class QN(OPC):
    def Iterate(self,guess,lineSearchVariant=None,UpdateVariant=None,NumOfIterations=None):
        if NumOfIterations==None:
            NumOfIterations=30
        def ChosenLineSearch(x,s):
            if lineSearchVariant=="exact":
                return self.ExactLineSearch(x,s)
            elif lineSearchVariant=="inexact":
                return self.InexactLineSearch(x,s)[0]
    
        def ChosenUpdate(iH,g,d):
            if UpdateVariant=="good":
                return GoodBroyden.Update(iH,g,d)
            elif UpdateVariant=="bad":
                return BadBroyden.Update(iH,g,d)
            elif UpdateVariant=="dfp":
                return DFP.Update(iH,g,d)
            elif UpdateVariant=="bfgs":
                return BFGS.Update(iH,g,d)
            else:
                print("Err")
        x=self.listtoarray(guess)
        invH=self.InvHessian(x)
        print("invH is: ",invH)
        print("bestHessian is: ",self.besthessian(x))
        print("inverse is: ",linalg.inv(self.besthessian(x)))
        counter=1
        for i in range(NumOfIterations):
            
            print("round: ",counter)
            grad=self.Gradient(x).T
            print("grad is: ",grad)
            s=-invH*grad #step 1
            print("x is: ",x," s is: ",s)
            alfa=ChosenLineSearch(x,s) #step 2
            print("alfa is: ",alfa)
            next_x=x+alfa*s #step 3
            delta=next_x-x
            next_grad=self.Gradient(next_x)
            gamma=next_grad-grad
            x=next_x #prepare for next iteration
            if(lin.norm(grad)<0.00001):
                return x
            invH=ChosenUpdate(invH,gamma,delta)# step 4: update the hessian
            print("updated invH is: ",invH)
            counter=counter+1
            print("grad is: ",grad)
        return x


class GoodBroyden(QN):
    #i think this works
    def Update(invH,gamma,delta):
        u=delta-dot(invH,gamma)
        u_T=u.T
        a=1/dot(u_T,gamma)
        H_k=invH+a*dot(u,u_T)
        return H_k
        
        
class BadBroyden(QN):
    def Update(invH,gamma,delta):
        #slide 54? straight codified version, anyway, does not work
        return invH+divide((gamma-invH*delta),(transpose(delta)*delta))*transpose(delta)
        
class BFGS(QN):
    def Update(invH,gamma,delta):
        return invH+(1+(transpose(gamma)*invH*gamma)/(transpose(delta)*gamma))*((delta*transpose(delta))/(transpose(delta)*gamma))\
        -(delta*transpose(delta)*invH+invH*gamma*transpose(delta))/(transpose(delta)*gamma)

class DFP(QN):
    def Update(invH,gamma,delta):
        return invH+((delta*transpose(delta))/(transpose(delta)*gamma))-((invH*gamma*transpose(gamma)*invH)/(transpose(gamma)*invH*gamma))
