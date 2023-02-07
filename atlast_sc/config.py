import os
from pathlib import Path
import json
from yaml import load, Loader
from astropy.units import Unit
from astropy.units.quantity import Quantity

from atlast_sc import inputs

PARENT_PATH = Path(__file__).resolve().parents[0]

STANDARD_CONFIG_PATH = os.path.join(PARENT_PATH, "configs", "standard")
BENCHMARKING_CONFIGS_PATH = os.path.join(PARENT_PATH, "configs", "benchmarking")
BENCHMARKING_JCMT_PATH = os.path.join(BENCHMARKING_CONFIGS_PATH, "JCMT")
BENCHMARKING_APEX_PATH = os.path.join(BENCHMARKING_CONFIGS_PATH, "APEX")

STANDARD_SETUP = 'standard'
CUSTOM_SETUP = 'custom'
# TODO: are these benchmarking setups still required?
BENCHMARKING_APEX = 'apex'
BENCHMARKING_JCMT = 'jcmt'


class Config:
    """
    Sets up the configuration used to perform the sensitivity calculations.

    Attributes
    ----------

    Methods
    -------
    """
    # def __init__(self, user_input, setup="setup_inputs.yaml", fixed="fixed_inputs.yaml",
    #              default="default_inputs.yaml"):
    def __init__(self, user_input, setup='standard', file_path=None, setup_inputs_file="setup_inputs.yaml",
                 default_inputs_file="default_inputs.yaml"):
        """
        Initialises all the required parameters from various input sources
        setup_input, fixed_input and the default can be found in .yaml files in the configs directory
        User input is here read as dict but class methods allow reading various file types.

        :param user_input: A dictionary of user inputs of structure {'param_name':{'value': , 'unit': }}
        :type user_input: dict
        :param setup: The required telescope setup. Default value 'standard'
        """

        if setup == STANDARD_SETUP:
            config_path = STANDARD_CONFIG_PATH
        elif setup == BENCHMARKING_JCMT:
            config_path = BENCHMARKING_JCMT_PATH
        elif setup == BENCHMARKING_JCMT:
            config_path = BENCHMARKING_APEX_PATH
        elif setup == CUSTOM_SETUP:
            # User is expected to provide the path
            # TODO: figure out how to make this easy for the user
            # TODO: report an error if the file path is not provided
            config_path = file_path
        else:
            # TODO need some error handling/data validation
            pass

        # TODO: remove conversion from yaml. This object should be initialised with dicts
        #       that have already been converted from yamls
        inputs_dict = {}
        # Build up the dictionary of inputs in the order: defaults, setup, user input
        if default_inputs_file:
            inputs_dict = self._dict_from_yaml(config_path, default_inputs_file)
        if setup_inputs_file:
            inputs_dict = inputs_dict | self._dict_from_yaml(config_path, setup_inputs_file)
        inputs_dict = inputs_dict | user_input

        # TODO: do we want to keep this and make it part of the object?
        #       Or, do we want a function that can be called by the Calculator object?
        self.calculation_inputs = inputs.CalculationInput(**inputs_dict)

        # TODO: provide accessor methods for properties
        # TODO: get a list of properties that are editable and provide setters


    # TODO: review which of these utility methods we want/need, and move to a utitilies class
    @classmethod
    def from_yaml(cls, path, file_name):
        """
        Takes a .yaml input file of user inputs and returns an instance of ``Config``

        :param path: the path to the input .yaml file
        :type path: str
        :param file_name: the name of input file
        :type path: str
        """
        inputs = cls._dict_from_yaml(path, file_name)
        return Config(inputs)

    @classmethod
    def from_json(cls, path):
        """
        Takes a .json input file of user inputs and returns an instance of Config

        :param path: the path of the input json file
        :type path: str
        """
        with open(path, "r") as json_file:
            inputs = json.load(json_file)
        return Config(inputs)


    @classmethod
    def to_file(cls, params, path):
        """
        Write config parameters to file
        
        :param path: the path of the output log file
        :type path: str
        """
        # TODO update docstring
        with open(path, "w") as f:
            for key, value in params._iter():
                f.write(f"{key} = {value} \n")

    @classmethod
    def to_yaml(cls, params, path):
        # TODO: docstring
        with open(path, "w") as f:
            for key, value in params._iter():
                if hasattr(value, "unit"):
                    unit = value.unit
                    f.write(f"{key: <16}: {{value: {value: >10}, unit: {unit}}} \n")
                else:
                    # TODO: do we need 'none' for unit?
                    f.write(f"{key: <16}: {{value: {value: >10}, unit: none}} \n")

    @classmethod
    def _dict_from_yaml(cls, path, file_name):
        """
        Read input from a .yaml file and return a dictionary

        :param path: the .yaml file with parameters described as param_name: {value:param_value, unit:param_unit}
        :type path: str (file path)
        """

        file_path = os.path.join(path, file_name)
        with open(file_path, "r") as yaml_file:
            inputs = load(yaml_file, Loader=Loader)
        return inputs