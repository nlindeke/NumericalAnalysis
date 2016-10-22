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
nbrIter=1
omega=0.8
def plot_func(x,y,z):
    """
    A plotting function for the heat distribution
    """
    #Rotated_Plot = ndimage.rotate(Your_Plot, 90)
    fig = plt.figure(figsize=(6,5))
    st = fig.suptitle("AFB's Worst Nightmare", fontsize="x-large")

    ax1 = fig.add_subplot(131)
    img = plt.imshow(x)
    plt.axis('off')
    ax2 = fig.add_subplot(132)
    img = plt.imshow(y)
    plt.axis('off')
    ax2 = fig.add_subplot(133)
    img = plt.imshow(z)
    plt.axis('off')
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()

for i in range(nbrIter+1):#+1 to allow for initial boundary setup from large room
    if rank==2:#left room
        comm.Recv(ascontiguousarray(leftborder),source=0)
        temp=a
        temp.border(leftborder)
        temp.compute_func()
        a.compute_func()
        a.matrice=omega*a.matrice+(1-omega)*temp.matrice #relaxation
        bound1 = a.get_boundary()
        if i==nbrIter:
            comm.Send(a.matrice,dest=0)
        else:
            comm.Send(ascontiguousarray(bound1),dest=0)
        
    if rank==1:#right room
        comm.Recv(ascontiguousarray(rightborder),source=0)
        temp=c
        temp.border(rightborder)
        temp.compute_func()
        c.compute_func()
        c.matrice=omega*c.matrice+(1-omega)*temp.matrice #relaxation
        bound2 = c.get_boundary()
        if i==nbrIter:
            comm.Send(c.matrice,dest=0)
        else:
            comm.Send(ascontiguousarray(bound2),dest=0)
        
    if rank==0:#big room
        print("hello from BIG, i is: ",i)
        if i==0:
            bound1=transpose(zeros((2,1)))
            bound2=transpose(zeros((2,1)))
        else:
            comm.Recv(bound1,source=2)
            comm.Recv(bound2,source=1)
        temp=b
        temp.boundary(bound2,bound1)
        temp.compute_func()
        b.compute_func()
        b.matrice=omega*b.matrice+(1-omega)*temp.matrice #relaxation
        boundaries=b.get_boundary()
        leftborder=boundaries[1]
        rightborder=boundaries[0]
        comm.Send(ascontiguousarray(leftborder),dest=2)
        comm.Send(ascontiguousarray(rightborder),dest=1)
        if i == nbrIter:
            print(b.matrice)
            comm.Recv(a.matrice,source=2)
            comm.Recv(c.matrice,source=1)
            plot_func(a.matrice,b.matrice,c.matrice)
        



