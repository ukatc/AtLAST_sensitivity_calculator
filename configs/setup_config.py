import astropy.units as u
import numpy as np

def get_Tspl(Tspl):
    raise NotImplementedError

def get_dish_area(radius):
    area = np.pi * radius**2
    return area



surface_rms = 25 * u.micron
dish_area = get_dish_area(25 * u.m)
T_spl = get_Tspl(0)
# will need all the efficiencies here!