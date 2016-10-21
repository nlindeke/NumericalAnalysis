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
#np=comm.size

#initial setup for rooms here
#-------------------------------------
nbrIter=int(sys.argv[1]) #command line argument
dx=float(sys.argv[2])
#print(nbrIter)
neumannLeft=zeros(1,dx)
neumannRight=zeros(1,dx)
dirichletLeft=zeros(1,dx)
dirichletRight=zeros(1,dx)
omega=0.8
#-------------------------------------

#iteration

#create the rooms
LeftRoom = Room(1,dx)  #left
MidRoom = Room(2,dx)   #mid
RightRoom = Room(3,dx) #right

for i in range(nbrIter):
    
    if rank is 0:
        comm.Recv(neumannLeft,source=1)
        LeftRoom.compute_func()
        tempLeft=LeftRoom
        tempLeft.border(neumannLeft.T)#!!! is the border even used anywhere?
        for i in range(0,tempLeft.dimyy):
            tempLeft[tempLeft.dimxx-1,i]=neumannLeft[i]
        tempLeft.compute_func()
        LeftRoom.matrice=omega*LeftRoom.matrice+(1-omega)*tempLeft.matrice#relax
        dirichletLeft=LeftRoom.get_boundary()#is this right?
        comm.Send(dirichletLeft,dest=1)
        
    if rank is 1:
        comm.Recv(dirichletLeft,source=0)
        comm.Recv(dirichletRight,source=2)
        
        MidRoom.compute_func
        tempMid=MidRoom
        
        
        if i is nbtIter-1: #end condition
            "plot and exit"
        else:
            comm.Send(neumannLeft,dest=0)
            comm.Send(neumannRight,dest=2)
        
    if rank is 2:
        comm.Recv(neumannRight,source=1)
        RightRoom.compute_func()
        tempRight=RightRoom
        tempRight.border(neumannRight.T)#!!!
        for i in range(0,tempRight.dimyy):
            tempRight[0,i]=neumannLeft[i]
        tempRight.compute_func()
        RightRoom.matrice=omega*RightRoom.matrice+(1-omega)*tempLeft.matrice#relax
        dirichletRight=RightRoom.get_boundary()#is this right?
        comm.Send(dirichletRight,dest=1)