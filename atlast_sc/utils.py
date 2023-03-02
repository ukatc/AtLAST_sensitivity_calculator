import os
import functools
import json
from yaml import load, Loader


########################
# Decorator functions  #
########################

def params_updater(func):
    """
    Decorator to support setter methods on calculations input parameters.
    The returned function first validates the type, value and units
    of the new value before updating the parameter. If the new value is
    different from the old, derived parameters are recalculated.
    """
    # If the new value is different from the current value,
    # recalculate the other parameters used in the calculation

    @functools.wraps(func)
    def update_param(*args, **kwargs):
        calculator = args[0]
        value = args[1]
        attribute = getattr(calculator, func.__name__)

        # Make sure the new value is of the correct type
        if not isinstance(value, type(attribute)):
            raise ValueError(f'Value {value} for parameter {func.__name__} '
                             f'is of invalid type. '
                             f'Expected {type(attribute)}. '
                             f'Received {type(value)}.')

        # Validate the new value
        try:
            calculator.calculation_inputs.\
                validate_update(func.__name__, value)
        except ValueError as e:
            raise e

        # Determine if the old and new values differ
        dirty = (attribute != value)

        # Update the parameter
        func(*args, **kwargs)

        # Recalculate derived parameters, if necessary
        if dirty:
            # TODO: be intelligent about this - only update affected params?
            calculator.calculate_derived_parameters()

    return update_param


class FileHelper:
    # TODO: Sort out the inconsistency between supported reader types and
    #   supported writer types

    SUPPORTED_FILE_EXTENSIONS = ['yaml', 'yml', 'txt', 'json']

    @staticmethod
    def read_from_file(path, file_name):
        file_reader = FileHelper._get_reader(file_name)

        file_path = os.path.join(path, file_name)

        with open(file_path, "r") as file:
            inputs = file_reader(file)

        return inputs

    @staticmethod
    def _get_reader(file_name):

        # Extract the extension from the file name
        # and remove the leading '.'
        extension = os.path.splitext(file_name)[1].lstrip('.').lower()

        match extension:
            case 'yaml' | 'yml':
                return FileHelper._dict_from_yaml
            case 'json':
                return FileHelper._dict_from_json
            case 'txt':
                return FileHelper._dict_from_txt
            case _:
                raise ValueError(f'Unsupported file type {extension}. Must be '
                                 f'one of: '
                                 f'{FileHelper.SUPPORTED_FILE_EXTENSIONS}')

    @staticmethod
    def _dict_from_yaml(file):
        """
        Read input from a yaml file with parameters described in the
        format <param_name>: {<value>:<param_value>, <unit>:<param_unit>}
        and return a dictionary

        :param path: the path to the yaml file
        :type path: str
        :param file_name: the name of the yaml file
        :type file_name: str
        """
        inputs = load(file, Loader=Loader)

        return inputs

    @staticmethod
    def _dict_from_json(file):
        """
        Takes a .json input file of user inputs and returns a dictionary

        :param path: the path of the input json file
        :type path: str
        """
        inputs = json.load(file)

        return inputs

    @staticmethod
    def _dict_from_txt(file):
        def _parse_line(line_to_parse):
            try:
                # parse the parameter name, which appears before '='
                ind = line_to_parse.index('=')
                param_name = line_to_parse[:ind].strip()

                # parse the value, which appears between '=' and
                # the space before the unit, if there is one
                # (there may or not be a space between '=' and the value)
                sub_str = line_to_parse[ind + 1:].strip()
                ind = sub_str.find(' ')
                if ind != -1:
                    value = sub_str[:ind].strip()
                    # parse the unit, if there is one
                    unit = sub_str[ind:].strip()
                else:
                    value = sub_str.strip()
                    unit = None

            except ValueError as e:
                raise e

            return param_name, value, unit

        inputs = {}
        for line in file.read().splitlines():
            parsed_values = _parse_line(line)
            inputs[parsed_values[0]] = {
                'value': parsed_values[1],
                'unit': parsed_values[2]
            }

        return inputs

    @staticmethod
    def write_to_file(params, path, file_name, file_type):

        file_writer = FileHelper._get_writer(file_type)

        file_path = f'{os.path.join(path, file_name)}.{file_type}'

        with open(file_path, "w") as f:
            file_writer(f, params)

    @staticmethod
    def _get_writer(file_type):
        match file_type:
            case 'yaml' | 'yml':
                return FileHelper._to_yaml
            case 'txt':
                return FileHelper._to_txt
            case 'json':
                return FileHelper._to_json
            case _:
                raise ValueError(f'Unsupported file type {file_type}. '
                                 f'Must be one of '
                                 f'{FileHelper.SUPPORTED_FILE_EXTENSIONS}')

    @staticmethod
    def _to_txt(file, params):
        """
        Write config parameters to file

        :param path: the path of the output log file
        :type path: str
        """

        for key, value in params.items():
            file.write(f"{key} = {value} \n")

    @staticmethod
    def _to_yaml(file, params):
        # TODO: docstring

        for key, value in params.items():
            if hasattr(value, "unit"):
                unit = value.unit
                value = value.value
                file.write(f"{key: <16}: {{value: {value: >10}, "
                           f"unit: {unit}}} \n")
            else:
                file.write(f"{key: <16}: "
                           f"{{value: {value: >10}}} \n")

    @staticmethod
    def _to_json(file, params):

        outputs = {}
        for key, value in params.items():
            if hasattr(value, "unit"):
                unit = str(value.unit)
                value = value.value
                outputs[key] = {'value': value, 'unit': unit}
            else:
                outputs[key] = {'value': value}

        json.dump(outputs, file, indent=2)
