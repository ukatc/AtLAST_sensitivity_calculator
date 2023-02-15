from atlast_sc import inputs
from atlast_sc import constants
from atlast_sc import utils


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

        if setup == constants.STANDARD_SETUP:
            config_path = constants.STANDARD_CONFIG_PATH
        elif setup == constants.BENCHMARKING_JCMT:
            config_path = constants.BENCHMARKING_JCMT_PATH
        elif setup == constants.BENCHMARKING_JCMT:
            config_path = constants.BENCHMARKING_APEX_PATH
        elif setup == constants.CUSTOM_SETUP:
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
            inputs_dict = utils.from_yaml(config_path, default_inputs_file)
        if setup_inputs_file:
            inputs_dict = inputs_dict | utils.from_yaml(config_path, setup_inputs_file)
        inputs_dict = inputs_dict | user_input

        # TODO: do we want to keep this and make it part of the object?
        #       Or, do we want a function that can be called by the Calculator object?
        self.calculation_inputs = inputs.CalculationInput(**inputs_dict)

        # TODO: provide accessor methods for properties
        # TODO: get a list of properties that are editable and provide setters
