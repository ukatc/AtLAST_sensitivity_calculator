# flake8: noqa
import math
import os
import astropy.units as u
from atlast_sc.calculator import Calculator
from atlast_sc.utils import FileHelper

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Read the user input from a yaml file
user_input = FileHelper.read_from_file('input_data', 'user_inputs.yaml')
# Initialise the Calculator with user inputs dictionary
calculator = Calculator(user_input)
# calculator = Calculator()

# Calculate sensitivity or t_int depending on input
print("-----------")

# print('started with params', calculator.calculation_params)

# Calculate the sensitivity for a given integration time
# (here, specified in user_input.yaml)
# calculator.bandwidth = 10*u.kHz
# calculator.elevation = 5*u.deg
# calculator.dish_radius = 100*u.m
# calculator.dish_radius = 'nonsense'
# calculator.obs_freq = 140*u.GHz
# calculator.t_int = 2*u.s
# calculator.sensitivity = float('inf')*u.Jy
# calculator.n_pol = 1
# print('using params', calculator.calculation_parameters_as_dict)
# calculator.t_int = 100*u.min
# calculator.obs_freq = 550*u.GHz
# t_int = 5 * u.s
# calculated_sensitivity = \
#     calculator.calculate_sensitivity(t_int, False)
# print("Sensitivity: {:0.2f} for an integration time of {:0.2f} "
#       .format(calculated_sensitivity, t_int))
# calculator.sensitivity = calculated_sensitivity
# calculator.bandwidth = 10*u.GHz
sens = 10*u.mJy
calculated_t_int = \
    calculator.calculate_t_integration(sens, False)
print("Integration time: {:0.2f} to obtain a sensitivity of {:0.2f}"
      .format(calculated_t_int, sens))

print("-----------")

# Write all parameters to a log file
# calculator.output_to_file("logs", "output_parameters")
# calculator.output_to_file("logs", "output_parameters", "yml")
FileHelper.write_to_file(calculator, "logs", "output_parameters", "yml")

print(calculator.instrument_setup)
print(calculator.user_input)
print(calculator.derived_parameters)
# print(calculator.T_sys.round(4))
# # reset the calculator
# print('before resetting', calculator.calculation_parameters_as_dict)
# calculator.reset()
# print('after resetting', calculator.calculation_parameters_as_dict)
# TODO: add something here to demonstrate that the calculator has been reset
