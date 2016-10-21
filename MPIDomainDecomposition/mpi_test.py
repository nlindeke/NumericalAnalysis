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

comm=MPI.COMM_WORLD
rank=comm.Get_rank()
a = Room(1,dx=1.0/30)
b = Room(2,dimy=2,dx=1.0/30)
c = Room(3,dx=1.0/30)
leftborder=zeros((a.dimyy,1))
rightborder=zeros((a.dimyy,1))
bound1=zeros((a.dimyy,1))
bound2=zeros((a.dimyy,1))

for i in range(10):
    
    if rank==0:#left room
        a.border(comm.recv(leftborder,source=2))
        a.compute_func()
        bound1 = a.get_boundary()
        comm.send(bound1,dest=2)
        
    if rank==1:#right room
        c.border(comm.recv(rightborder,source=2))
        c.compute_func()
        bound2 = c.get_boundary()
        comm.send(bound2,dest=2)
        
    if rank==2:#big room
        bound1=comm.recv(bound1,source=0)
        bound2=comm.recv(bound2,source=1)
        b.boundary(bound2,bound1)
        b.compute_func()
        boundaries=b.get_boundary()
        leftborder=boundaries[0]
        rightborder=boundaries[1]
        comm.send(leftborder,dest=0)
        comm.send(rightborder,dest=1)
        if i == 9:
            plot_func(a,b,c)
        


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
