from functions.sensitivity import Calculator
from functions.calculations import *
import astropy.units as u
from astropy import constants 
import numpy as np
from configs.config import Config


params = Config("configs/user_inputs.yaml","configs/setup_inputs.yaml", "configs/fixed_inputs.yaml", "configs/default_inputs.yaml")

####################
# AT THE MOMENT THERE IS A DISCONNECT HERE 
# SOME FILLER INPUT VALUES FOR NOW
bandwidth = 7.5 * u.GHz
tau_atm = 0.7
sefd = 10 * u.K / u.m**2 * (constants.k_B)
n_pol = 1
eta_s = 1
sensitivity = 5e-6 * u.Jy
t_int= 1 * u.s
T_sys = 270 * u.K
radius = 25 * u.m
area = np.pi * radius**2
eta_A = 1
####################



sefd = get_SEFD(T_sys, area, eta_A)
print(sefd)

bandwidth = bandwidth.to(u.Hz)

calculator = Calculator(bandwidth, tau_atm, sefd, n_pol, eta_s)

print("Sensitivity: ", calculator.calc_sensitivity(t_int))

print("Integration time: ", calculator.calc_t_integration(sensitivity))