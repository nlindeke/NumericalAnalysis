# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 13:14:24 2016

@author: Laroy
"""

#call with: mpiexec -n 3 python "pathToFile" arg1 arg2 ... argn


import Heat
from mpi4py import MPI
from numpy import *
from scipy import *
import sys


comm=MPI.COMM_WORLD
rank=comm.Get_rank()
np=comm.size

#initial setup for rooms here, I guess
nbrIter=sys.argv[1] #command line argument
#print(nbrIter)




#iteration
#the rooms get a "rank" in the setup like this:
#left=0
#mid=1
#right=2
for i in range(nbrIter):
    
    if rank is 0:
        comm.Recv(neumannLeft,source=1)
        #do stuff
        comm.Send(dirichletLeft,dest=1)
        
    if rank is 1:
        comm.Recv(dirichletLeft,source=0)
        comm.Recv(dirichletRight,source=2)
        #do stuff
        comm.Send(neumannLeft,dest=0)
        comm.Send(neumannRight,dest=2)
        
    if rank is 2:
        comm.Recv(neumannRight,source=1)
        #do stuff
        comm.Send(dirichletRight,dest=1)
        
    
