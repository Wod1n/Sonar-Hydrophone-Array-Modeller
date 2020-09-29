# 2D Test Case

import antarray
import numpy as np
import matplotlib.pyplot as pyplt

test_array = antarray.LinearArray(4, 1)
theta = np.arange(-90, 90, 0.1)

test_array.toggle_panels([0,0])

print(test_array.get_pattern(theta)["weight"])

pyplt.plot(np.abs(test_array.get_pattern(theta)["array_factor"])**2)

pyplt.show()
