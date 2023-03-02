import os
import functools
import json
from yaml import load, Loader


########################
# Decorator functions  #
########################

def params_updater(func):
    # If the new value is different from the current value,
    # recalculate the other parameters used in the calculation

    @functools.wraps(func)
    def update_param(*args, **kwargs):
        obj = args[0]
        value = args[1]
        attribute = getattr(obj, func.__name__)

        # Make sure the new value is of the correct type
        if not isinstance(value, type(attribute)):
            raise ValueError(f'Value {value} for parameter {func.__name__} '
                             f'is of invalid type. '
                             f'Expected {type(attribute)}. '
                             f'Received {type(value)}.')

        # Validate the new value
        try:
            obj.calculation_inputs.validate_update(func.__name__,
                                                   value)
        except ValueError as e:
            raise e

        # Determine if the old and new values differ
        dirty = (attribute != value)

        # Update the parameter
        func(*args, **kwargs)

        # Recalculate other parameters, if necessary
        if dirty:
            # TODO: be intelligent about this - only update affected params?
            # TODO: check the data validation is happening when this func is
            #  called
            obj.calculate_derived_parameters()

    return update_param


class FileHelper:
    # TODO: Sort out the inconsistency between supported reader types and
    #   supported writer types

    @staticmethod
    def read_from_file(path, file_name):
        file_reader = FileHelper._get_reader(file_name)

        file_path = os.path.join(path, file_name)

        return file_reader(file_path)

    @staticmethod
    def _get_reader(file_name):

        # Extract the extension from the file name
        # and remove the leading '.'
        extension = os.path.splitext(file_name)[1].lstrip('.')

        match extension:
            case 'yaml' | 'yml':
                return FileHelper._dict_from_yaml
            case 'json':
                return FileHelper._dict_from_json
            case 'txt':
                raise ValueError('TXT not yet supported')
            case _:
                raise ValueError(f'Unsupported file type {extension}. Must be '
                                 f'"json", "yaml", or "yml"')

    @staticmethod
    def _dict_from_yaml(file_path):
        """
        Read input from a yaml file with parameters described in the
        format <param_name>: {<value>:<param_value>, <unit>:<param_unit>}
        and return a dictionary

        :param path: the path to the yaml file
        :type path: str
        :param file_name: the name of the yaml file
        :type file_name: str
        """

        with open(file_path, "r") as yaml_file:
            inputs = load(yaml_file, Loader=Loader)

        return inputs

    @staticmethod
    def _dict_from_json(path, file_name):
        """
        Takes a .json input file of user inputs and returns a dictionary

        :param path: the path of the input json file
        :type path: str
        """
        # TODO: NOT TESTED
        with open(path, "r") as json_file:
            inputs = json.load(json_file)
        return inputs

    @staticmethod
    def write_to_file(params, path, file_name, file_type):

        file_writer = FileHelper._get_writer(file_type)

        file_path = f'{os.path.join(path, file_name)}.{file_type}'

        with open(file_path, "w") as f:
            for key, value in params.items():
                file_writer(f, key, value)

    @staticmethod
    def _get_writer(file_type):
        match file_type:
            case 'yaml' | 'yml':
                return FileHelper._to_yaml
            case 'txt':
                return FileHelper._to_txt
            case 'json':
                raise ValueError('JSON not yet supported')
            case _:
                raise ValueError(f'Unsupported file type {file_type}. Must be '
                                 f'"txt", "yaml", or "yml"')

    @staticmethod
    def _to_txt(f, key, value):
        """
        Write config parameters to file

        :param path: the path of the output log file
        :type path: str
        """
        # TODO update docstring
        # with open(file_path, "w") as f:
        #     for key, value in params.items():
        f.write(f"{key} = {value} \n")

    @staticmethod
    def _to_yaml(f, key, value):
        # TODO: docstring
        # with open(file_path, "w") as f:
        #     for key, val in params.items():
        if hasattr(value, "unit"):
            unit = value.unit
            value = value.value
            f.write(f"{key: <16}: {{value: {value: >10}, "
                    f"unit: {unit}}} \n")
        else:
            # TODO: do we need 'none' for unit?
            f.write(f"{key: <16}: {{value: {value: >10}, unit: none}} \n")
