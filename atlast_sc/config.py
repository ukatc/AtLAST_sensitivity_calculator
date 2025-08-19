import copy
from atlast_sc.models import UserInput
from atlast_sc.models import InstrumentSetup
from atlast_sc.models import CalculationInput
from atlast_sc.utils import Decorators

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

        new_user_input = UserInput(**user_input)
        new_instrument_setup = InstrumentSetup(**instrument_setup)
        self._calculation_inputs = \
            CalculationInput(user_input=new_user_input,
                             instrument_setup=new_instrument_setup)

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
    def calculation_inputs(self):
        """
        The inputs to the calculation (user input and instrument setup)
        """
        return self._calculation_inputs

    @property
    def user_input(self):
        """
        User inputs to the calculation
        """
        return self._calculation_inputs.user_input

    @property
    def instrument_setup(self):
        """
        Instrument setup parameters
        """
        return self._calculation_inputs.instrument_setup

    def reset(self):

        """
        Resets the calculator configuration parameters (user input and
        instrument setup to their original values.
        """
        self._calculation_inputs = \
            self._original_inputs
