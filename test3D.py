# Test case

import antarray
import numpy as np
import matplotlib.pyplot as pyplt
from mpl_toolkits import mplot3d
from matplotlib import cm

test_array = antarray.RectArray(4, 4)
#theta = np.arange(-180, 180, 0.1)

x = np.linspace(0, 10, 512)
y = np.linspace(0, 10, 512)

xgrid, ygrid = np.meshgrid(x,y)

fig = pyplt.figure()
ax = pyplt.axes(projection='3d')

failed_coordinates = ([0,0], [0,1], [0,2], [0,3])
print(len(failed_coordinates))

test_array.toggle_panels(failed_coordinates)

ax.contour3D(xgrid, ygrid, np.abs(test_array.get_pattern()["array_factor"]), 50, rstride=1, cstride=1,
    cmap=cm.coolwarm, linewidth=0, antialiased=False)

print(test_array.get_pattern()["weight"])

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z');

ax.view_init(60, 35)
pyplt.show()
