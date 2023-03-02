import copy
from atlast_sc import models


class Config:
    """
    Sets up the configuration used to perform the sensitivity calculations.

    Attributes
    ----------

    Methods
    -------
    """
    def __init__(self, user_input={}, instrument_setup={}):
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

        self._user_input = models.UserInput(**user_input)
        self._instrument_setup = models.InstrumentSetup(**instrument_setup)
        print('instantiating calculation input')
        self._calculation_inputs = \
            models.CalculationInput(user_input=self._user_input,
                                    instrument_setup=self._instrument_setup)

        # Make a deep copy of the calculation inputs to enable the
        # calculator to be reset to its initial setup
        self._original_inputs = copy.deepcopy(self._calculation_inputs)

    @property
    def calculation_inputs(self):
        return self._calculation_inputs

    @calculation_inputs.setter
    def calculation_inputs(self, value):
        self._calculation_inputs = value

    @property
    def original_calculation_inputs(self):
        return self._original_inputs

    def calculation_inputs_as_dict(self):
        return dict(self.calculation_inputs.user_input) \
               | dict(self._calculation_inputs.instrument_setup)
