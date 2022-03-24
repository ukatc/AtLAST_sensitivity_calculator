from atlast_sc.sensitivity import Sensitivity
import astropy.units as u
from atlast_sc.configs.config import Config

# Initialise the input parameters from Config
calculator = Sensitivity(Config.from_yaml("user_inputs.yaml"))

# Store the parameters input to this calculation instance in the variable "config"
config = calculator.config


# Calculate sensitivity or t_int depending on input
print("-----------")
if config.t_int.value and not config.sensitivity.value: 
    calculated_sensitivity = calculator.sensitivity(config.t_int).to(u.mJy) 
    print("Sensitivity: {:0.2f} for an integration time of {:0.2f} ".format(calculated_sensitivity, config.t_int))
    config.sensitivity = calculated_sensitivity
elif config.sensitivity.value and not config.t_int.value:
    calculated_t_int = calculator.t_integration(config.sensitivity)
    print("Integration time: {:0.2f} to obtain a sensitivity of {:0.2f}".format(calculated_t_int, config.sensitivity.to(u.mJy)))
    config.t_int = calculated_t_int
else:
    print("Please add either a sensitivity *or* an integration time to your input.")
print("-----------")


# Print all parameters to a log file
config.to_file("logs/log_output_parameters.txt")
config.to_yaml("logs/repeat.yaml")