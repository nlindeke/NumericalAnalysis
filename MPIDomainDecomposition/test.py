from Heat import Room

a = Room(1)
b = Room(2,dimy=2)
c = Room(3)

a.compute_func()
c.compute_func()

bound1 = a.get_boundary()
bound2 = c.get_boundary()
b.boundary(bound2,bound1)


b.compute_func()
print(b.matrice)