import numpy as np 
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, CubicSpline

# 1D Array of Data points
x = np.array([1,6,7,9,12,20])
y = np.array([2,8,6,10,14,41])

x_interp = np.linspace(np.min(x),np.max(x),50)

# 1D linear spline Interpolation
y_linear = interp1d(x,y)
# 1D quadratic Spline interpolation
y_quadratic = interp1d(x,y, kind= "quadratic")
# 1D Cubic Spline Interpolation
y_cubic = interp1d(x,y, kind="cubic")
# 1D Cubic Spline Interpolation w/BC
y_cubicBC = CubicSpline(x,y,bc_type = "natural")
plt.plot(x,y,"o",label="Data Points")
plt.plot(x_interp,y_linear(x_interp),color ='red',label = "Linear Spline")
plt.plot(x_interp,y_quadratic(x_interp),color = "green", label="Quadratic Spline")
plt.plot(x_interp,y_cubic(x_interp),color="orange",label = "Cubic Spline")
plt.plot(x_interp,y_cubicBC(x_interp),color="black",label = "Cubic spline BC")

plt.legend()
plt.show()


