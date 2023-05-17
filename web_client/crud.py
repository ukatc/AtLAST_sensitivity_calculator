import json
import math
from dataclasses import asdict
from pydantic import ValidationError
from atlast_sc.calculator import Calculator
from atlast_sc.data import Data


def do_calculation(user_input, calculation):
    """
    Perform the specified calculation (sensitivity or integration time)
    """
    try:
        calculator = _create_calculater(user_input)
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


def _create_calculater(user_input):
    """
    Create a calculator object with the specified user input
    """
    try:
        calculator = Calculator(user_input)
    except ValidationError as e:
        message = json.loads(e.json())[0]["msg"]
        raise UserInputError(message)

    return calculator


class UserInputError(ValueError):

    def __init__(self, message):
        self.message = message

        super().__init__(message)
