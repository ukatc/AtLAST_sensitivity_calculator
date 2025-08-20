import copy
from atlast_sc.models import UserInput
from atlast_sc.models import InstrumentSpecific
from atlast_sc.models import CalculationInput
from atlast_sc.models import TelescopeAndEnvironment
from atlast_sc.utils import Decorators

class ParameterSetup:
    """
    Class that holds the user input and instrument setup parameters
    used to perform the sensitivity calculations.
    """
    def __init__(self, user_input={}, instrument_specific={}, telescope_and_environment={}, finetune=False):
        """
        Initialises all the required parameters from user_input and
        instrument_specific.

        :param user_input: A dictionary of user inputs of structure
        {'param_name':{'value': <value>, 'unit': <unit>}}
        :type user_input: dict
        :param instrument_specific: A dictionary of instrument setup parameters
        of structure
        {'param_name':{'value': <value>, 'unit': <unit>}}
        :type instrument_specific: dict
        """
        self.finetune = finetune

        new_user_input = UserInput(**user_input)
        new_instrument_specific = InstrumentSpecific(**instrument_specific)
        new_telescope_and_environment = TelescopeAndEnvironment(**telescope_and_environment)
        
        self._calculation_inputs = \
            CalculationInput(user_input=new_user_input,
                             instrument_specific=new_instrument_specific,
                             telescope_and_environment=new_telescope_and_environment)

        # Make a deep copy of the calculation inputs to enable the
        # calculator to be reset to its initial setup
        self._original_inputs = copy.deepcopy(self._calculation_inputs)

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
    def instrument_specific(self):
        """
        Instrument specific parameters
        """
        return self._calculation_inputs.instrument_specific
    
    @property
    def telescope_and_environment(self):
        """
        Telescope and environment parameters
        """
        return self._calculation_inputs.telescope_and_environment

    def reset(self):

        """
        Resets the calculator configuration parameters (user input and
        instrument setup to their original values.
        """
        self._calculation_inputs = \
            self._original_inputs
