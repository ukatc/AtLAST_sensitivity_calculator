import os
import functools
import json
from yaml import load, Loader
from astropy.units import Unit


class Decorators:
    """
    Decorator functions
    """

    @staticmethod
    def validate_value(func):
        """
        Decorator to support setter methods on calculations input parameters.
        Validates the value for the
        target parameter.
        """
        @functools.wraps(func)
        def do_validation(calculator, value, **kwargs):
            """
            Validates the type, value and units of the value for the target
            parameter.

            :param calculator: The Calculator object
            :type calculator: Calculator
            :param value: The new value
            :type value: int, float or Quantity
            """

            # Ensure integer values are converted to floats (all parameter values
            # are expected to be floats)
            if isinstance(value, int):
                value = float(value)

            # Validate the new value
            DataHelper.validate(calculator, func.__name__, value)

            # Update the parameter
            func(calculator, value, **kwargs)

        return do_validation

    @staticmethod
    def validate_and_update_params(func):
        """
        Decorator to support setter methods on calculations input parameters
        that input to the derived parameters. Validates the value for the
        target parameter and recalculates derived parameters where necessary.

        :param func: function that updates the calculation input parameter
        :type func: property setter function
        """

        @functools.wraps(func)
        def do_update(calculator, value, **kwargs):
            """
            Validates the type, value and units of the value for the target
            parameter. If the new value is different from the old, derived
            parameters are recalculated.

            :param calculator: The Calculator object
            :type calculator: Calculator
            :param value: The new value
            :type value: int, float or Quantity
            """

            # Ensure integer values are converted to floats (all parameter values
            # are expected to be floats)
            if isinstance(value, int):
                value = float(value)

            # Validate the new value
            DataHelper.validate(calculator, func.__name__, value)

            # Determine if the old and new values differ
            attribute = getattr(calculator, func.__name__)
            dirty = (attribute != value)

            # Update the parameter
            func(calculator, value, **kwargs)

            # Recalculate derived parameters, if necessary
            if dirty:
                calculator._calculate_derived_parameters()

        return do_update


class FileHelper:
    """
    Class that provides support for reading input parameters from a file
    and writing outputs to a file.
    Supported file formats are `yaml`, `txt`, and `json`.
    """

    _SUPPORTED_FILE_EXTENSIONS = ['yaml', 'yml', 'txt', 'json']
    _UNSUPPORTED_FILE_TYPE_ERROR_MSG = \
        'Unsupported file type "{file_type}". ' \
        'Must be one of: {supported_extensions}'

    @staticmethod
    def read_from_file(path, file_name):
        """
        Reads the file with name `file_name` located in directory `path`
        and returns a dictionary. The file type (e.g., `yaml`) is
        and returns a dictionary. The file type (e.g., `yaml`) is
        determined from the file extension in`file_name`.

        :param path: The directory where the file is located.
        :type path: str
        :param file_name: The name of the file, including the file extension.
        :type file_name: str
        :return: Dictionary of input parameters.
        :rtype: dict[str, float]
        """
        file_reader = FileHelper._get_reader(file_name)

        file_path = os.path.join(path, file_name)

        with open(file_path, "r") as file:
            inputs = file_reader(file)

        # Try to convert values to floats
        for key, param in inputs.items():
            try:
                param['value'] = float(param['value'])
            except ValueError:
                # Raise a TypeError with a pretty message
                raise TypeError(f'Value "{param["value"]}" is invalid '
                                f'for parameter "{key}". '
                                f'Parameter values must be numeric.')

        return inputs

    @staticmethod
    def write_to_file(calculator, path, file_name, file_type):
        """
        Writes the values stored in `calculator` to a file with name
        `file_name` and extension `file_type` to location `path`.

        :param calculator: A Calculator object.
        :type calculator: atlast_sc.calculator.Calculator
        :param path: The location where the file is saved.
        :type path: str
        :param file_name: The name of the file to write. Note this should not
                            include the file extension.
        :type file_name: str
        :param file_type: The file type (e.g., `yaml`).
        :type file_type: str
        """

        file_type = file_type.lower()
        file_writer = FileHelper._get_writer(file_type)

        file_path = f'{os.path.join(path, file_name)}.{file_type}'

        # Create and concatenate dictionaries from the user input model and
        # the derived parameters model
        params = {param: val['value']
                  for param, val in calculator.user_input.dict().items()} | \
            calculator.derived_parameters.dict()

        with open(file_path, "w") as f:
            file_writer(f, params)

    @staticmethod
    def _get_reader(file_name):
        """
        Factory method that returns the file reader for the
        file type indicated by the extension in `file_name`.

        :param file_name: The name of file to read.
        :type file_name: str
        :return: A file reader function
        :rtype: function
        """
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
                raise ValueError(FileHelper._UNSUPPORTED_FILE_TYPE_ERROR_MSG
                                 .format(file_type=extension,
                                         supported_extensions=FileHelper
                                         ._SUPPORTED_FILE_EXTENSIONS))

    @staticmethod
    def _dict_from_yaml(file):
        """
        Read data from a yaml file.

        :param file: the yaml file
        :type file: buffered text stream (TextIOWrapper)
        :return: a dictionary of parameters
        :rtype: dict
        """
        inputs = load(file, Loader=Loader)
        return inputs

    @staticmethod
    def _dict_from_json(file):
        """
        Read data from a json file.

        :param file: the json file
        :type file: buffered text stream (TextIOWrapper)
        :return: a dictionary of parameters
        :rtype: dict
        """

        def _remove_none_values(d):
            """
            Remove 'None' values from a dictionary `d`.
            This is used when reading input data from a json file
            in which unit-less values are provided. Not strictly
            necessary, but does make the resulting dictionary
            consistent with those produced when reading from a yaml
            or txt file.
            """
            return {key: val for key, val in d.items() if val is not None}

        inputs = json.load(file, object_hook=_remove_none_values)

        return inputs

    @staticmethod
    def _dict_from_txt(file):
        """
        Read data from a txt file.

        :param file: the txt file
        :type file: buffered text stream (TextIOWrapper)
        :return: a dictionary of parameters
        :rtype: dict
        """

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
                'value': parsed_values[1]
            }
            if parsed_values[2]:
                inputs[parsed_values[0]]['unit'] = parsed_values[2]

        return inputs

    @staticmethod
    def _get_writer(file_type):
        """
        Factory method that returns the file writer for the
        specified `file_type`.

        :param file_type: The type of file to write (e.g., `yaml`).
        :type file_type: str
        :return: A file writer function
        :rtype: function
        """

        # Sanity check - make sure the file type is lowercase
        file_type = file_type.lower()

        match file_type:
            case 'yaml' | 'yml':
                return FileHelper._to_yaml
            case 'txt':
                return FileHelper._to_txt
            case 'json':
                return FileHelper._to_json
            case _:
                raise ValueError(FileHelper._UNSUPPORTED_FILE_TYPE_ERROR_MSG
                                 .format(file_type=file_type,
                                         supported_extensions=FileHelper
                                         ._SUPPORTED_FILE_EXTENSIONS))

    @staticmethod
    def _to_txt(file, params):
        """
        Writes a dictionary to a txt file.

        :param file: The txt file
        :type file: buffered text stream (TextIOWrapper)
        :param params: A dictionary of parameters to write.
        :type params: dict
        """
        for key, value in params.items():
            file.write(f"{key} = {value} \n")

    @staticmethod
    def _to_yaml(file, params):
        """
        Writes a dictionary to a yaml file.

        :param file: The yaml file
        :type file: buffered text stream (TextIOWrapper)
        :param params: A dictionary of parameters to write.
        :type params: dict
        """
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
        """
        Writes a dictionary to a json file.

        :param file: The json file
        :type file: buffered text stream (TextIOWrapper)
        :param params: A dictionary of parameters to write.
        :type params: dict
        """
        outputs = {}
        for key, value in params.items():
            if hasattr(value, "unit"):
                unit = str(value.unit)
                value = value.value
                outputs[key] = {'value': value, 'unit': unit}
            else:
                outputs[key] = {'value': value}

        json.dump(outputs, file, indent=2)


class DataHelper:

    @staticmethod
    def validate(calculator, param_name, value):
        attribute = getattr(calculator, param_name)

        # Ensure integer values are converted to floats (all parameter values
        # are expected to be floats)
        if isinstance(value, int):
            value = float(value)

        # Make sure the new value is of the correct type
        if not isinstance(value, type(attribute)):
            raise ValueError(f'Value {value} for parameter {param_name} '
                             f'is of invalid type. '
                             f'Expected {type(attribute)}. '
                             f'Received {type(value)}.')

        # Validate the new value
        try:
            calculator.calculation_inputs. \
                validate_value(param_name, value)
        except ValueError as e:
            raise e

    @staticmethod
    def data_conversion_factors(default_unit, allowed_units):
        """
        Creates a dictionary of units and conversion factors where each
        conversion factor provides the conversion from an allowed
        unit to the default unit for a parameter.

        :param default_unit: The default unit for the parameter
        :type default_unit: str
        :param allowed_units: A list of allowed units for the parameter
        :type allowed_units: list[str]
        :return: A dictionary of units and conversion factors
        :rtype: dict
        """
        conversion_factors = \
            {unit: DataHelper._convert(1, unit, default_unit)
             for unit in allowed_units}

        return conversion_factors

    @staticmethod
    def _convert(value, from_unit, to_unit):
        """
        Converts the specified value from the source to the target unit.

        :param value: The value to be converted
        :type value: float or int
        :param from_unit: The unit to convert from
        :type from_unit: str
        :param to_unit: The unit to convert to
        :type to_unit: str
        :return: A converted value
        :rtype: float
        """
        source_unit = Unit(from_unit)
        target_unit = Unit(to_unit)

        source_quantity = value * source_unit
        converted_quantity = source_quantity.to(target_unit)

        return converted_quantity.value
