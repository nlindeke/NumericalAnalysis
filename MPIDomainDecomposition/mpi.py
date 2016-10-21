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


print("hello from mpi")
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
#np=comm.size

#initial setup for rooms here
#-------------------------------------
#nbrIter=int(sys.argv[1]) #command line argument
#dx=float(sys.argv[2])
#print(nbrIter)
nbrIter=10
idx=1/30.0
neumannLeft=zeros([int(1/idx-1),1])
neumannRight=zeros([int(1/idx-1),1])
dirichletLeft=zeros([int(1/idx-1),1])
dirichletRight=zeros([int(1/idx-1),1])
omega=0.8
#-------------------------------------

#iteration

#create the rooms
LeftRoom = Room(1,dx=idx)  #left
MidRoom = Room(2,dimy=2,dx=idx)   #mid
RightRoom = Room(3,dx=idx) #right

for i in range(nbrIter):
    
    if rank is 0:
        print("hello from left")
        comm.Recv(neumannLeft,source=1)
        LeftRoom.compute_func()
        tempLeft=LeftRoom
        #tempLeft.border(neumannLeft.T)#!!! is the border even used anywhere?
        for i in range(0,LeftRoom.dimyy):
            LeftRoom[LeftLeft.dimxx-1,i]=neumannLeft[i]
        LeftRoom.compute_func()
        LeftRoom.matrice=omega*LeftRoom.matrice+(1-omega)*tempLeft.matrice#relax
        dirichletLeft=LeftRoom.get_boundary()[0]#is this right?
        comm.Send(ascontiguousarray(dirichletLeft),dest=1)
        
    if rank is 1:
        print("hello from mid")
        comm.Recv(dirichletLeft,source=0)
        comm.Recv(dirichletRight,source=2)
        
        MidRoom.compute_func
        tempMid=MidRoom
        MidRoom.boundary(dirichletLeft,dirichletRight)
        MidRoom.compute_func()
        MidRoom=omega*MidRoom.matrice+(1-omega)*tempMid.matrice
        boundaries=MidRoom.get_boundary()
        neumannLeft=boundaries[0]
        neumannRight=boundaries[1]
        
        if i is nbtIter-1: #end condition
            plot_func(LeftRoom,MidRoom,RightRoom)
        else:
            comm.Send(ascontiguousarray(neumannLeft),dest=0)
            comm.Send(ascontiguousarray(neumannRight),dest=2)
        
    if rank is 2:
        print("hello from right")
        comm.Recv(neumannRight,source=1)
        RightRoom.compute_func()
        tempRight=RightRoom
        #tempRight.border(neumannRight.T)#!!!
        for i in range(0,RightRoom.dimyy):
            tempRightRoom[0,i]=neumannRight[i]
        RightRoom.compute_func()
        RightRoom.matrice=omega*RightRoom.matrice+(1-omega)*tempRight.matrice#relax
        dirichletRight=RightRoom.get_boundary()[0]#is this right?
        comm.Send(ascontiguousarray(dirichletRight),dest=1)

def plot_func(a,b,c):
    """
    A plotting function for the heat distribution
    """
    #Rotated_Plot = ndimage.rotate(Your_Plot, 90)
    fig = plt.figure(figsize=(6,5))
    st = fig.suptitle("AFB's Worst Nightmare", fontsize="x-large")

    ax1 = fig.add_subplot(131)
    img = plt.imshow(a.matrice)
    plt.axis('off')
    ax2 = fig.add_subplot(132)
    img = plt.imshow(b.matrice)
    plt.axis('off')
    ax2 = fig.add_subplot(133)
    img = plt.imshow(c.matrice)
    plt.axis('off')
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()