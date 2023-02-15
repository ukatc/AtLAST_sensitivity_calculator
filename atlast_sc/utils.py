import os
import json
from yaml import load, Loader


def from_yaml(path, file_name):
    """
    Read input from a .yaml file and return a dictionary

    :param path: the .yaml file with parameters described as param_name: {value:param_value, unit:param_unit}
    :type path: str (file path)
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
                f.write(f"{key: <16}: {{value: {value: >10}, unit: {unit}}} \n")
            else:
                # TODO: do we need 'none' for unit?
                f.write(f"{key: <16}: {{value: {value: >10}, unit: none}} \n")

