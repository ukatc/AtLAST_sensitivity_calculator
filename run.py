from src.functions.atmosphere_params import AtmosphereParams
from src.functions.sensitivity import Sensitivity
from src.functions.sefd import SEFD
from src.functions.system_temperature import SystemTemperature
from src.functions.efficiencies import Efficiencies
import astropy.units as u
from astropy import constants 
import numpy as np
from src.configs.config import Config


params = Config("src/configs/user_inputs.yaml","src/configs/setup_inputs.yaml", "src/configs/fixed_inputs.yaml", "src/configs/default_inputs.yaml")

####################
# AT THE MOMENT THERE IS A DISCONNECT HERE 
# SOME FILLER INPUT VALUES FOR NOW

eta_s = 1
sensitivity = 0.01 * u.Jy
t_int= 50 * u.s

# Temperatures

T_rx = 50 * u.K
T_amb = 270 * u.K
T_gal = 10 * u.K

eta_eff = 0.9

####################

params.area = np.pi * params.dish_radius**2

atm = AtmosphereParams(
    params.obs_freq, 
    params.weather, params.elevation)

params.tau_atm = atm.tau_atm()
params.T_atm = atm.T_atm()

# At present, eta_a does not calculate efficiency properly! just a placeholder!
eta_a = Efficiencies(
    params.eta_radf,
    params.eta_block,
    params.eta_ill 
    ).eta_a()

T_sys = SystemTemperature(
    T_rx, 
    params.T_cmb, 
    params.T_atm, 
    T_amb, 
    T_gal, 
    params.tau_atm
    ).system_temperature(
        params.g, 
        eta_eff)

sefd = SEFD.calculate(
    T_sys, 
    params.area, 
    eta_a)

calculator = Sensitivity(
    params.bandwidth.to(u.Hz), 
    params.tau_atm, 
    sefd,
    params.n_pol, 
    eta_s)

print("For the following parameters: ")
for attr in vars(params):
    if type(getattr(params, attr)) == dict:
        pass
    else:
        print("{} = {}".format(attr, getattr(params, attr)))


print("-----------")
print("Sensitivity: {:0.2f} for an integration time of {:0.2f} ".format(calculator.sensitivity(t_int).to(u.mJy), t_int))

print("Integration time: {:0.2f} to obtain a sensitivity of {:0.2f}".format(calculator.t_integration(sensitivity), sensitivity.to(u.mJy)))

print("-----------")
