import os
import functools
import json
from yaml import load, Loader


def from_yaml(path, file_name):
    """
    Read input from a yaml file with parameters described in the
    format <param_name>: {<value>:<param_value>, <unit>:<param_unit>}
    and return a dictionary

    :param path: the path to the yaml file
    :type path: str
    :param file_name: the name of the yaml file
    :type file_name: str
    """

    file_path = os.path.join(path, file_name)
    with open(file_path, "r") as yaml_file:
        inputs = load(yaml_file, Loader=Loader)

    return inputs


def from_json(path):
    """
    Takes a .json input file of user inputs and returns an instance of Config

    :param path: the path of the input json file
    :type path: str
    """
    with open(path, "r") as json_file:
        inputs = json.load(json_file)
    return inputs


def to_file(params, path):
    """
    Write config parameters to file

    :param path: the path of the output log file
    :type path: str
    """
    # TODO update docstring
    with open(path, "w") as f:
        for key, value in params.items():
            f.write(f"{key} = {value} \n")


def to_yaml(params, path):
    # TODO: docstring
    with open(path, "w") as f:
        for key, value in params.items():
            if hasattr(value, "unit"):
                unit = value.unit
                f.write(f"{key: <16}: {{value: {value: >10}, "
                        f"unit: {unit}}} \n")
            else:
                # TODO: do we need 'none' for unit?
                f.write(f"{key: <16}: {{value: {value: >10}, unit: none}} \n")


def update_input_param(func):
    # If the new value is different from the current value,
    # recalculate the other parameters used in the calculation

    @functools.wraps(func)
    def update_param(*args, **kwargs):
        obj = args[0]
        value = args[1]
        attribute = getattr(obj, func.__name__)

        # Make sure the new value is of the correct type
        # TODO: this assert might not be necessary if I can enforce
        #       data validation at the point where the parameters is set
        #       to the new value
        assert isinstance(value, type(attribute))
        # Determine if the old and new values differ
        dirty = (attribute != value)

        # Update the parameter
        func(*args, **kwargs)

        # Recalculate other parameters, if necessary
        if dirty:
            # TODO: be intelligent about this - only update affected params?
            # TODO: check the data validation is happening when this func is
            #  called
            obj.generate_calculation_params()

    return update_param
