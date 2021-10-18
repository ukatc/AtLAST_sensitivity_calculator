from src.functions.sensitivity import Calculator
from src.functions.calculations import *
import astropy.units as u
from astropy import constants 
import numpy as np
from src.configs.config import Config


params = Config("src/configs/user_inputs.yaml","src/configs/setup_inputs.yaml", "src/configs/fixed_inputs.yaml", "src/configs/default_inputs.yaml")

####################
# AT THE MOMENT THERE IS A DISCONNECT HERE 
# SOME FILLER INPUT VALUES FOR NOW
bandwidth = 7.5 * u.GHz
tau_atm = 0.7
# sefd = 10 * u.K / u.m**2 * (constants.k_B)
n_pol = 1
eta_s = 1
sensitivity = 0.00882922 * u.Jy
t_int= 1 * u.s
T_sys = 270 * u.K
radius = 25 * u.m
area = np.pi * radius**2
eta_A = 1
####################



sefd = SEFD.calculate(T_sys, area, eta_A)
print(sefd)

bandwidth = bandwidth.to(u.Hz)

calculator = Calculator(bandwidth, tau_atm, sefd, n_pol, eta_s)

print("Sensitivity: ", calculator.sensitivity(t_int))

print("Integration time: ", calculator.t_integration(sensitivity))