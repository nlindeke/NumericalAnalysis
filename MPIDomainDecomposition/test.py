from Heat import Room
import matplotlib.pyplot as plt

a = Room(1,dx=1.0/30)
b = Room(2,dimy=2,dx=1.0/30)
c = Room(3,dx=1.0/30)
for i in range(10):
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
plt.imshow(a.matrice)
#plt.imshow(b.matrice)
#plt.imshow(c.matrice)