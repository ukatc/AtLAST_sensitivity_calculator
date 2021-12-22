from src.functions.atmosphere_params import AtmosphereParams
from src.functions.sensitivity import Sensitivity
from src.functions.sefd import SEFD
from src.functions.system_temperature import SystemTemperature
from src.functions.efficiencies import Efficiencies
import astropy.units as u
from astropy import constants 
import numpy as np
from src.configs.config import Config


# Initialise the input parameters from Config
params = Config("src/configs/user_inputs.yaml","src/configs/setup_inputs.yaml", "src/configs/fixed_inputs.yaml", "src/configs/default_inputs.yaml")

# Calculate area of dish & add to parameters
params.area = np.pi * params.dish_radius**2

# Perform atmospheric model calculation, and add atmospheric opacity and temperature to params
atm = AtmosphereParams(
    params.obs_freq, 
    params.weather,
    params.elevation)
params.tau_atm = atm.tau_atm()
params.T_atm = atm.T_atm()

# Perform efficiency calculations and add to params
eta = Efficiencies(
    params.eta_ill)
params.eta_a = eta.eta_a(params.obs_freq, params.surface_rms)
params.eta_s = eta.eta_s()

# Calculate system temperature
T_sys = SystemTemperature(
    params.T_rx, 
    params.T_cmb, 
    params.T_atm, 
    params.T_amb, 
    params.tau_atm
    ).system_temperature(
        params.g, 
        params.eta_eff)

# Calculate source equivalent flux density
sefd = SEFD.calculate(
    T_sys, 
    params.area, 
    params.eta_a)

# Initialise sensitivity calculator
calculator = Sensitivity(
    params.bandwidth.to(u.Hz), 
    params.tau_atm, 
    sefd,
    params.n_pol, 
    params.eta_s)

# List the parameters input to this calculation instance
print("For the following parameters: ")
for attr in vars(params):
    if type(getattr(params, attr)) == dict:
        pass
    else:
        print("{} = {:0.2f}".format(attr, getattr(params, attr)))

# Calculate and print either integration time or sensitivity, depending on input
# (one or the other, not both)
print("-----------")
if params.t_int.value and not params.sensitivity.value:
    print("Sensitivity: {:0.2f} for an integration time of {:0.2f} ".format(calculator.sensitivity(params.t_int).to(u.mJy), params.t_int))
elif params.sensitivity.value and not params.t_int.value:
    print("Integration time: {:0.2f} to obtain a sensitivity of {:0.2f}".format(calculator.t_integration(params.sensitivity), params.sensitivity.to(u.mJy)))
else:
    print("Please add either a sensitivity or an integration time to your input.")
print("-----------")
