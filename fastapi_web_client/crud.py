import json
from pydantic import ValidationError
from atlast_sc.calculator import Calculator
from atlast_sc.data import param_data_type_dicts


def do_calculation(user_input, calculation):

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

    calculated_param = func()

    value = calculated_param.value
    unit = str(calculated_param.unit)

    return {"value": value, "unit": unit}


def get_param_values_units():
    return json.dumps(param_data_type_dicts)


def _create_calculater(user_input):

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
