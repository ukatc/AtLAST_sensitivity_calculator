import math
from fastapi import Request
from atlast_sc.data import param_data_type_dicts


def utility_processor(request: Request):
    return {'placeholder': 'Enter a value...'}


def default_values_processor(request: Request):
    def default_value(param):
        return param_data_type_dicts[param]['DEFAULT_VALUE']

    return dict(default_value=default_value)


def default_units_processor(request: Request):
    def default_unit(param):
        return param_data_type_dicts[param]['DEFAULT_UNIT']

    return dict(default_unit=default_unit)


def allowed_range_processor(request: Request):
    def allowed_range(param):
        print(param_data_type_dicts)
        param_data = param_data_type_dicts[param]
        print(param)
        print(param_data)
        maximum = None

        if 'LOWER_VALUE_IS_FLOOR' in param_data:
            minimum = f"> {param_data['LOWER_VALUE']}"
        else:
            minimum = f"{param_data['LOWER_VALUE']}"
        if 'UPPER_VALUE_IS_CEIL' in param_data:
            print(param)
            print(maximum)
            if not math.isinf(param_data['UPPER_VALUE']):
                print('so i am here with param', param)
                maximum = f"< {param_data['UPPER_VALUE']}"
        else:
            maximum = f"{param_data['UPPER_VALUE']}"

        message = F"Min: {minimum}{'; Max: ' + str(maximum) if maximum else ''}"

        return message

    return dict(allowed_range=allowed_range)

