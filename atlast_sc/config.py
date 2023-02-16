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
    def __init__(self, user_input=None, setup='standard', file_path=None,
                 setup_inputs_file=None, default_inputs_file=None):
        """
        Initialises all the required parameters from various input sources
        setup_input, fixed_input and the default can be found in .yaml files
        in the configs directory User input is here read as dict but class
        methods allow reading various file types.

        :param user_input: A dictionary of user inputs of structure
        {'param_name':{'value': <value>, 'unit': <unit>}}
        :type user_input: dict
        :param setup: The required telescope setup. Default value 'standard'
        """

        match setup:
            case constants.STANDARD_SETUP:
                inputs_path = constants.STANDARD_INPUTS_PATH
            case constants.BENCHMARKING_JCMT | constants.BENCHMARKING_APEX:
                # Setup and default inputs are read from yaml files
                setup_inputs_file = constants.SETUP_INPUTS_FILE
                default_inputs_file = constants.DEFAULT_INPUTS_FILE

                # Set the path where the input files are located
                match setup:
                    case constants.BENCHMARKING_JCMT:
                        inputs_path = constants.BENCHMARKING_JCMT_PATH
                    case constants.BENCHMARKING_APEX:
                        inputs_path = constants.BENCHMARKING_APEX_PATH
            # TODO: do we want to support custom input? That is, is there a
            #  use case whereby the user would want to specify their own
            #  instrument setup params? I'm guessing no - confirm.
            case constants.CUSTOM_SETUP:
                inputs_path = file_path
            case _:
                # TODO: need some proper error handling
                return

        inputs_dict = {}
        # Build up the dictionary of inputs in the order: defaults, setup,
        # user input
        if default_inputs_file:
            inputs_dict = utils.from_yaml(inputs_path, default_inputs_file)
        if setup_inputs_file:
            inputs_dict = inputs_dict | utils.from_yaml(inputs_path,
                                                        setup_inputs_file)
        if user_input:
            inputs_dict = inputs_dict | user_input

        self._calculation_inputs = inputs.CalculationInput(**inputs_dict)

    @property
    def calculation_inputs(self):
        return self._calculation_inputs
