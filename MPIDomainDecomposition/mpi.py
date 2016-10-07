# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 13:14:24 2016

@author: Laroy
"""
import Heat
from mpi4py import MPI
from numpy import *
from scipy import *
import sys


comm=MPI.COMM_WORLD
rank=comm.Get_rank()
np=comm.size

#initial setup for rooms here, I guess
nbrIter=sys.argv[1]
print(nbrIter)


#iteration
#the rooms get a "rank" in the setup like this:
#left=0
#mid=1
#right=2
for i in range(nbrIter):
    
    if rank is 0:
        comm.Recv(neumannLeft,source=1)
        
    if rank is 1:
        comm.Recv(dirichletLeft,source=0)
        comm.Recv(dirichletRight,source=2)
        
    if rank is 2:
        comm.Recv(neumannRight,source=1)
        
    
