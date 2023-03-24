import math
from fastapi import Request
from atlast_sc.data import param_data_type_dicts


def invalid_massage_processor(request: Request):
    def invalid_message(param):
        param_values_units = param_data_type_dicts[param]

        message = "Please enter a valid number "

        if param_values_units.lower_value_is_floor:
            message = message + \
                f"greater than {param_values_units.lower_value}"
        # if param_values_units.upper_value_is_ceil:
        #     less_than_message = f"less than {param_values_units.upper_value}"
        else:
            message = message + f"between {param_values_units.lower_value} " \
                                f"and {[param_values_units.upper_value]}"

        return message

    return dict(invalid_message=invalid_message)


def default_values_processor(request: Request):
    def default_value(param):
        return param_data_type_dicts[param].default_value

    return dict(default_value=default_value)


def default_units_processor(request: Request):
    def default_unit(param):
        return param_data_type_dicts[param].default_unit

    return dict(default_unit=default_unit)


def allowed_range_processor(request: Request):
    def allowed_range(param):
        param_data = param_data_type_dicts[param]
        maximum = None

        if param_data.lower_value_is_floor:
            minimum = f"> {param_data.lower_value}"
        else:
            minimum = f"{param_data.lower_value}"
        if param_data.upper_value_is_ceil:
            if not math.isinf(param_data.upper_value):
                maximum = f"< {param_data.upper_value}"
        else:
            maximum = f"{param_data.upper_value}"

        message = F"Min: {minimum}{'; Max: ' + str(maximum) if maximum else ''}"

        return message

    return dict(allowed_range=allowed_range)

