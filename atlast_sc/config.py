import copy
from atlast_sc import models


class Config:
    """
    Class that holds the user input and instrument setup parameters
    used to perform the sensitivity calculations.
    """
    def __init__(self, user_input={}, instrument_setup={}):
        """
        Initialises all the required parameters from user_input and
        instrument_setup.

        :param user_input: A dictionary of user inputs of structure
        {'param_name':{'value': <value>, 'unit': <unit>}}
        :type user_input: dict
        :param instrument_setup: A dictionary of instrument setup parameters
        of structure
        {'param_name':{'value': <value>, 'unit': <unit>}}
        :type instrument_setup: dict
        """

        self._user_input = models.UserInput(**user_input)
        self._instrument_setup = models.InstrumentSetup(**instrument_setup)
        self._calculation_inputs = \
            models.CalculationInput(user_input=self._user_input,
                                    instrument_setup=self._instrument_setup)

        # Make a deep copy of the calculation inputs to enable the
        # calculator to be reset to its initial setup
        self._original_inputs = copy.deepcopy(self._calculation_inputs)

    @property
    def calculation_inputs(self):
        """
        Get the calculation inputs (user input and instrument setup)
        """
        return self._calculation_inputs

    @property
    def user_input(self):
        """
        Get the user input parameters
        """
        return self._user_input

    @property
    def instrument_setup(self):
        """
        Get the instrument setup parameters
        """
        return self._instrument_setup

    def reset(self):
        """
        Resets the calculator configuration parameters (user input and
        instrument setup to their original values.
        """
        self._calculation_inputs = \
            self._original_inputs
