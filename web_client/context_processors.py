import math
from fastapi import Request
from atlast_sc.data import param_data_type_dicts


def invalid_message_processor(request: Request):
    def invalid_message(param):
        param_data = param_data_type_dicts[param]

        message = "Please enter a valid number "

        # Not that the conditions below don't capture every possible
        #   scenario, but they do cover the scenarios expected with the
        #   parameters we have.
        if param_data.lower_value_is_floor:
            message = message + \
                f"> {param_data.lower_value}"
        elif param_data.upper_value_is_ceil \
                and math.isinf(param_data.upper_value):
            message = message + f">= {param_data.lower_value}"
        else:
            message = message + f"between {param_data.lower_value} " \
                                f"and {param_data.upper_value}"

        # Specify the default unit in the message if the lower value is not
        # zero and there is more than one possible unit
        if param_data.lower_value != 0 \
                and param_data.units and \
                len(param_data.units) > 1:
            message = message + " " + param_data.default_unit

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
        # NB: the message construction code below does not cover all
        #   logically possible conditions. However, it does cover the
        #   scenarios that exist in the application.

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

        if maximum is None and not param_data.lower_value_is_floor:
            message = f">={minimum}"
        else:
            message = \
                f"{minimum}{' - ' + str(maximum) if maximum else ''}"

        # Specify the default unit in the message if the lower value is not
        # zero and there is more than one possible unit
        if param_data.lower_value != 0 \
                and param_data.units and \
                len(param_data.units) > 1:
            message = message + " " + param_data.default_unit

        return message

    return dict(allowed_range=allowed_range)
