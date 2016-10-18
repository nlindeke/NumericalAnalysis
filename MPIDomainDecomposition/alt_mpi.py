# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 13:14:24 2016

@author: Laroy
"""
#To install mpi4py on windows with python 3.x:
#run conda install mpi4py in cmd, then download and run:
#http://www.microsoft.com/en-us/download/details.aspx?id=47259

#call with: mpiexec -n 3 python "pathToFile" arg1 arg2 ... argn


from Heat import Room
from mpi4py import MPI
from numpy import *
from scipy import *
import sys


comm=MPI.COMM_WORLD
rank=comm.Get_rank()
np=comm.size

#initial setup for rooms here
#-------------------------------------
nbrIter=int(sys.argv[1]) #command line argument
#print(nbrIter)
neumannLeft="some initial stuff"
neumannRight="some initial stuff"
dirichletLeft="some initial stuff"
dirichletRight="some initial stuff"
omega=0.8
#--------------------------------------

#iteration
#the rooms get a "rank" in the setup like this:
#left=0
#mid=1
#right=2
for i in range(nbrIter):
    status = MPI.Status()
    Recieve = comm.Recv(NeumannLeft,source=(rank-1)%np,status=status)
    #do some stuff wtih the conditions
    comm.send(dirichletLeft,(rank+1)%np,0)