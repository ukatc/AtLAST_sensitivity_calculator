import os
import astropy.units as u
from atlast_sc.calculator import Calculator
from atlast_sc import utils

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Read the user input from a yaml file
user_input = utils.from_yaml('input_data', 'user_inputs.yaml')
# Initialise the Calculator with user inputs dictionary
calculator = Calculator(user_input)
# calculator = Calculator()

# Calculate sensitivity or t_int depending on input
print("-----------")

# print('started with params', calculator.calculation_params)

# Calculate the sensitivity for a given integration time
# (here, specified in user_input.yaml)
# calculator.bandwidth = 10.5*u.GHz
# calculator.elevation = 10*u.deg
# calculator.obs_frequency = 1*u.GHz
# print('using params', calculator.calculation_params)

# TODO: is there a reason for not converting the sensitivity to mJy by default?
calculated_sensitivity = \
    calculator.calculate_sensitivity(calculator.t_int).to(u.mJy)
print("Sensitivity: {:0.2f} for an integration time of {:0.2f} "
      .format(calculated_sensitivity, calculator.t_int))
# TODO: How to store the calculated sensitivity?
#  (Writing it to the calculator object is not a good idea)
calculator.sensitivity = calculated_sensitivity

# Calculate the integration time for a given sensitivity
calculated_t_int = \
    calculator.calculate_t_integration(calculator.sensitivity)
print("Integration time: {:0.2f} to obtain a sensitivity of {:0.2f}"
      .format(calculated_t_int, calculator.sensitivity.to(u.mJy)))
# TODO: How to store the calculated integration time?
#  (Writing it to the calculator object is not a good idea)
calculator.t_int = calculated_t_int

print("-----------")

# Print all parameters to a log file
# TODO: the user should not have to interact with the utils module directly.
#  Create a wrapper to access this functionality via the Calculator object.
# TODO: provide a wrapper for the calculator_params function in
#  the Calculator class
utils.to_file(calculator.calculation_params, "logs/output_parameters.txt")
utils.to_yaml(calculator.calculation_params, "logs/output_parameters.yaml")

# reset the calculator
calculator.reset_calculator()
# print('params now', calculator.calculation_params)
