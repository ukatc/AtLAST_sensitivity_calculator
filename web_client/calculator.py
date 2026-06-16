import json
import math
from dataclasses import asdict
from atlast_sc.calculator import Calculator
from pydantic import ValidationError
from atlast_sc.data import Data


def do_calculation(user_input, calculation):
    """
    Perform the specified calculation (sensitivity or integration time)
    """
    try:
        calculator = _create_calculator(user_input)
    except UserInputError as e:
        raise e

    func = None
    match calculation:
        case "sensitivity":
            func = calculator.calculate_sensitivity
        case "integration_time":
            func = calculator.calculate_t_integration
        case _:
            # TODO: handle error
            pass
    
    calculated_param = func(update_calculator=False)

    value = calculated_param.value
    unit = str(calculated_param.unit)

    return {"value": value, "unit": unit}


def get_param_values_units():
    """
    Return the values, units, data conversion factors, etc. for each of the
    calculator input parameters (user input and instrument setup)
    """
    param_values_units = {
        param: asdict(data) for param, data in
        Data.param_data_type_dicts.items()
    }

    # convert 'inf' to very large number, otherwise the json encoder will
    # complain
    for param in param_values_units:
        for key, val in param_values_units[param].items():
            # print(key)
            if type(val) == float and math.isinf(val):
                param_values_units[param][key] = 100**10
    return param_values_units


def get_available_instruments():
    """
    Return a list of available instruments with Default always first
    """
    from atlast_sc.instruments.config import InstrumentConfig
    inst_config = InstrumentConfig()
    instrument_names = list(inst_config.instrument_classes.keys())
    # Sort the instruments, but put "Default" first
    sorted_instruments = sorted(instrument_names)
    if "Default" in sorted_instruments:
        sorted_instruments.remove("Default")
        sorted_instruments.insert(0, "Default")
    return sorted_instruments


def _create_calculator(user_input):
    """
    Create a calculator object with the specified user input and apply
    the currently selected instrument if one has been set.
    """
    try:
        calculator = Calculator(user_input)
    except ValidationError as e:
        message = json.loads(e.json())[0]["msg"]
        raise UserInputError(message)
    
    # Apply the selected instrument if one has been set
    try:
        from web_client import main
        if main.selected_instrument:
            calculator.chosen_instrument = main.selected_instrument
    except Exception as e:
        # If there's any error applying the instrument, log it but continue
        print(f"Warning: Could not apply selected instrument: {e}")

    return calculator


class UserInputError(ValueError):

    def __init__(self, message):
        self.message = message

        super().__init__(message)
