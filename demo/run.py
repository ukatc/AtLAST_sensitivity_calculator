import astropy.units as u
from atlast_sc.calculator import Calculator
from atlast_sc import utils

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialise the Calculator with user inputs
# TODO: simplify this interface further. The user should not have to interact directly with the utils module
calculator = Calculator(utils.from_yaml("input_data", "user_inputs.yaml"))

# Calculate sensitivity or t_int depending on input
print("-----------")
if calculator.t_int:
    calculated_sensitivity = calculator.calculate_sensitivity(calculator.t_int).to(u.mJy)
    print("Sensitivity: {:0.2f} for an integration time of {:0.2f} ".format(calculated_sensitivity, calculator.t_int))
    # TODO: How to store the calculated sensitivity? (Writing it to the calculator object is not a good idea)
    calculator.sensitivity = calculated_sensitivity
elif calculator.sensitivity:
    calculated_t_int = calculator.calculate_t_integration(calculator.sensitivity)
    print("Integration time: {:0.2f} to obtain a sensitivity of {:0.2f}".format(calculated_t_int, calculator.sensitivity.to(u.mJy)))
    # TODO: How to store the calculated integration time? (Writing it to the calculator object is not a good idea)
    calculator.t_int = calculated_t_int
print("-----------")


# Print all parameters to a log file
# TODO: the user should not have to interact with the utils module directly. Creator a wrapper to access this
#       functionality via the Calculator object.
# TODO: provide a wrapper for the calculator_params function in the Calculator class
utils.to_file(calculator.sensitivity_calc_params.calculator_params(), "logs/log_output_parameters.txt")
utils.to_yaml(calculator.sensitivity_calc_params.calculator_params(), "logs/repeat.yaml")
