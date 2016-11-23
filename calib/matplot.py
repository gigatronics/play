# plot camera calibration matrix
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import math

#quiver(0, 0, 0, )

#cam0

c0 = 1.899569921573962

cameraMatrix0 = [[  2.09568078e+03,   0.00000000e+00,   3.18214209e+02],
       [  0.00000000e+00,   5.57675417e+01,   2.46543834e+02],
       [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]]

distCoeffs0 = [ -2.78368880e-02,   8.55074262e-04,   2.67017819e-05,
         -6.04830887e-04,  -1.02104565e-05]

r0 = [-0.84594608, -0.6469101, 0.35012867]

t0 = [ 1.17171227, 8.57989453, 4.85995469]

x, y, z = -np.transpose(r0)*t0          # camera 0 position in the world view
print(x, y, z)#cam1

c1 =  0.9364567176844519

cameraMatrix1 = [[  2.09568078e+03,   0.00000000e+00,   3.18214209e+02],
       [  0.00000000e+00,   5.57675417e+01,   2.46543834e+02],
       [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]]

distCoeffs1 = [1.16612340e-02,  -8.26868898e-04,  -9.95864419e-03,
         -2.23300686e-04,   1.68891762e-05]

r1 = [-0.90066137, -1.29740651,  0.83682154]

t1 = [0.28185356, 30.44873529, 11.96919407]



u, v, w = -np.transpose(r1)*t1
print(u, v, w)

l1 = math.sqrt(x**2 + y**2 + z**2)
l2 = math.sqrt(u**2 + v**2 + w**2)
print('distances: ', l1 - l2)

v1 = (x, y, z)
v2 = (u, v, w)

theta = math.acos(np.dot(v1, v2)/(l1*l2))/math.pi*180 # in degrees
print('two vectors are seperated by: ', theta)

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.scatter(0, 0, 0)
ax.scatter(x, y, z)
ax.scatter(u, v, w)

plt.show()
