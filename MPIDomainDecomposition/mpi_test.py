# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 13:33:06 2016

@author: Laroy
"""

from Heat import Room
from scipy import ndimage
import matplotlib.pyplot as plt
from mpi4py import MPI
from numpy import *
print('hello')
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
a = Room(1,dx=1.0/3)
b = Room(2,dimy=2,dx=1.0/3)
c = Room(3,dx=1.0/3)
leftborder=zeros((a.dimxx,1))
rightborder=zeros((a.dimxx,1))
bound1=zeros((a.dimxx,1))
bound2=zeros((a.dimxx,1))
nbrIter=10

for i in range(nbrIter+1):
    if rank==2:#left room
        comm.Recv(ascontiguousarray(leftborder),source=0)
        a.border(leftborder)
        a.compute_func()
        bound1 = a.get_boundary()
        if i==nbrIter:
            comm.Send(a.matrice,dest=0)
        else:
            comm.Send(ascontiguousarray(bound1),dest=0)
        
    if rank==1:#right room
        comm.Recv(ascontiguousarray(rightborder),source=0)
        c.border(rightborder)        
        c.compute_func()
        bound2 = c.get_boundary()
        if i==nbrIter:
            comm.Send(c.matrice,dest=0)
        else:
            comm.Send(ascontiguousarray(bound2),dest=0)
        
    if rank==0:#big room
        if i==0:
            bound1=transpose(zeros((2,1)))
            print(bound1)
            bound2=transpose(zeros((2,1)))
        else:
            comm.Recv(bound1,source=2)
            comm.Recv(bound2,source=1)
        b.boundary(bound2,bound1)
        b.compute_func()
        boundaries=b.get_boundary()
        leftborder=boundaries[0]
        rightborder=boundaries[1]
        comm.Send(ascontiguousarray(leftborder),dest=2)
        comm.Send(ascontiguousarray(rightborder),dest=1)
        if i == nbrIter:
            print("done")
            comm.Recv(a.matrice,source=2)
            print(b.matrice)
            comm.Recv(a.matrice,source=1)
            plot_func()
        


def plot_func():
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
