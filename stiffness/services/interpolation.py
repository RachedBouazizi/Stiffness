import numpy as np
from scipy.interpolate import interp1d

# Define the data points
angles = np.array([20, 25, 30, 35, 40, 45])
a_values = np.array([2.399, 3.332, 4.565, 6.816, 10.959, 17.658])
b_values = np.array([0.439, 0.839, 1.234, 2.019, 1.783, 3.309])
c_values = np.array([-0.03, -0.09, -0.089, -0.146, 0.045, 0.048])
d_values = np.array([0.001059, 0.005606, 0.004275, 0.007651, -0.005425, -0.006443])
e_values = np.array([-0.00001754, -0.0001319, -0.00009159, -0.0001683, -0.0001153, -0.0001299])

# Create interpolation functions for each parameter

def get_interpolation_data():
    phi_range = np.arange(20, 46, 5)
    a_interpolated = np.interp(phi_range, angles, a_values)
    b_interpolated = np.interp(phi_range, angles, b_values)
    c_interpolated = np.interp(phi_range, angles, c_values)
    d_interpolated = np.interp(phi_range, angles, d_values)
    e_interpolated = np.interp(phi_range, angles, e_values)
    

    return  {
        'phi_range': phi_range.tolist(),
        'a': a_interpolated.tolist(),
        'b': b_interpolated.tolist(),
        'c': c_interpolated.tolist(),
        'd': d_interpolated.tolist(),
        'e': e_interpolated.tolist(),

    }

def interpolate_parameters(phi):
    if phi < 20 or phi > 45:
        raise ValueError("phi must be between 20 and 45 degrees")
    
    a_interpolated = np.interp(phi, angles, a_values)
    a_interpolated = round(float(a_interpolated), 3)
    b_interpolated = np.interp(phi, angles, b_values)
    b_interpolated = round(float(b_interpolated), 3)
    c_interpolated = np.interp(phi, angles, c_values)
    c_interpolated = round(float(c_interpolated), 3)
    d_interpolated = np.interp(phi, angles, d_values)
    # d_interpolated = round(float(d_interpolated), 3)
    e_interpolated = np.interp(phi, angles, e_values)
    # e_interpolated = round(float(e_interpolated), 3)    

    return a_interpolated, b_interpolated, c_interpolated, d_interpolated, e_interpolated

# Example usage: Interpolating for phi = 23°
# phi = 23
# a, b, c, d, e = interpolate_parameters(phi)

# print(f"Interpolated values for phi={phi}°:")
# print(f"a = {a}")
# print(f"b = {b}")
# print(f"c = {c}")
# print(f"d = {d}")
# print(f"e = {e}")
