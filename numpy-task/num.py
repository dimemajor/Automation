import numpy as np

coord = [] # list to store the coordinates of the rectangle
def create_rect(x,y):
    def new_point(arr, point): # generate a new points from previous point gotten 
        point = np.array(arr) * dim + point
        coord.append(point)
        return point

    point = np.random.randn(1, 2)
    coord.append(point)
    dim = np.array([x,y])
    point = new_point([1,0], point)
    point = new_point([0,1], point)
    point = new_point([-1,0], point)
    point = new_point([0,-1], point)

create_rect(3,4)
print(coord)