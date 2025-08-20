from atlast_sc.calculator import Calculator
from atlast_sc.parameter_setup import ParameterSetup
from atlast_sc.parameters.user_input_parameters import UserInputParameters
from atlast_sc.parameters.instrument_specific_parameters import InstrumentSpecificParameters
from atlast_sc.parameters.telescope_and_environment_parameters import TelescopeAndEnvironmentParameters
from atlast_sc.models import UserInput

class CalculatorFactory:
    def __init__(self, user_input={}, instrument_setup={}, telescope_and_environment= {}, finetune=False):

        # Make sure the user input doesn't contain any unexpected parameter
        # names
        self._check_input_param_names(user_input)

        # Store the input parameters used to initialise the calculator
        self._param_setup = ParameterSetup(user_input, instrument_setup, telescope_and_environment, finetune)
        # Calculate the derived parameters used in the calculation
        self._uip = UserInputParameters(self._param_setup)
        self._isp = InstrumentSpecificParameters(self._param_setup)
        self._tep = TelescopeAndEnvironmentParameters(self._param_setup)
        self.calculator = Calculator(self._param_setup, self._uip, self._isp, self._tep)

    #####################
    # Protected methods #
    #####################

    @staticmethod
    def _check_input_param_names(user_input):
        """
        Validates the user input parameters (just the names; value validation
        is handled by the model)

        :param user_input: Dictionary containing user-defined input parameters
        :type user_input: dict
        """

        test_model = UserInput()

        for param in user_input:
            if param not in test_model.__dict__:
                raise ValueError(f'"{param}" is not a valid input parameter')