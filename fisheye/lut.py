import numpy as np
import math

radius = 240

def lut(radius):
    dict = {}
    i = np.arange(1, radius) #, dtype=int)
    j = np.arange(1, radius*4) #], dtype=int)

    for j in range(int(radius)):
        for i in range(int(4*radius)):
            R = radius - j
            theta = - 2.0 * math.pi * i / (4.0 * radius) + math.pi/2        # starts at bottom of img.. pi/2 shifts the rectlinear to the right

            x = int( (R * math.cos(theta)) + radius )
            y = radius - int( R * math.sin(theta) )

            dict2 = {(i, j):(x, y)}
            dict.update(dict2)
    return dict
    np.save('lut.npy', dict)


if __name__ =="__main__":

    dict = lut(240)
#    print(dict)
#    list(dict.keys())
    print(sorted(dict.keys()))
    print(dict[(1,200)], dict[(200, 200)], dict[(200, 1)])
    #print(dict[(0,0)])
