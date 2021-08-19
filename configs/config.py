import yaml
from yaml import Loader, Dumper
import astropy.units as u


def get_inputs(file, dict):
    file = open(file, "r")
    inputs = yaml.load(file, Loader=Loader)
    for key in inputs.keys():
        unit = getattr(u, inputs[key]['unit'])
        dict[key] = inputs[key]['value'] * unit

input_params = {}
get_inputs("fixed_inputs.yaml", input_params)
get_inputs("setup_inputs.yaml", input_params)

print(input_params)
