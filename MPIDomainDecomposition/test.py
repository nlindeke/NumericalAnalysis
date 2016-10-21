from Heat import Room
from scipy import ndimage
import matplotlib.pyplot as plt

a = Room(1,dx=1.0/30)
b = Room(2,dimy=2,dx=1.0/30)
c = Room(3,dx=1.0/30)
for i in range(2):
    a.compute_func()
    c.compute_func()
    
    bound1 = a.get_boundary()
    bound2 = c.get_boundary()
    b.boundary(bound2,bound1)
    
    
    b.compute_func()
    boundaries=b.get_boundary()
    a.border(boundaries[1])
    c.border(boundaries[0])
print(a.matrice)
print(b.matrice)
print(c.matrice)


def plot_func():
    """
    A plotting function for the heat distribution
    """
    #Rotated_Plot = ndimage.rotate(Your_Plot, 90)
    fig = plt.figure(figsize=(8,8))
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
