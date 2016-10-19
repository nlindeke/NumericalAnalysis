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
dx=int(sys.argv[2])
#print(nbrIter)
neumannLeft=zeros(1,dx)
neumannRight=zeros(1,dx)
dirichletLeft=zeros(1,dx)
dirichletRight=zeros(1,dx)
omega=0.8
#-------------------------------------

#iteration

#create the rooms
LeftRoom = Room(1)
LeftMatrix=LeftRoom.matrice #don't know if this is needed in here

MidRoom = Room(2)
MidMatrix=MidRoom.matrice

RightRoom = Room(3)
RightMatrix=RightRoom.matrice

for i in range(nbrIter):
    
    if rank is 0:
        comm.Recv(neumannLeft,source=1)
        LeftRoom=LeftRoom.compute_with_neu(neumannLeft,rank)#function that doesn't exist, but you get the idea
        dirichletLeft=LeftRoom.compute_dir(rank)
        comm.Send(dirichletLeft,dest=1)
        
    if rank is 1:
        comm.Recv(dirichletLeft,source=0)
        comm.Recv(dirichletRight,source=2)
        MidRoom=MidRoom.compute_with_neu(neumannLeft,neumannRight,rank)
        neumannLeft="compute the left side"
        neumannRight="compute the right side"
        comm.Send(neumannLeft,dest=0)
        comm.Send(neumannRight,dest=2)
        if i is nbtIter-1: #end condition
            "plot and exit"
        
    if rank is 2:
        comm.Recv(neumannRight,source=1)
        RightRoom=RightRoom.compute_neu(neumannRight,rank)
        dirichletRight=LeftRoom.compute_dir(rank)
        comm.Send(dirichletRight,dest=1)