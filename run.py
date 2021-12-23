from src.backend.atmosphere_params import AtmosphereParams
from src.backend.sensitivity import Sensitivity
from src.backend.sefd import SEFD
from src.backend.system_temperature import SystemTemperature
from src.backend.efficiencies import Efficiencies
import astropy.units as u
import numpy as np
from src.configs.config import Config


params = Config.from_yaml("user_inputs.yaml")               # Initialise the input parameters from Config
params.area = np.pi * params.dish_radius**2                             # Calculate area of dish & add to parameters

atm = AtmosphereParams( 
    params.obs_freq, 
    params.weather,
    params.elevation)                                                   # Perform atmospheric model calculation
params.tau_atm = atm.tau_atm()                                          # add atmospheric opacity to params
params.T_atm = atm.T_atm()                                              # add atmospheric temperature to params

eta = Efficiencies(
    params.eta_ill)                                                     # Perform efficiency calculations
params.eta_a = eta.eta_a(params.obs_freq, params.surface_rms)           # add eta_a to params
params.eta_s = eta.eta_s()                                              # add eta_s to params - NOTE: currently not implmented, placeholder value!!

T_sys = SystemTemperature(
    params.T_rx, 
    params.T_cmb, 
    params.T_atm, 
    params.T_amb, 
    params.tau_atm
    ).system_temperature(
        params.g, 
        params.eta_eff)                                                 # Calculate system temperature

sefd = SEFD.calculate(
    T_sys, 
    params.area, 
    params.eta_a)                                                       # Calculate source equivalent flux density

calculator = Sensitivity(
    params.bandwidth.to(u.Hz), 
    params.tau_atm, 
    sefd,
    params.n_pol, 
    params.eta_s)                                                       # Initialise sensitivity calculator

print("For the following parameters: ")                                 # List the parameters input to this calculation instance
for attr in vars(params):                                               # May be useful to add a save to file function here
    if type(getattr(params, attr)) == dict:
        pass
    else:
        print("{} = {:0.2f}".format(attr, getattr(params, attr)))

print("-----------")
if params.t_int.value and not params.sensitivity.value:                 # Calculate sensitivity or t_int depending on input
    calculated_sensitivity = calculator.sensitivity(params.t_int).to(u.mJy) 
    print("Sensitivity: {:0.2f} for an integration time of {:0.2f} ".format(calculated_sensitivity, params.t_int))
elif params.sensitivity.value and not params.t_int.value:
    calculated_t_int = calculator.t_integration(params.sensitivity)
    print("Integration time: {:0.2f} to obtain a sensitivity of {:0.2f}".format(calculated_t_int, params.sensitivity.to(u.mJy)))
else:
    print("Please add either a sensitivity or an integration time to your input.")
print("-----------")
