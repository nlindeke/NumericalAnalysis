#3rd Project in Advanced Numerical Algorithms
#Charles Rohart, Laroy Sjödahl, Ingrid Odlen and Niklas Lindeke

from Heat import Room
from scipy import ndimage
import matplotlib.pyplot as plt
from mpi4py import MPI
from numpy import *
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
#rooms---------------------
a = Room(1,dx=1.0/20)
b = Room(2,dimy=2,dx=1.0/20)
c = Room(3,dx=1.0/20)
#--------------------------

#initiate the variables used
leftborder=zeros((a.dimxx,1))
rightborder=zeros((a.dimxx,1))
bound1=zeros((a.dimxx,1))
bound2=zeros((a.dimxx,1))
nbrIter=10
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

#Iteration
for i in range(nbrIter+1):
    if rank==2:#left room
        leftborder=comm.recv(source=0)
        temp=a
        temp.border(leftborder)
        temp.compute_func()
        a.compute_func()
        a.matrice=omega*a.matrice+(1-omega)*temp.matrice #relaxation
        bound1 = a.get_boundary()
        if i==nbrIter:#for plotting
            comm.send(a.matrice,dest=0)
        else:
            comm.send(bound1,dest=0)
        
    if rank==1:#right room
        rightborder=comm.recv(source=0)
        temp=c
        temp.border(rightborder)
        temp.compute_func()
        c.compute_func()
        c.matrice=omega*c.matrice+(1-omega)*temp.matrice #relaxation
        bound2 = c.get_boundary()
        if i==nbrIter:#for plotting
            comm.send(c.matrice,dest=0)
        else:
            comm.send(bound2,dest=0)
        
    if rank==0:#big room
        if i==0:
            bound1=transpose(zeros((9,1)))
            bound2=transpose(zeros((9,1)))
        else:
            bound1=comm.recv(source=2)
            bound2=comm.recv(source=1)
        temp=b
        temp.boundary(bound2,bound1)
        temp.compute_func()
        b.compute_func()
        b.matrice=omega*b.matrice+(1-omega)*temp.matrice #relaxation
        boundaries=b.get_boundary()
        leftborder=boundaries[1]
        rightborder=boundaries[0]
        comm.send(leftborder,dest=2)
        comm.send(rightborder,dest=1)
        if i == nbrIter:#collect the other rooms and plot
            a.matrice=comm.recv(source=2)
            c.matrice=comm.recv(source=1)
            plot_func(a.matrice,b.matrice,c.matrice)
        



